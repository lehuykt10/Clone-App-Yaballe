"""Orchestration: reference analysis -> storyboard -> clip generation -> voiceover -> final video."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from . import analyzer, generator, media, store
from .config import settings
from .schemas import Project, ProjectStatus, RenderSettings, Segment, SegmentStatus, Storyboard
from .video_models import TTS_USD_PER_1K_CHARS, frame_size, get_model

log = logging.getLogger(__name__)


# ---------------------------------------------------------------- cost estimate

def estimate_cost(storyboard: Storyboard, render: RenderSettings) -> dict:
    model = get_model(render.video_model)
    groups = generator.plan_segments(storyboard, model)
    segments = []
    video_total = 0.0
    for group in groups:
        shots = [storyboard.shots[i] for i in group]
        duration = generator.segment_duration(shots, model)
        has_refs = any(s.copy_reference_motion for s in shots)
        cost = model.estimate_usd(duration, render.resolution, has_refs)
        video_total += cost
        segments.append({"shots": group, "duration": duration, "usd": cost, "video_reference": has_refs})
    tts = len(storyboard.voiceover_script) / 1000 * TTS_USD_PER_1K_CHARS if render.voiceover else 0.0
    return {
        "model": model.label,
        "resolution": render.resolution,
        "usd_per_second": round(model.usd_per_second(render.resolution), 4),
        "segments": segments,
        "video_usd": round(video_total, 3),
        "voiceover_usd": round(tts, 3),
        "total_usd": round(video_total + tts, 3),
        "note": "Ước tính theo bảng giá fal.ai; mỗi lần tạo lại tốn thêm tương ứng.",
    }


# ---------------------------------------------------------------- helpers

def _update(project: Project, **fields) -> None:
    for key, value in fields.items():
        setattr(project, key, value)
    store.save(project)


async def _uploaded(project: Project, path: str) -> str:
    """Upload a local file to fal storage once; reuse the URL afterwards."""
    if path not in project.uploaded_urls:
        project.uploaded_urls[path] = await generator.upload(Path(path))
        store.save(project)
    return project.uploaded_urls[path]


# ---------------------------------------------------------------- step 1: analyze

async def analyze(project_id: str) -> None:
    project = store.load(project_id)
    work = store.project_dir(project_id)
    try:
        media.require_ffmpeg()
        _update(project, status=ProjectStatus.analyzing, error=None, progress="Đang chuẩn bị video mẫu…")

        if project.reference_url and not project.reference_video:
            _update(project, progress="Đang tải video mẫu từ link…")
            path = await media.download_social_video(project.reference_url, work / "reference")
            _update(project, reference_video=str(path))

        frames: list[tuple[float, Path]] = []
        ref_duration: float | None = None
        transcript = ""
        if project.reference_video:
            ref = Path(project.reference_video)
            ref_duration = await media.duration_of(ref)
            _update(project, progress="Đang cắt khung hình video mẫu…")
            frames = await media.extract_frames(ref, work / "frames")
            if not settings.demo_mode:
                _update(project, progress="Đang nghe lời thoại video mẫu (Whisper)…")
                try:
                    audio = await media.extract_audio(ref, work / "reference_audio.mp3")
                    if audio:
                        transcript = await generator.transcribe(audio)
                except Exception as exc:  # transcript is a nice-to-have
                    log.warning("transcription failed: %s", exc)

        _update(project, transcript=transcript, progress="Claude đang phân tích và viết storyboard…")
        storyboard = await analyzer.write_storyboard(
            project.product_name,
            project.product_description,
            project.target_duration,
            [Path(p) for p in project.product_images],
            frames,
            ref_duration,
            transcript,
        )
        _update(project, storyboard=storyboard, status=ProjectStatus.storyboard_ready, progress="Storyboard sẵn sàng — hãy xem và sửa trước khi render.")
    except Exception as exc:
        log.exception("analyze failed")
        _update(project, status=ProjectStatus.failed, error=str(exc), progress="")


# ---------------------------------------------------------------- step 2: render

async def _prepare_segments(project: Project) -> list[Segment]:
    storyboard = project.storyboard
    assert storyboard is not None
    model = get_model(project.settings.video_model)
    work = store.project_dir(project.id)

    image_urls = []
    if not settings.demo_mode:
        for path in project.product_images[: model.max_images]:
            image_urls.append(await _uploaded(project, path))

    segments = []
    for n, group in enumerate(generator.plan_segments(storyboard, model)):
        shots = [storyboard.shots[i] for i in group]
        video_urls: list[str] = []
        video_numbers: list[int | None] = []
        for i, shot in zip(group, shots):
            clip = shot.copy_reference_motion
            usable = (
                clip is not None
                and project.reference_video
                and len(video_urls) < model.max_videos
                and len(image_urls) + len(video_urls) < model.max_total_files
            )
            if not usable:
                video_numbers.append(None)
                continue
            clip_path = await media.trim(Path(project.reference_video), clip.start_s, clip.end_s, work / f"refclip_{i:02d}.mp4")
            video_urls.append("demo" if settings.demo_mode else await _uploaded(project, str(clip_path)))
            video_numbers.append(len(video_urls))
        segments.append(Segment(
            index=n,
            shot_indexes=group,
            duration=generator.segment_duration(shots, model),
            prompt=generator.build_segment_prompt(shots, len(image_urls), video_numbers, project.settings.aspect_ratio),
            image_urls=image_urls,
            video_urls=video_urls,
        ))
    return segments


async def _run_segment(project: Project, segment: Segment, semaphore: asyncio.Semaphore) -> None:
    model = get_model(project.settings.video_model)
    work = store.project_dir(project.id)
    render = project.settings
    async with semaphore:
        segment.status = SegmentStatus.running
        segment.error = None
        store.save(project)
        try:
            out = work / "clips" / f"segment_{segment.index:02d}.mp4"
            out.parent.mkdir(exist_ok=True)
            if settings.demo_mode:
                w, h = frame_size(render.resolution, render.aspect_ratio)
                await media.make_test_clip(out, segment.duration, w, h, f"Segment {segment.index + 1}")
                segment.video_url = None
            else:
                result = await generator.generate_segment(segment, model, render.resolution, render.aspect_ratio)
                segment.video_url = result["video"]["url"]
                await media.download(segment.video_url, out)
                segment.cost_usd = model.estimate_usd(segment.duration, render.resolution, bool(segment.video_urls))
                project.spent_usd = round(project.spent_usd + segment.cost_usd, 4)
            segment.local_path = str(out)
            segment.status = SegmentStatus.done
        except Exception as exc:
            log.exception("segment %s failed", segment.index)
            segment.status = SegmentStatus.failed
            segment.error = str(exc)
        store.save(project)


async def _voiceover(project: Project) -> Path | None:
    storyboard = project.storyboard
    if not project.settings.voiceover or storyboard is None or not storyboard.voiceover_script:
        return None
    out = store.project_dir(project.id) / "voiceover.mp3"
    if settings.demo_mode:
        return await media.make_silent_voice(out, storyboard.total_duration)
    await generator.text_to_speech(storyboard.voiceover_script, project.settings.voice, out)
    project.spent_usd = round(project.spent_usd + len(storyboard.voiceover_script) / 1000 * TTS_USD_PER_1K_CHARS, 4)
    return out


def _subtitle_cues(project: Project, video_duration: float) -> list[tuple[float, float, str]]:
    """Time each shot's voiceover line to where that shot lands in the final video."""
    storyboard = project.storyboard
    assert storyboard is not None
    cues = []
    offset = 0.0
    for segment in project.segments:
        shots = [storyboard.shots[i] for i in segment.shot_indexes]
        planned = sum(s.duration_s for s in shots) or 1.0
        scale = segment.duration / planned
        t = offset
        for shot in shots:
            length = shot.duration_s * scale
            cues.append((t, t + length, shot.voiceover))
            t += length
        offset += segment.duration
    # Compensate for small differences between requested and delivered clip lengths.
    ratio = video_duration / offset if offset else 1.0
    return [(s * ratio, e * ratio, text) for s, e, text in cues]


async def _compose(project: Project) -> None:
    render = project.settings
    work = store.project_dir(project.id)
    clips = [Path(s.local_path) for s in project.segments if s.local_path]
    _update(project, progress="Đang tạo giọng đọc…")
    voice = await _voiceover(project)
    _update(project, voiceover_path=str(voice) if voice else None, progress="Đang ghép video, giọng đọc và phụ đề…")
    w, h = frame_size(render.resolution, render.aspect_ratio)
    total = float(sum(s.duration for s in project.segments))
    srt = media.build_srt(_subtitle_cues(project, total)) if render.subtitles else None
    out = work / "final.mp4"
    await media.compose(
        clips, out, work / "compose", w, h,
        voiceover=voice,
        music=Path(project.music) if project.music else None,
        srt_text=srt,
        native_audio_volume=render.native_audio_volume,
    )
    _update(project, final_video=str(out), status=ProjectStatus.done, progress="Hoàn thành!")


async def render(project_id: str, render_settings: RenderSettings) -> None:
    project = store.load(project_id)
    try:
        media.require_ffmpeg()
        if project.storyboard is None:
            raise RuntimeError("Chưa có storyboard — chạy bước phân tích trước.")
        get_model(render_settings.video_model)  # validate
        _update(project, settings=render_settings, status=ProjectStatus.rendering, error=None,
                final_video=None, progress="Đang chuẩn bị ảnh sản phẩm và clip tham chiếu…")
        project.segments = await _prepare_segments(project)
        _update(project, progress=f"Đang tạo {len(project.segments)} clip bằng {get_model(render_settings.video_model).label}…")
        semaphore = asyncio.Semaphore(settings.max_parallel_generations)
        await asyncio.gather(*(_run_segment(project, s, semaphore) for s in project.segments))
        failed = [s for s in project.segments if s.status == SegmentStatus.failed]
        if failed:
            raise RuntimeError(f"{len(failed)} clip bị lỗi — bấm 'Tạo lại' ở clip đó. Lỗi đầu tiên: {failed[0].error}")
        await _compose(project)
    except Exception as exc:
        log.exception("render failed")
        _update(project, status=ProjectStatus.failed, error=str(exc), progress="")


async def regenerate_segment(project_id: str, index: int, prompt: str | None = None) -> None:
    """Re-roll a single clip (optionally with an edited prompt), then rebuild the final video."""
    project = store.load(project_id)
    try:
        segment = next(s for s in project.segments if s.index == index)
        if prompt:
            segment.prompt = prompt
        _update(project, status=ProjectStatus.rendering, error=None, progress=f"Đang tạo lại clip {index + 1}…")
        await _run_segment(project, segment, asyncio.Semaphore(1))
        if segment.status == SegmentStatus.failed:
            raise RuntimeError(f"Clip {index + 1} lỗi: {segment.error}")
        if all(s.status == SegmentStatus.done for s in project.segments):
            await _compose(project)
        else:
            _update(project, status=ProjectStatus.failed, error="Còn clip khác bị lỗi — tạo lại các clip đó.", progress="")
    except Exception as exc:
        log.exception("regenerate failed")
        _update(project, status=ProjectStatus.failed, error=str(exc), progress="")
