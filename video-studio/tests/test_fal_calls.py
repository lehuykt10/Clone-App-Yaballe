"""Check the arguments sent to fal without making paid calls."""

import fal_client
import pytest

from app import generator
from app.schemas import Segment
from app.video_models import get_model


class FakeHandle:
    request_id = "req-123"

    async def get(self):
        return {"video": {"url": "https://fal.media/out.mp4"}}


@pytest.fixture
def captured(monkeypatch):
    calls = {}

    async def fake_submit(endpoint, arguments):
        calls["endpoint"] = endpoint
        calls["arguments"] = arguments
        return FakeHandle()

    monkeypatch.setenv("FAL_KEY", "test")
    monkeypatch.setattr(fal_client, "submit_async", fake_submit)
    return calls


async def test_generate_segment_arguments(captured):
    seg = Segment(index=0, shot_indexes=[0, 1], duration=12, prompt="p",
                  image_urls=[f"https://img/{i}" for i in range(12)], video_urls=["https://v/1"])
    result = await generator.generate_segment(seg, get_model("seedance-2.0"), "720p", "9:16")
    assert result["video"]["url"].endswith("out.mp4")
    assert seg.request_id == "req-123"
    assert captured["endpoint"] == "bytedance/seedance-2.0/reference-to-video"
    args = captured["arguments"]
    assert args["duration"] == "12" and args["resolution"] == "720p" and args["aspect_ratio"] == "9:16"
    assert len(args["image_urls"]) == 9
    assert args["video_urls"] == ["https://v/1"]


async def test_no_video_urls_key_without_refs(captured):
    seg = Segment(index=0, shot_indexes=[0], duration=5, prompt="p", image_urls=["https://img/0"])
    await generator.generate_segment(seg, get_model("seedance-2.0-fast"), "480p", "9:16")
    assert "video_urls" not in captured["arguments"]
    assert captured["endpoint"] == "bytedance/seedance-2.0/fast/reference-to-video"
