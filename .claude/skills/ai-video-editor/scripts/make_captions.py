#!/usr/bin/env python3
"""Tạo phụ đề kiểu Shorts/Reels (ASS) từ SRT, hoặc tự nghe ra chữ từ audio/video.

Dùng:
  python make_captions.py --srt script.srt --out captions.ass --style shorts
  python make_captions.py --audio vo.mp3 --lang vi --out captions.ass     # cần: pip install faster-whisper
  python make_captions.py --srt sub.srt --out captions.ass --style youtube --size 16:9

Kiểu:
  shorts  — chữ to, đậm, 1–3 từ/cụm, tô màu từ đang đọc, đặt ở 2/3 màn hình (tránh vùng nút bấm)
  youtube — 1 dòng gọn dưới đáy, dành cho video dài 16:9
"""
import argparse
import re
import subprocess
import sys

STYLES = {
    # tên: (cỡ chữ ở chiều rộng 1080, viền, MarginV theo % chiều cao, số từ mỗi cụm, căn lề ASS)
    "shorts": dict(size=78, outline=6, margin=0.30, words=3, align=2),
    "youtube": dict(size=48, outline=3, margin=0.06, words=8, align=2),
}
SIZES = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}


def ts_to_s(ts):
    h, m, rest = ts.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def s_to_ass(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def s_to_srt(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def parse_srt(path):
    blocks = re.split(r"\n\s*\n", open(path, encoding="utf-8-sig").read().strip())
    words = []
    for b in blocks:
        lines = [l for l in b.strip().splitlines() if l.strip()]
        tl = next((l for l in lines if "-->" in l), None)
        if not tl:
            continue
        a, b2 = [ts_to_s(x.strip().split()[0]) for x in tl.split("-->")]
        text = " ".join(lines[lines.index(tl) + 1:])
        toks = re.sub(r"<[^>]+>", "", text).split()
        if not toks:
            continue
        # SRT không có mốc từng từ → chia đều theo độ dài chữ (đủ khớp cho mắt người xem).
        total = sum(len(t) + 1 for t in toks)
        t = a
        for tok in toks:
            d = (b2 - a) * (len(tok) + 1) / total
            words.append((t, t + d, tok))
            t += d
    return words


def transcribe(path, lang, model_size):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Chưa cài faster-whisper. Chạy: pip install faster-whisper  (hoặc đưa file .srt có sẵn qua --srt)")
    model = WhisperModel(model_size, compute_type="int8")
    segs, _ = model.transcribe(path, language=lang, word_timestamps=True, vad_filter=True)
    return [(w.start, w.end, w.word.strip()) for s in segs for w in s.words if w.word.strip()]


def chunk(words, n, max_gap=0.6):
    out, cur = [], []
    for w in words:
        if cur and (len(cur) >= n or w[0] - cur[-1][1] > max_gap or cur[-1][2][-1:] in ".?!,:;"):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


def write_srt(words, path, n):
    with open(path, "w", encoding="utf-8") as fh:
        for i, c in enumerate(chunk(words, n), 1):
            fh.write(f"{i}\n{s_to_srt(c[0][0])} --> {s_to_srt(c[-1][1])}\n{' '.join(w[2] for w in c)}\n\n")


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--srt")
    src.add_argument("--audio", help="file audio/video để tự nhận dạng giọng nói")
    ap.add_argument("--out", required=True)
    ap.add_argument("--style", choices=list(STYLES), default="shorts")
    ap.add_argument("--size", choices=list(SIZES), help="mặc định 9:16 cho shorts, 16:9 cho youtube")
    ap.add_argument("--lang", default="vi")
    ap.add_argument("--model", default="small", help="model whisper: tiny/base/small/medium/large-v3")
    ap.add_argument("--highlight", default="&H0000E5FF", help="màu từ đang đọc (ASS &HBBGGRR), mặc định vàng")
    ap.add_argument("--no-highlight", action="store_true")
    ap.add_argument("--upper", action="store_true", help="viết HOA toàn bộ")
    ap.add_argument("--font", default="DejaVu Sans")
    ap.add_argument("--words", type=int, help="số từ tối đa mỗi cụm")
    args = ap.parse_args()

    st = STYLES[args.style]
    W, H = SIZES[args.size or ("9:16" if args.style == "shorts" else "16:9")]
    words = parse_srt(args.srt) if args.srt else transcribe(args.audio, args.lang, args.model)
    if not words:
        sys.exit("Không có chữ nào để làm phụ đề.")
    if args.upper:
        words = [(a, b, t.upper()) for a, b, t in words]
    n = args.words or st["words"]
    if args.audio:
        write_srt(words, args.out.rsplit(".", 1)[0] + ".srt", n)  # giữ bản SRT để sửa chính tả / tải lên YouTube

    size = int(st["size"] * W / 1080)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{args.font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,{st['outline']},2,{st['align']},{int(W * 0.08)},{int(W * 0.08)},{int(H * st['margin'])},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for c in chunk(words, n):
        if args.no_highlight or args.style == "youtube":
            lines.append(f"Dialogue: 0,{s_to_ass(c[0][0])},{s_to_ass(c[-1][1])},Cap,,0,0,0,,{' '.join(w[2] for w in c)}")
            continue
        # Mỗi từ một sự kiện: cả cụm hiện, riêng từ đang đọc đổi màu + phóng nhẹ.
        for j, (a, b, _) in enumerate(c):
            end = c[j + 1][0] if j + 1 < len(c) else b
            txt = " ".join(
                f"{{\\c{args.highlight}\\fscx108\\fscy108}}{w[2]}{{\\r}}" if k == j else w[2]
                for k, w in enumerate(c))
            lines.append(f"Dialogue: 0,{s_to_ass(a)},{s_to_ass(end)},Cap,,0,0,0,,{txt}")
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(header + "\n".join(lines) + "\n")
    print(f"✓ {len(lines)} dòng phụ đề → {args.out}")


if __name__ == "__main__":
    main()
