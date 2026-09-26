"""Registry of video models available through fal.ai, with cost estimation.

Prices are estimates. fal bills Seedance by tokens:
    tokens = width * height * duration * 24 / 1024
and the per-1k-token rate differs per model. Verify on fal.ai before relying on them.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Output frame size (portrait) per resolution; landscape swaps width/height.
RESOLUTION_SIZES: dict[str, tuple[int, int]] = {
    "480p": (480, 854),
    "720p": (720, 1280),
    "1080p": (1080, 1920),
}


@dataclass(frozen=True)
class VideoModel:
    key: str
    label: str
    endpoint: str
    usd_per_1k_tokens: float
    resolutions: tuple[str, ...]
    min_duration: int = 4
    max_duration: int = 15
    max_images: int = 9
    max_videos: int = 3
    max_reference_video_seconds: float = 15.0
    max_total_files: int = 12
    video_input_multiplier: float = 0.6
    notes: str = ""
    extra_args: dict = field(default_factory=dict)

    def usd_per_second(self, resolution: str) -> float:
        width, height = RESOLUTION_SIZES[resolution]
        tokens_per_second = width * height * 24 / 1024
        return tokens_per_second / 1000 * self.usd_per_1k_tokens

    def estimate_usd(self, duration: float, resolution: str, has_video_refs: bool) -> float:
        cost = duration * self.usd_per_second(resolution)
        if has_video_refs:
            cost *= self.video_input_multiplier
        return round(cost, 4)


VIDEO_MODELS: dict[str, VideoModel] = {
    m.key: m
    for m in [
        VideoModel(
            key="seedance-2.0-fast",
            label="Seedance 2.0 Fast (nháp, rẻ nhất)",
            endpoint="bytedance/seedance-2.0/fast/reference-to-video",
            usd_per_1k_tokens=0.0112,
            resolutions=("480p", "720p"),
            notes="Dùng để test prompt nhanh trước khi render bản chính.",
        ),
        VideoModel(
            key="seedance-2.0",
            label="Seedance 2.0 (khuyên dùng)",
            endpoint="bytedance/seedance-2.0/reference-to-video",
            usd_per_1k_tokens=0.014,
            resolutions=("480p", "720p"),
            notes="Cân bằng chất lượng/giá cho video sản phẩm 10-15s.",
        ),
        VideoModel(
            key="seedance-2.5",
            label="Seedance 2.5 (cao cấp)",
            endpoint="bytedance/seedance-2.5/reference-to-video",
            usd_per_1k_tokens=0.024,
            resolutions=("480p", "720p", "1080p"),
            # The model supports longer single takes; keep 15s until fal's limit is confirmed.
            max_duration=15,
            notes="Giữ nhân vật/khẩu hình tốt hơn, đắt hơn ~2-3 lần.",
        ),
    ]
}

DEFAULT_MODEL = "seedance-2.0"

# ElevenLabs via fal, billed per character (estimate).
TTS_ENDPOINT = "fal-ai/elevenlabs/tts/multilingual-v2"
TTS_USD_PER_1K_CHARS = 0.10
TRANSCRIBE_ENDPOINT = "fal-ai/whisper"

ENGLISH_VOICES = ["Aria", "Sarah", "Laura", "Charlotte", "Jessica", "Roger", "Charlie", "George", "Brian", "Daniel"]


def get_model(key: str) -> VideoModel:
    try:
        return VIDEO_MODELS[key]
    except KeyError as exc:
        raise ValueError(f"Unknown video model: {key}") from exc


def frame_size(resolution: str, aspect_ratio: str) -> tuple[int, int]:
    """Final composition frame size for the chosen resolution and aspect ratio."""
    short, long = RESOLUTION_SIZES[resolution]
    if aspect_ratio == "16:9":
        return long, short
    if aspect_ratio == "1:1":
        return short, short
    return short, long  # 9:16 default
