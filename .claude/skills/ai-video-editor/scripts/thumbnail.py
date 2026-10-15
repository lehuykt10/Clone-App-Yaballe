#!/usr/bin/env python3
"""Chọn khung hình làm thumbnail và ghép chữ tiêu đề.

Dùng:
  python thumbnail.py sheet video.mp4 --out frames/            # 12 khung ứng viên + 1 ảnh tổng (contact sheet)
  python thumbnail.py make frames/f_07.jpg --text "SAI LẦM\\nAI CŨNG MẮC" --out thumb.jpg
  python thumbnail.py make anh.jpg --text "3 MẸO" --size 9:16 --out cover.jpg   # ảnh bìa Shorts/Reels

Chữ trên thumbnail nên ≤ 4–5 từ, không lặp lại tiêu đề video (xem references/youtube-value.md).
"""
import argparse
import os
import subprocess
import sys

SIZES = {"16:9": (1280, 720), "9:16": (1080, 1920), "1:1": (1080, 1080)}
FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("ffmpeg lỗi:\n" + "\n".join(p.stderr.splitlines()[-15:]))


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


def esc(p):
    return p.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def sheet(args):
    os.makedirs(args.out, exist_ok=True)
    d = duration(args.video)
    n = args.count
    for i in range(n):
        # Bỏ 5% đầu/cuối (thường là màn đen / chuyển cảnh).
        t = d * (0.05 + 0.9 * i / max(1, n - 1))
        run(["ffmpeg", "-y", "-hide_banner", "-ss", f"{t:.2f}", "-i", args.video, "-frames:v", "1",
             "-q:v", "2", os.path.join(args.out, f"f_{i + 1:02d}.jpg")])
    cols = 4
    rows = (n + cols - 1) // cols
    run(["ffmpeg", "-y", "-hide_banner", "-i", os.path.join(args.out, "f_%02d.jpg"),
         "-vf", f"scale=480:-2,drawtext=fontfile='{esc(args.font)}':text='%{{frame_num}}':start_number=1:"
                f"x=10:y=10:fontsize=36:fontcolor=yellow:box=1:boxcolor=black@0.6,tile={cols}x{rows}",
         "-frames:v", "1", os.path.join(args.out, "contact_sheet.jpg")])
    print(f"✓ {n} khung ứng viên + contact_sheet.jpg trong {args.out} (số trên ảnh = f_NN.jpg)")


def make(args):
    W, H = SIZES[args.size]
    textfile = args.out + ".txt"
    with open(textfile, "w", encoding="utf-8") as fh:
        fh.write(args.text.replace("\\n", "\n"))
    fs = args.fontsize or int(H * (0.13 if args.size == "16:9" else 0.07))
    x = {"left": "w*0.05", "center": "(w-text_w)/2", "right": "w*0.95-text_w"}[args.align]
    y = {"top": "h*0.08", "center": "(h-text_h)/2", "bottom": "h*0.92-text_h"}[args.valign]
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"eq=contrast=1.12:saturation=1.25:brightness=0.02,unsharp=5:5:0.8,"
          f"drawtext=fontfile='{esc(args.font)}':textfile='{esc(textfile)}':fontsize={fs}:"
          f"fontcolor={args.color}:borderw={max(4, fs // 12)}:bordercolor=black:"
          f"shadowx=4:shadowy=4:shadowcolor=black@0.7:line_spacing={fs // 6}:x={x}:y={y}")
    run(["ffmpeg", "-y", "-hide_banner", "-i", args.image, "-vf", vf, "-frames:v", "1", "-q:v", "2", args.out])
    os.remove(textfile)
    print(f"✓ Thumbnail {W}x{H} → {args.out}")


def main():
    font = next((f for f in FONTS if os.path.exists(f)), "")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheet")
    s.add_argument("video")
    s.add_argument("--out", default="frames")
    s.add_argument("--count", type=int, default=12)
    s.add_argument("--font", default=font)
    m = sub.add_parser("make")
    m.add_argument("image")
    m.add_argument("--text", required=True)
    m.add_argument("--out", required=True)
    m.add_argument("--size", choices=list(SIZES), default="16:9")
    m.add_argument("--color", default="yellow")
    m.add_argument("--fontsize", type=int)
    m.add_argument("--align", choices=["left", "center", "right"], default="left")
    m.add_argument("--valign", choices=["top", "center", "bottom"], default="center")
    m.add_argument("--font", default=font)
    args = ap.parse_args()
    if not args.font:
        sys.exit("Không tìm thấy font — truyền --font /đường/dẫn/font.ttf")
    (sheet if args.cmd == "sheet" else make)(args)


if __name__ == "__main__":
    main()
