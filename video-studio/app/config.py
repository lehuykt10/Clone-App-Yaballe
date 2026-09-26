"""Runtime settings, read from environment variables (or a .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    """Minimal .env loader so the app runs without python-dotenv."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


ROOT_DIR = Path(__file__).resolve().parent.parent
_load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    fal_key: str
    anthropic_api_key: str
    claude_model: str
    data_dir: Path
    max_parallel_generations: int
    demo_mode: bool

    @property
    def projects_dir(self) -> Path:
        return self.data_dir / "projects"


def load_settings() -> Settings:
    data_dir = Path(os.environ.get("DATA_DIR", "./data"))
    if not data_dir.is_absolute():
        data_dir = ROOT_DIR / data_dir
    return Settings(
        fal_key=os.environ.get("FAL_KEY", ""),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
        claude_model=os.environ.get("CLAUDE_MODEL", "claude-opus-5"),
        data_dir=data_dir,
        max_parallel_generations=int(os.environ.get("MAX_PARALLEL_GENERATIONS", "2")),
        demo_mode=os.environ.get("DEMO_MODE", "0") == "1",
    )


settings = load_settings()
