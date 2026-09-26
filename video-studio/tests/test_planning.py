import pytest

from app import generator, media, pipeline
from app.analyzer import clamp_storyboard
from app.schemas import ReferenceClip, RenderSettings, Shot, Storyboard
from app.video_models import get_model


def board(durations, refs=()):
    return Storyboard(
        title="t",
        shots=[
            Shot(duration_s=d, purpose="p", prompt=f"shot {i} with the product", voiceover=f"line {i}",
                 copy_reference_motion=ReferenceClip(start_s=0, end_s=3) if i in refs else None)
            for i, d in enumerate(durations)
        ],
    )


def test_seedance_720p_price_matches_fal_rate():
    assert get_model("seedance-2.0").usd_per_second("720p") == pytest.approx(0.3024)
    assert get_model("seedance-2.0-fast").usd_per_second("720p") == pytest.approx(0.2419, abs=1e-4)


def test_video_reference_discount():
    m = get_model("seedance-2.0")
    assert m.estimate_usd(10, "720p", True) == pytest.approx(10 * 0.3024 * 0.6, abs=1e-3)


def test_12s_storyboard_is_one_call():
    groups = generator.plan_segments(board([3, 3, 3, 3]), get_model("seedance-2.0"))
    assert groups == [[0, 1, 2, 3]]


def test_long_storyboard_splits_at_max_duration():
    groups = generator.plan_segments(board([5, 5, 5, 5, 4]), get_model("seedance-2.0"))
    assert groups == [[0, 1, 2], [3, 4]]


def test_split_when_too_many_video_refs():
    groups = generator.plan_segments(board([2, 2, 2, 2], refs={0, 1, 2, 3}), get_model("seedance-2.0"))
    assert groups == [[0, 1, 2], [3]]


def test_segment_duration_respects_min():
    shots = board([1.5]).shots
    assert generator.segment_duration(shots, get_model("seedance-2.0")) == 4


def test_prompt_has_image_and_video_refs_and_cuts():
    shots = board([3, 4]).shots
    prompt = generator.build_segment_prompt(shots, 2, [1, None], "9:16")
    assert "@Image1, @Image2" in prompt
    assert "the product (@Image1)" in prompt
    assert "@Video1" in prompt
    assert "Cut scene to: [3s-7s]" in prompt


def test_estimate_cost_totals():
    est = pipeline.estimate_cost(board([3, 3, 3, 3]), RenderSettings())
    assert len(est["segments"]) == 1
    assert est["video_usd"] == pytest.approx(12 * 0.3024, abs=1e-3)
    assert est["total_usd"] > est["video_usd"]


def test_clamp_drops_out_of_range_motion_refs():
    sb = board([3, 3, 3], refs={0, 1, 2})
    sb.shots[0].copy_reference_motion = ReferenceClip(start_s=1, end_s=20)
    sb.shots[1].copy_reference_motion = ReferenceClip(start_s=9.5, end_s=12)
    clamp_storyboard(sb, reference_duration=10.0)
    assert sb.shots[0].copy_reference_motion == ReferenceClip(start_s=1, end_s=6)
    assert sb.shots[1].copy_reference_motion is None
    assert clamp_storyboard(board([3], refs={0}), None).shots[0].copy_reference_motion is None


def test_srt_splits_long_lines():
    srt = media.build_srt([(0, 4, "one two three four five six seven eight"), (4, 5, "")])
    assert srt.count("-->") == 2
    assert "00:00:02,000 --> 00:00:04,000" in srt
