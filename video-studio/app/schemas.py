"""Data models: storyboard (written by Claude) and project state (persisted as JSON)."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class ReferenceClip(BaseModel):
    """A slice of the reference video whose motion/camera work a shot should copy."""

    start_s: float = Field(description="Start time in the reference video, seconds")
    end_s: float = Field(description="End time in the reference video, seconds")


class Shot(BaseModel):
    duration_s: float = Field(description="Shot length in seconds (2-6 typical)")
    purpose: str = Field(description="Role in the ad: hook, problem, demo, benefit, social proof, CTA...")
    prompt: str = Field(
        description=(
            "English video-generation prompt for this shot: subject, action, camera movement, "
            "framing, lighting, setting. Refer to the product as 'the product'."
        )
    )
    voiceover: str = Field(default="", description="English voiceover line spoken during this shot")
    on_screen_text: str = Field(default="", description="Short caption overlay, may be empty")
    copy_reference_motion: ReferenceClip | None = Field(
        default=None,
        description="Set only when this shot should copy camera/motion from a slice of the reference video",
    )


class ReferenceAnalysis(BaseModel):
    hook: str = Field(description="What happens in the first 1-3 seconds and why it stops the scroll")
    structure: str = Field(description="Scene-by-scene structure of the reference video")
    style: str = Field(description="Visual style: UGC/studio, lighting, color, camera, pacing")
    why_it_works: str = Field(description="Why this video performs, in 2-3 sentences")


class Storyboard(BaseModel):
    title: str
    reference_analysis: ReferenceAnalysis | None = None
    shots: list[Shot]
    music_mood: str = Field(default="", description="Suggested background music mood")

    @property
    def total_duration(self) -> float:
        return sum(s.duration_s for s in self.shots)

    @property
    def voiceover_script(self) -> str:
        return " ".join(s.voiceover.strip() for s in self.shots if s.voiceover.strip())


class ProjectStatus(str, Enum):
    draft = "draft"
    analyzing = "analyzing"
    storyboard_ready = "storyboard_ready"
    rendering = "rendering"
    done = "done"
    failed = "failed"


class SegmentStatus(str, Enum):
    pending = "pending"
    running = "running"
    done = "done"
    failed = "failed"


class Segment(BaseModel):
    """One call to the video model. A segment packs several shots (scene cuts) into one clip."""

    index: int
    shot_indexes: list[int]
    duration: int
    prompt: str
    image_urls: list[str] = []
    video_urls: list[str] = []
    status: SegmentStatus = SegmentStatus.pending
    request_id: str | None = None
    video_url: str | None = None
    local_path: str | None = None
    error: str | None = None
    cost_usd: float = 0.0


class RenderSettings(BaseModel):
    video_model: str = "seedance-2.0"
    resolution: str = "720p"
    aspect_ratio: str = "9:16"
    voice: str = "Aria"
    voiceover: bool = True
    subtitles: bool = True
    native_audio_volume: float = 0.25


class Project(BaseModel):
    id: str
    name: str
    product_name: str
    product_description: str = ""
    target_duration: int = 12
    reference_url: str = ""
    reference_video: str | None = None  # local path
    product_images: list[str] = []  # local paths
    uploaded_urls: dict[str, str] = {}  # local path -> fal storage URL
    music: str | None = None
    status: ProjectStatus = ProjectStatus.draft
    progress: str = ""
    error: str | None = None
    transcript: str = ""
    storyboard: Storyboard | None = None
    settings: RenderSettings = RenderSettings()
    segments: list[Segment] = []
    voiceover_path: str | None = None
    final_video: str | None = None
    spent_usd: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
