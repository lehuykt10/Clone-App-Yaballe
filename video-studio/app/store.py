"""Project persistence: one folder per project, state in project.json."""

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path

from .config import settings
from .schemas import Project

_locks: dict[str, asyncio.Lock] = {}


def project_dir(project_id: str) -> Path:
    path = settings.projects_dir / project_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def new_project_id() -> str:
    return uuid.uuid4().hex[:12]


def save(project: Project) -> None:
    path = project_dir(project.id) / "project.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(project.model_dump_json(indent=2), encoding="utf-8")
    tmp.replace(path)


def load(project_id: str) -> Project:
    path = settings.projects_dir / project_id / "project.json"
    if not path.exists():
        raise FileNotFoundError(project_id)
    return Project.model_validate_json(path.read_text(encoding="utf-8"))


def list_projects() -> list[Project]:
    if not settings.projects_dir.exists():
        return []
    projects = []
    for path in settings.projects_dir.glob("*/project.json"):
        projects.append(Project.model_validate_json(path.read_text(encoding="utf-8")))
    return sorted(projects, key=lambda p: p.created_at, reverse=True)


def lock(project_id: str) -> asyncio.Lock:
    return _locks.setdefault(project_id, asyncio.Lock())
