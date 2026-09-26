"""End-to-end run in DEMO_MODE: real ffmpeg, no paid API calls."""

import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")


def make_inputs(tmp: Path) -> tuple[Path, Path]:
    image = tmp / "product.png"
    video = tmp / "ref.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=orange:s=400x400", "-frames:v", "1", str(image)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=540x960:rate=24:duration=6",
                    "-f", "lavfi", "-i", "sine=duration=6", "-shortest", "-pix_fmt", "yuv420p", str(video)], check=True)
    return image, video


def wait_for(client, pid, statuses, timeout=120):
    import time
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = client.get(f"/api/projects/{pid}").json()
        if data["status"] in statuses:
            return data
        time.sleep(0.5)
    raise AssertionError(f"timeout, last status {data['status']}: {data.get('error')}")


def test_full_flow(tmp_path):
    image, video = make_inputs(tmp_path)
    with TestClient(app) as client:
        assert client.get("/api/config").json()["demo_mode"] is True
        with image.open("rb") as img, video.open("rb") as vid:
            res = client.post(
                "/api/projects",
                data={"product_name": "Eye Massager", "product_description": "heated", "target_duration": "12"},
                files=[("product_images", ("p.png", img, "image/png")), ("reference_video", ("r.mp4", vid, "video/mp4"))],
            )
        assert res.status_code == 200, res.text
        pid = res.json()["id"]

        assert client.post(f"/api/projects/{pid}/analyze").status_code == 200
        data = wait_for(client, pid, {"storyboard_ready", "failed"})
        assert data["status"] == "storyboard_ready", data["error"]
        assert len(data["storyboard"]["shots"]) == 4
        assert data["estimate"]["total_usd"] > 0

        sb = data["storyboard"]
        sb["shots"][1]["voiceover"] = "Edited line for the second shot."
        assert client.put(f"/api/projects/{pid}/storyboard", json=sb).status_code == 200

        settings = {"video_model": "seedance-2.0-fast", "resolution": "480p", "aspect_ratio": "9:16"}
        assert client.post(f"/api/projects/{pid}/render", json=settings).status_code == 200
        data = wait_for(client, pid, {"done", "failed"})
        assert data["status"] == "done", data["error"]
        assert data["segments"][0]["video_urls"] == ["demo"]  # motion reference was trimmed and attached

        final = client.get(data["final_video"])
        assert final.status_code == 200 and len(final.content) > 10_000

        assert client.post(f"/api/projects/{pid}/segments/0/regenerate", json={"prompt": "new prompt"}).status_code == 200
        data = wait_for(client, pid, {"done", "failed"})
        assert data["status"] == "done", data["error"]
        assert data["segments"][0]["prompt"] == "new prompt"


def test_rejects_bad_render_settings(tmp_path):
    image, _ = make_inputs(tmp_path)
    with TestClient(app) as client:
        with image.open("rb") as img:
            pid = client.post("/api/projects", data={"product_name": "X"},
                              files=[("product_images", ("p.png", img, "image/png"))]).json()["id"]
        assert client.post(f"/api/projects/{pid}/render", json={}).status_code == 400  # no storyboard yet
        assert client.get("/media/zzz/../../etc/passwd").status_code == 404
        assert client.get(f"/media/{pid}/project.json").status_code == 404
