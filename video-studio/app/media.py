"""ffmpeg helpers: probing, frame extraction, trimming, downloading and final composition."""

from __future__ import annotations

import asyncio
import json
import shutil
from pathlib import Path

import httpx


class MediaError(RuntimeError):
    pass


async def run(*args: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        tail = stderr.decode(errors="replace")[-1500:]
        raise MediaError(f"{args[0]} failed ({proc.returncode}): {tail}")
    return stdout.decode(errors="replace")


def require_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            raise MediaError(f"{tool} không có trong PATH — cài ffmpeg trước (xem README).")


async def probe(path: Path) -> dict:
    out = await run("ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path))
    return json.loads(out)


async def duration_of(path: Path) -> float:
    info = await probe(path)
    return float(info["format"]["duration"])


async def has_audio(path: Path) -> bool:
    info = await probe(path)
    return any(s.get("codec_type") == "audio" for s in info.get("streams", []))


async def extract_frames(video: Path, out_dir: Path, max_frames: int = 16) -> list[tuple[float, Path]]:
    """Evenly sample up to max_frames JPEG frames; returns (timestamp, path) pairs."""
    out_dir.mkdir(parents=True, exist_ok=True)
    duration = await duration_of(video)
    count = max(1, min(max_frames, int(duration * 2)))
    step = duration / count
    frames = []
    for i in range(count):
        ts = round(step * i + step / 2, 2)
        path = out_dir / f"frame_{i:02d}.jpg"
        await run(
            "ffmpeg", "-y", "-v", "error", "-ss", str(ts), "-i", str(video),
            "-frames:v", "1", "-vf", "scale=512:-2", "-q:v", "4", str(path),
        )
        frames.append((ts, path))
    return frames


async def extract_audio(video: Path, out_path: Path) -> Path | None:
    if not await has_audio(video):
        return None
    await run("ffmpeg", "-y", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", str(out_path))
    return out_path


async def trim(video: Path, start: float, end: float, out_path: Path) -> Path:
    """Cut a slice for use as a motion reference (≤720p, no audio, H.264)."""
    await run(
        "ffmpeg", "-y", "-v", "error", "-ss", f"{start:.2f}", "-i", str(video), "-t", f"{end - start:.2f}",
        "-vf", "scale='if(gt(iw,ih),-2,min(720,iw))':'if(gt(iw,ih),min(720,ih),-2)'",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", str(out_path),
    )
    return out_path


async def download(url: str, out_path: Path) -> Path:
    async with httpx.AsyncClient(timeout=300, follow_redirects=True) as client:
        async with client.stream("GET", url) as resp:
            resp.raise_for_status()
            with out_path.open("wb") as fh:
                async for chunk in resp.aiter_bytes():
                    fh.write(chunk)
    return out_path


async def download_social_video(url: str, out_dir: Path) -> Path:
    """Download a TikTok/Instagram/YouTube video with yt-dlp (falls back to a plain HTTP download)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "reference.mp4"
    if url.lower().split("?")[0].endswith((".mp4", ".mov", ".webm")):
        return await download(url, target)
    if shutil.which("yt-dlp") is None:
        raise MediaError("Cần yt-dlp để tải video từ link mạng xã hội (pip install yt-dlp), hoặc upload file video.")
    await run(
        "yt-dlp", "-f", "mp4/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best", "--merge-output-format", "mp4",
        "-o", str(target), "--no-playlist", url,
    )
    if not target.exists():
        raise MediaError("yt-dlp không tải được video.")
    return target


async def make_test_clip(out_path: Path, duration: int, width: int, height: int, label: str) -> Path:
    """Colour-bar clip with a tone — used in DEMO_MODE instead of a paid generation."""
    await run(
        "ffmpeg", "-y", "-v", "error",
        "-f", "lavfi", "-i", f"testsrc2=size={width}x{height}:rate=24:duration={duration}",
        "-f", "lavfi", "-i", f"sine=frequency=330:duration={duration}",
        "-vf", f"drawtext=text='{label}':fontsize={width // 14}:fontcolor=white:box=1:boxcolor=black@0.6:x=(w-tw)/2:y=h*0.15",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out_path),
    )
    return out_path


async def make_silent_voice(out_path: Path, duration: float) -> Path:
    await run("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"sine=frequency=660:duration={duration:.2f}",
              "-af", "volume=0.2", str(out_path))
    return out_path


def _srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(cues: list[tuple[float, float, str]]) -> str:
    """cues: (start, end, text). Long lines are split into ≤2 short chunks for vertical video."""
    blocks = []
    n = 0
    for start, end, text in cues:
        text = " ".join(text.split())
        if not text or end <= start:
            continue
        words = text.split()
        chunks = [" ".join(words[i:i + 6]) for i in range(0, len(words), 6)]
        span = (end - start) / len(chunks)
        for i, chunk in enumerate(chunks):
            n += 1
            blocks.append(f"{n}\n{_srt_time(start + i * span)} --> {_srt_time(start + (i + 1) * span)}\n{chunk}\n")
    return "\n".join(blocks)


async def normalize_clip(src: Path, out_path: Path, width: int, height: int) -> Path:
    """Scale/pad to the target frame, 30fps, with an audio track (silent if the clip has none)."""
    vf = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,fps=30,format=yuv420p,setsar=1"
    )
    if await has_audio(src):
        args = ["-i", str(src), "-vf", vf, "-map", "0:v:0", "-map", "0:a:0"]
    else:
        args = ["-i", str(src), "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-vf", vf, "-map", "0:v:0", "-map", "1:a:0", "-shortest"]
    await run(
        "ffmpeg", "-y", "-v", "error", *args,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-ar", "44100", "-ac", "2", str(out_path),
    )
    return out_path


async def compose(
    clips: list[Path],
    out_path: Path,
    work_dir: Path,
    width: int,
    height: int,
    voiceover: Path | None = None,
    music: Path | None = None,
    srt_text: str | None = None,
    native_audio_volume: float = 0.25,
) -> Path:
    """Normalize + concatenate clips, mix voiceover/music over the clips' own audio, burn subtitles."""
    work_dir.mkdir(parents=True, exist_ok=True)
    normalized = []
    for i, clip in enumerate(clips):
        normalized.append(await normalize_clip(clip, work_dir / f"norm_{i:02d}.mp4", width, height))

    concat_list = work_dir / "concat.txt"
    concat_list.write_text("".join(f"file '{p.resolve()}'\n" for p in normalized), encoding="utf-8")
    joined = work_dir / "joined.mp4"
    await run("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(joined))

    inputs = ["-i", str(joined)]
    # With a voiceover, the clips' native audio becomes background ambience.
    base_volume = native_audio_volume if voiceover else 1.0
    filters = [f"[0:a]volume={base_volume}[a0]"]
    mix = ["[a0]"]
    next_input = 1
    if voiceover:
        inputs += ["-i", str(voiceover)]
        filters.append(f"[{next_input}:a]volume=1.0,apad[vo]")
        mix.append("[vo]")
        next_input += 1
    if music:
        inputs += ["-stream_loop", "-1", "-i", str(music)]
        filters.append(f"[{next_input}:a]volume=0.15[mu]")
        mix.append("[mu]")
    filters.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0[aout]")

    vf = "null"
    if srt_text:
        srt_path = work_dir / "subtitles.srt"
        srt_path.write_text(srt_text, encoding="utf-8")
        # libass scales these to a 288px-high canvas: ~13/288 of frame height, ~15% from the bottom.
        style = (
            "FontName=DejaVu Sans,Fontsize=13,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
            "BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=45"
        )
        vf = f"subtitles='{_ffmpeg_escape(srt_path)}':force_style='{style}'"
    filters.append(f"[0:v]{vf}[vout]")

    await run(
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", ";".join(filters), "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out_path),
    )
    return out_path


def _ffmpeg_escape(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
