"""Storyboard writer: Claude studies the reference video (frames + transcript) and the
product photos, then writes a shot-by-shot storyboard with generation prompts."""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import anthropic

from .config import settings
from .schemas import ReferenceAnalysis, ReferenceClip, Shot, Storyboard

SYSTEM_PROMPT = """\
You are a senior performance-ad director who makes short vertical product videos \
(TikTok, Reels, Shorts) for e-commerce stores selling to US/UK shoppers. You turn a \
viral reference video into a fresh storyboard for the user's product, and you write \
prompts for an AI video model (Seedance) that receives the product photos as reference images.

How to write the storyboard:
- Keep what makes the reference work (hook, pacing, shot types, camera moves, energy), \
but recreate it with the user's product. Never copy people's identities, brand names or \
logos from the reference.
- Total duration must be within 1 second of the target. Use 3-6 shots of 2-5 seconds each. \
The first shot is the hook and must grab attention within 2 seconds.
- Each shot prompt is self-contained English: subject and action, camera movement and \
framing, lens feel, lighting, setting, mood. Call the product "the product" and describe \
it so it matches the product photos exactly (shape, colour, material). Realistic hands and \
real homes beat studio renders for UGC style.
- Do not ask the video model for on-screen text, captions, subtitles, logos or speech; \
captions and voiceover are added afterwards.
- Voiceover: natural spoken US English, about 2.5 words per second of shot duration, \
benefit-led, ending with a clear call to action. No medical or exaggerated claims \
(no "cure", "treat", "guaranteed"), no fake reviews or fake prices.
- Set copy_reference_motion only for shots whose camera move or motion in the reference \
is distinctive and worth copying; use a 2-5 second slice inside the reference duration, \
at most 3 shots.
- If no reference video is given, build the storyboard from a proven UGC structure: \
hook -> problem -> product demo -> key benefit -> call to action.
"""


def _image_block(path: Path) -> dict:
    media_type = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}}


def build_user_content(
    product_name: str,
    product_description: str,
    target_duration: int,
    product_images: list[Path],
    frames: list[tuple[float, Path]],
    reference_duration: float | None,
    transcript: str,
) -> list[dict]:
    content: list[dict] = [{
        "type": "text",
        "text": (
            f"Product: {product_name}\n"
            f"Product details: {product_description or '(none given)'}\n"
            f"Target duration: {target_duration} seconds, vertical 9:16.\n\n"
            "Product photos (these are passed to the video model as reference images):"
        ),
    }]
    content += [_image_block(p) for p in product_images[:4]]
    if frames:
        content.append({
            "type": "text",
            "text": f"\nReference video ({reference_duration:.1f}s). Sampled frames in order:",
        })
        for ts, path in frames:
            content.append({"type": "text", "text": f"t={ts:.1f}s"})
            content.append(_image_block(path))
        content.append({
            "type": "text",
            "text": f"\nReference video speech transcript:\n{transcript or '(no speech detected)'}",
        })
    else:
        content.append({"type": "text", "text": "\nNo reference video was given."})
    content.append({
        "type": "text",
        "text": "Analyse the reference (if any) and write the storyboard for this product.",
    })
    return content


async def write_storyboard(
    product_name: str,
    product_description: str,
    target_duration: int,
    product_images: list[Path],
    frames: list[tuple[float, Path]],
    reference_duration: float | None,
    transcript: str,
) -> Storyboard:
    if settings.demo_mode:
        return demo_storyboard(product_name, target_duration, reference_duration)

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key or None)
    response = await client.beta.messages.parse(
        model=settings.claude_model,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        # Re-run on Anthropic's recommended fallback model if the request is declined.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": build_user_content(
                product_name, product_description, target_duration,
                product_images, frames, reference_duration, transcript,
            ),
        }],
        output_format=Storyboard,
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("Claude từ chối yêu cầu này — thử đổi mô tả sản phẩm hoặc video mẫu.")
    if response.stop_reason == "max_tokens" or response.parsed_output is None:
        raise RuntimeError("Claude không trả về storyboard hợp lệ — thử lại.")
    return clamp_storyboard(response.parsed_output, reference_duration)


def clamp_storyboard(storyboard: Storyboard, reference_duration: float | None) -> Storyboard:
    """Drop motion references that fall outside the reference video or are too short/long."""
    for shot in storyboard.shots:
        clip = shot.copy_reference_motion
        if clip is None:
            continue
        if reference_duration is None:
            shot.copy_reference_motion = None
            continue
        start = max(0.0, clip.start_s)
        end = min(reference_duration, clip.end_s)
        if end - start < 2.0:
            shot.copy_reference_motion = None
        else:
            shot.copy_reference_motion = ReferenceClip(start_s=start, end_s=min(end, start + 5.0))
    return storyboard


def demo_storyboard(product_name: str, target_duration: int, reference_duration: float | None) -> Storyboard:
    per_shot = target_duration / 4
    motion = ReferenceClip(start_s=0, end_s=min(3.0, reference_duration)) if reference_duration and reference_duration >= 2 else None
    return Storyboard(
        title=f"{product_name} — demo",
        reference_analysis=ReferenceAnalysis(
            hook="(demo) Close-up reveal in the first second.",
            structure="(demo) Hook -> problem -> demo -> CTA",
            style="(demo) Handheld UGC, warm daylight",
            why_it_works="(demo) Fast payoff and a clear benefit.",
        ) if reference_duration else None,
        shots=[
            Shot(duration_s=per_shot, purpose="hook", prompt="Handheld close-up of the product being unboxed on a wooden desk, warm morning light.",
                 voiceover="Stop scrolling if your eyes feel tired every evening.", copy_reference_motion=motion),
            Shot(duration_s=per_shot, purpose="problem", prompt="A young woman rubs her tired eyes in front of a laptop at night, soft blue screen light.",
                 voiceover="Hours of screens leave them strained and heavy."),
            Shot(duration_s=per_shot, purpose="demo", prompt="She puts on the product and leans back on the sofa, slow push-in, cosy lamp light.",
                 voiceover="Ten minutes with this and I actually unwind."),
            Shot(duration_s=per_shot, purpose="cta", prompt="Top-down shot of the product resting on a bed next to a phone, gentle camera orbit.",
                 voiceover="Tap the link to get yours today."),
        ],
        music_mood="calm lo-fi",
    )
