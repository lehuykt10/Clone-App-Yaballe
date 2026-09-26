"""fal.ai calls: file upload, Seedance reference-to-video, ElevenLabs TTS, Whisper transcription."""

from __future__ import annotations

import os
from pathlib import Path

import fal_client

from .config import settings
from .schemas import Segment, Shot, Storyboard
from .video_models import TRANSCRIBE_ENDPOINT, TTS_ENDPOINT, VideoModel


def _ensure_key() -> None:
    if settings.fal_key:
        os.environ["FAL_KEY"] = settings.fal_key
    if not os.environ.get("FAL_KEY"):
        raise RuntimeError("Chưa có FAL_KEY trong file .env")


async def upload(path: Path) -> str:
    _ensure_key()
    return await fal_client.upload_file_async(path)


def plan_segments(storyboard: Storyboard, model: VideoModel) -> list[list[int]]:
    """Greedily pack consecutive shots into model calls no longer than the model's max duration.

    Seedance handles scene cuts inside one clip, so fewer, longer calls keep the product and
    lighting consistent and avoid paying the minimum duration several times.
    """
    groups: list[list[int]] = []
    current: list[int] = []
    current_len = 0.0
    refs_in_current = 0
    for i, shot in enumerate(storyboard.shots):
        has_ref = shot.copy_reference_motion is not None
        too_long = current_len + shot.duration_s > model.max_duration + 0.5
        too_many_refs = has_ref and refs_in_current >= model.max_videos
        if current and (too_long or too_many_refs):
            groups.append(current)
            current, current_len, refs_in_current = [], 0.0, 0
        current.append(i)
        current_len += shot.duration_s
        refs_in_current += int(has_ref)
    if current:
        groups.append(current)
    return groups


def segment_duration(shots: list[Shot], model: VideoModel) -> int:
    total = round(sum(s.duration_s for s in shots))
    return max(model.min_duration, min(model.max_duration, total))


def build_segment_prompt(
    shots: list[Shot], image_count: int, video_ref_numbers: list[int | None], aspect_ratio: str
) -> str:
    """Compose one Seedance prompt with timed scene cuts.

    video_ref_numbers[i] is the @VideoN number for shot i, or None.
    """
    images = ", ".join(f"@Image{n}" for n in range(1, image_count + 1))
    header = (
        f"Vertical {aspect_ratio} social media product video, photorealistic, natural UGC look. "
        f"The product is shown in {images}: keep its exact shape, colours, materials and details "
        "in every scene. No on-screen text, no captions, no logos, no one speaking to camera; "
        "only natural ambient sound."
    ) if image_count else (
        f"Vertical {aspect_ratio} social media product video, photorealistic, natural UGC look. "
        "No on-screen text, no captions, no logos, no one speaking to camera; only natural ambient sound."
    )
    parts = [header]
    t = 0.0
    for i, shot in enumerate(shots):
        start, end = t, t + shot.duration_s
        t = end
        text = shot.prompt.strip().rstrip(".")
        if image_count:
            text = text.replace("the product", "the product (@Image1)", 1)
        video_n = video_ref_numbers[i]
        if video_n is not None:
            text += f". Follow the camera movement and motion of @Video{video_n}, but with this scene's subject and setting"
        prefix = "" if i == 0 else "Cut scene to: "
        parts.append(f"{prefix}[{start:.0f}s-{end:.0f}s] {text}.")
    return "\n".join(parts)


async def generate_segment(segment: Segment, model: VideoModel, resolution: str, aspect_ratio: str) -> dict:
    """Submit one clip to fal and wait for the result. Returns the raw fal response."""
    _ensure_key()
    arguments = {
        "prompt": segment.prompt,
        "resolution": resolution,
        "duration": str(segment.duration),
        "aspect_ratio": aspect_ratio,
        "generate_audio": True,
        **model.extra_args,
    }
    if segment.image_urls:
        arguments["image_urls"] = segment.image_urls[: model.max_images]
    if segment.video_urls:
        arguments["video_urls"] = segment.video_urls[: model.max_videos]
    handle = await fal_client.submit_async(model.endpoint, arguments=arguments)
    segment.request_id = handle.request_id
    return await handle.get()


async def text_to_speech(text: str, voice: str, out_path: Path) -> Path:
    from .media import download

    _ensure_key()
    result = await fal_client.subscribe_async(
        TTS_ENDPOINT, arguments={"text": text, "voice": voice, "stability": 0.5, "similarity_boost": 0.75, "speed": 1.0}
    )
    return await download(result["audio"]["url"], out_path)


async def transcribe(audio_path: Path) -> str:
    """Speech in the reference video, so Claude can study its script. Failures are non-fatal."""
    _ensure_key()
    url = await fal_client.upload_file_async(audio_path)
    result = await fal_client.subscribe_async(TRANSCRIBE_ENDPOINT, arguments={"audio_url": url, "task": "transcribe"})
    chunks = result.get("chunks") or []
    if chunks:
        lines = []
        for chunk in chunks:
            start, end = (chunk.get("timestamp") or [0, 0])[:2]
            lines.append(f"[{start or 0:.1f}-{end or 0:.1f}s] {chunk.get('text', '').strip()}")
        return "\n".join(lines)
    return (result.get("text") or "").strip()
