"""FastAPI app: REST API + static single-page UI.

Run:  uvicorn app.main:app --reload --port 8100
"""

from __future__ import annotations

import asyncio
import logging
import re
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import pipeline, store
from .config import ROOT_DIR, settings
from .schemas import Project, ProjectStatus, RenderSettings, Storyboard
from .video_models import DEFAULT_MODEL, ENGLISH_VOICES, VIDEO_MODELS

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Video Studio")
_tasks: set[asyncio.Task] = set()

ALLOWED_IMAGE = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO = {".mp4", ".mov", ".webm", ".m4v"}
ALLOWED_AUDIO = {".mp3", ".wav", ".m4a", ".aac"}


def _background(coro) -> None:
    task = asyncio.create_task(coro)
    _tasks.add(task)
    task.add_done_callback(_tasks.discard)


def _get(project_id: str) -> Project:
    if not re.fullmatch(r"[0-9a-f]{12}", project_id):
        raise HTTPException(404, "Không tìm thấy project")
    try:
        return store.load(project_id)
    except FileNotFoundError:
        raise HTTPException(404, "Không tìm thấy project") from None


def _busy(project: Project) -> bool:
    return project.status in (ProjectStatus.analyzing, ProjectStatus.rendering)


async def _save_upload(upload: UploadFile, dest_dir: Path, name: str, allowed: set[str]) -> str:
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, f"File {upload.filename} không đúng định dạng ({', '.join(sorted(allowed))})")
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"{name}{suffix}"
    with path.open("wb") as fh:
        while chunk := await upload.read(1 << 20):
            fh.write(chunk)
    return str(path)


def _public(project: Project) -> dict:
    """Project JSON for the UI, with local paths turned into /media URLs."""
    data = project.model_dump(mode="json")

    def url(path: str | None) -> str | None:
        if not path:
            return None
        rel = Path(path).resolve().relative_to(store.project_dir(project.id).resolve())
        return f"/media/{project.id}/{rel.as_posix()}"

    data["product_images"] = [url(p) for p in project.product_images]
    data["reference_video"] = url(project.reference_video)
    data["final_video"] = url(project.final_video)
    data["voiceover_path"] = url(project.voiceover_path)
    data["music"] = url(project.music)
    for seg, raw in zip(data["segments"], project.segments):
        seg["local_path"] = url(raw.local_path)
    data.pop("uploaded_urls", None)
    if project.storyboard:
        data["estimate"] = pipeline.estimate_cost(project.storyboard, project.settings)
    return data


# ---------------------------------------------------------------- API

@app.get("/api/config")
def get_config() -> dict:
    return {
        "demo_mode": settings.demo_mode,
        "has_fal_key": bool(settings.fal_key),
        "has_anthropic_key": bool(settings.anthropic_api_key),
        "default_model": DEFAULT_MODEL,
        "voices": ENGLISH_VOICES,
        "models": [
            {
                "key": m.key,
                "label": m.label,
                "notes": m.notes,
                "resolutions": list(m.resolutions),
                "usd_per_second": {r: round(m.usd_per_second(r), 4) for r in m.resolutions},
                "max_duration": m.max_duration,
            }
            for m in VIDEO_MODELS.values()
        ],
    }


@app.get("/api/projects")
def list_projects() -> list[dict]:
    return [
        {"id": p.id, "name": p.name, "status": p.status, "created_at": p.created_at, "spent_usd": p.spent_usd}
        for p in store.list_projects()
    ]


@app.post("/api/projects")
async def create_project(
    product_name: str = Form(...),
    product_description: str = Form(""),
    target_duration: int = Form(12),
    reference_url: str = Form(""),
    product_images: list[UploadFile] = File(...),
    reference_video: UploadFile | None = File(None),
    music: UploadFile | None = File(None),
) -> dict:
    if not 4 <= target_duration <= 60:
        raise HTTPException(400, "Thời lượng phải từ 4 đến 60 giây")
    images = [f for f in product_images if f.filename]
    if not images:
        raise HTTPException(400, "Cần ít nhất 1 ảnh sản phẩm")
    if len(images) > 9:
        raise HTTPException(400, "Tối đa 9 ảnh sản phẩm")

    project_id = store.new_project_id()
    folder = store.project_dir(project_id)
    project = Project(
        id=project_id,
        name=product_name.strip()[:80],
        product_name=product_name.strip(),
        product_description=product_description.strip(),
        target_duration=target_duration,
        reference_url=reference_url.strip(),
    )
    project.product_images = [
        await _save_upload(f, folder / "product", f"image_{i}", ALLOWED_IMAGE) for i, f in enumerate(images)
    ]
    if reference_video and reference_video.filename:
        project.reference_video = await _save_upload(reference_video, folder / "reference", "reference", ALLOWED_VIDEO)
    if music and music.filename:
        project.music = await _save_upload(music, folder, "music", ALLOWED_AUDIO)
    store.save(project)
    return _public(project)


@app.get("/api/projects/{project_id}")
def get_project(project_id: str) -> dict:
    return _public(_get(project_id))


@app.post("/api/projects/{project_id}/analyze")
async def analyze(project_id: str) -> dict:
    project = _get(project_id)
    if _busy(project):
        raise HTTPException(409, "Project đang chạy")
    if not settings.demo_mode and not settings.anthropic_api_key:
        raise HTTPException(400, "Chưa có ANTHROPIC_API_KEY trong .env")
    project.status = ProjectStatus.analyzing
    store.save(project)
    _background(pipeline.analyze(project_id))
    return _public(project)


@app.put("/api/projects/{project_id}/storyboard")
def update_storyboard(project_id: str, storyboard: Storyboard) -> dict:
    project = _get(project_id)
    if _busy(project):
        raise HTTPException(409, "Project đang chạy")
    if not storyboard.shots:
        raise HTTPException(400, "Storyboard cần ít nhất 1 cảnh")
    project.storyboard = storyboard
    store.save(project)
    return _public(project)


@app.post("/api/projects/{project_id}/estimate")
def estimate(project_id: str, render: RenderSettings) -> dict:
    project = _get(project_id)
    if project.storyboard is None:
        raise HTTPException(400, "Chưa có storyboard")
    _validate_render(render)
    return pipeline.estimate_cost(project.storyboard, render)


def _validate_render(render: RenderSettings) -> None:
    model = VIDEO_MODELS.get(render.video_model)
    if model is None:
        raise HTTPException(400, "Model không hợp lệ")
    if render.resolution not in model.resolutions:
        raise HTTPException(400, f"{model.label} không hỗ trợ {render.resolution}")
    if render.aspect_ratio not in ("9:16", "16:9", "1:1"):
        raise HTTPException(400, "Tỉ lệ khung hình không hợp lệ")


@app.post("/api/projects/{project_id}/render")
async def render(project_id: str, render: RenderSettings) -> dict:
    project = _get(project_id)
    if _busy(project):
        raise HTTPException(409, "Project đang chạy")
    if project.storyboard is None:
        raise HTTPException(400, "Chưa có storyboard")
    _validate_render(render)
    if not settings.demo_mode and not settings.fal_key:
        raise HTTPException(400, "Chưa có FAL_KEY trong .env")
    project.status = ProjectStatus.rendering
    store.save(project)
    _background(pipeline.render(project_id, render))
    return _public(project)


class RegenerateRequest(BaseModel):
    prompt: str | None = None


@app.post("/api/projects/{project_id}/segments/{index}/regenerate")
async def regenerate(project_id: str, index: int, body: RegenerateRequest) -> dict:
    project = _get(project_id)
    if _busy(project):
        raise HTTPException(409, "Project đang chạy")
    if not any(s.index == index for s in project.segments):
        raise HTTPException(404, "Không có clip này")
    project.status = ProjectStatus.rendering
    store.save(project)
    _background(pipeline.regenerate_segment(project_id, index, body.prompt))
    return _public(project)


@app.get("/media/{project_id}/{file_path:path}")
def media_file(project_id: str, file_path: str) -> FileResponse:
    _get(project_id)
    base = store.project_dir(project_id).resolve()
    path = (base / file_path).resolve()
    if not path.is_relative_to(base) or not path.is_file() or path.name == "project.json":
        raise HTTPException(404, "Không có file")
    return FileResponse(path)


app.mount("/", StaticFiles(directory=ROOT_DIR / "static", html=True), name="static")
