#!/usr/bin/env python3
"""Tóm tắt nhanh file media để lập kế hoạch dựng.

Dùng:
  python probe.py clip1.mp4 clip2.mov music.mp3          # bảng tóm tắt
  python probe.py raw.mp4 --scenes 0.3                   # thêm mốc đổi cảnh (tìm điểm cắt)
  python probe.py vo.wav --loudness                      # đo độ to LUFS
  python probe.py *.mp4 --json                           # xuất JSON cho script khác
"""
import argparse
import json
import re
import subprocess
import sys


def ffprobe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"ffprobe lỗi với {path}: {out.stderr.strip()}")
    return json.loads(out.stdout)


def fps_of(stream):
    num, _, den = (stream.get("avg_frame_rate") or "0/1").partition("/")
    try:
        return round(float(num) / float(den or 1), 2)
    except ZeroDivisionError:
        return 0.0


def rotation_of(stream):
    for sd in stream.get("side_data_list", []) or []:
        if "rotation" in sd:
            return int(sd["rotation"])
    return int((stream.get("tags") or {}).get("rotate", 0))


def summarize(path):
    info = ffprobe(path)
    fmt = info.get("format", {})
    v = next((s for s in info["streams"] if s["codec_type"] == "video"
              and not (s.get("disposition") or {}).get("attached_pic")), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    res = {"file": path, "duration": round(float(fmt.get("duration", 0) or 0), 2)}
    if v:
        w, h = v.get("width", 0), v.get("height", 0)
        rot = rotation_of(v)
        if abs(rot) in (90, 270):
            w, h = h, w
        res.update(width=w, height=h, fps=fps_of(v), vcodec=v.get("codec_name"),
                   orientation="dọc" if h > w else ("vuông" if h == w else "ngang"))
        if fmt.get("format_name", "").startswith(("png", "jpeg", "image2", "webp")) or v.get("codec_name") in ("png", "mjpeg", "webp"):
            res["kind"] = "image"
        else:
            res["kind"] = "video"
    else:
        res["kind"] = "audio"
    res["has_audio"] = a is not None
    if a:
        res["acodec"] = a.get("codec_name")
    return res


def scenes(path, threshold):
    cmd = ["ffmpeg", "-hide_banner", "-i", path, "-vf",
           f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    return [round(float(t), 2) for t in re.findall(r"pts_time:([\d.]+)", err)]


def loudness(path):
    cmd = ["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-vn", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--scenes", type=float, metavar="NGƯỠNG", help="phát hiện đổi cảnh, vd 0.3")
    ap.add_argument("--loudness", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = []
    for f in args.files:
        try:
            r = summarize(f)
        except Exception as e:  # noqa: BLE001 — báo lỗi từng file, chạy tiếp file khác
            rows.append({"file": f, "error": str(e)})
            continue
        if args.scenes is not None and r["kind"] == "video":
            r["scene_cuts"] = scenes(f, args.scenes)
        if args.loudness and r["has_audio"]:
            r["lufs"] = loudness(f)
        rows.append(r)

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    for r in rows:
        if "error" in r:
            print(f"✗ {r['file']}: {r['error']}")
            continue
        line = f"• {r['file']} [{r['kind']}] {r['duration']}s"
        if "width" in r:
            line += f" {r['width']}x{r['height']} ({r['orientation']}) {r['fps']}fps"
        line += " có tiếng" if r["has_audio"] else " không tiếng"
        if "lufs" in r:
            line += f" | {r['lufs']} LUFS"
        print(line)
        if r.get("scene_cuts"):
            print(f"    đổi cảnh tại: {', '.join(map(str, r['scene_cuts']))}")


if __name__ == "__main__":
    sys.exit(main())
