#!/usr/bin/env python3
"""Dựng video từ một file timeline (EDL) dạng JSON bằng ffmpeg.

Dùng:
  python render_edl.py edit.json                 # xuất bản chính thức
  python render_edl.py edit.json --preview       # bản nháp nửa độ phân giải, rất nhanh
  python render_edl.py edit.json --format 16:9 --out out/ngang.mp4   # đổi khung hình

Cấu trúc EDL: xem assets/edl-example.json và references/edl-schema.md.
Đường dẫn tương đối trong EDL được tính từ thư mục chứa file EDL.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

FORMATS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def run(cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-25:])
        sys.exit(f"ffmpeg lỗi:\n  {' '.join(cmd)}\n---\n{tail}")
    return proc


def has_audio(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                          "stream=index", "-of", "csv=p=0", path], capture_output=True, text=True)
    return bool(out.stdout.strip())


def duration_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    return float(out.stdout.strip() or 0)


def measure_lufs(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-vn", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else None


def atempo_chain(speed):
    # atempo chỉ nhận 0.5–2.0 mỗi lần, nên nối nhiều bộ lọc cho tốc độ ngoài khoảng đó.
    parts, s = [], speed
    while s > 2.0:
        parts.append("atempo=2.0")
        s /= 2.0
    while s < 0.5:
        parts.append("atempo=0.5")
        s /= 0.5
    parts.append(f"atempo={s:.4f}")
    return ",".join(parts)


def fit_filter(mode, W, H, zoom):
    """Đưa mọi nguồn về đúng khung W×H. fill = phóng + cắt, fit = viền đen, blur = nền mờ."""
    if mode == "fit":
        return (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
                f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black")
    if mode == "blur":
        return (f"split=2[bg][fg];[bg]scale={W}:{H}:force_original_aspect_ratio=increase,"
                f"crop={W}:{H},boxblur=30:3,eq=brightness=-0.08[bgb];"
                f"[fg]scale={W}:{H}:force_original_aspect_ratio=decrease[fgs];"
                f"[bgb][fgs]overlay=(W-w)/2:(H-h)/2")
    zw, zh = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
    return f"scale={zw}:{zh}:force_original_aspect_ratio=increase,crop={W}:{H}"


def render_segment(i, clip, base_dir, work, W, H, fps, enc):
    src = os.path.join(base_dir, clip["src"])
    if not os.path.exists(src):
        sys.exit(f"Không tìm thấy file clip #{i}: {src}")
    is_image = src.lower().endswith(IMAGE_EXT)
    speed = float(clip.get("speed", 1.0))
    mode = clip.get("fit", "fill")
    zoom = float(clip.get("zoom", 1.0))
    out = os.path.join(work, f"seg_{i:03d}.mp4")

    if is_image:
        dur = float(clip.get("duration", 3))
        inputs = ["-loop", "1", "-framerate", str(fps), "-t", f"{dur}", "-i", src]
        kb = clip.get("kenburns")
        if kb:
            frames = int(dur * fps)
            z = f"min(1+0.12*on/{frames},1.12)" if kb != "out" else f"max(1.12-0.12*on/{frames},1)"
            vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
                  f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={fps}")
        else:
            vf = fit_filter(mode, W, H, zoom)
        out_dur = dur
        audio_ok = False
    else:
        start = float(clip.get("in", 0))
        end = clip.get("out")
        src_dur = (float(end) if end is not None else duration_of(src)) - start
        inputs = ["-ss", f"{start}", "-t", f"{src_dur}", "-i", src]
        vf = fit_filter(mode, W, H, zoom)
        if speed != 1.0:
            vf += f",setpts=PTS/{speed}"
        out_dur = src_dur / speed
        audio_ok = has_audio(src) and not clip.get("mute", False)

    vf = f"[0:v]{vf},fps={fps},setsar=1,format=yuv420p[v]"
    if audio_ok:
        af = "[0:a]aresample=48000,aformat=channel_layouts=stereo"
        if speed != 1.0:
            af += "," + atempo_chain(speed)
        af += f",volume={clip.get('volume', 1.0)},apad,atrim=0:{out_dur:.3f}[a]"
        audio_inputs = []
    else:
        af = f"[1:a]atrim=0:{out_dur:.3f}[a]"
        audio_inputs = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]

    cmd = ["ffmpeg", "-y", "-hide_banner", *inputs, *audio_inputs,
           "-filter_complex", f"{vf};{af}", "-map", "[v]", "-map", "[a]",
           "-t", f"{out_dur:.3f}", *enc, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out]
    run(cmd)
    return out, out_dur


def esc_path(p):
    return p.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def text_filters(texts, work, W, H, font):
    s = W / 1080
    pos_y = {"top": "h*0.14", "center": "(h-text_h)/2", "bottom": "h*0.70"}
    filters = []
    for n, t in enumerate(texts):
        tf = os.path.join(work, f"text_{n}.txt")
        with open(tf, "w", encoding="utf-8") as fh:
            fh.write(t["text"])
        size = int(t.get("size", 72) * s)
        y = pos_y.get(t.get("position", "top"), t.get("position"))
        f = (f"drawtext=fontfile='{esc_path(t.get('font', font))}':textfile='{esc_path(tf)}':"
             f"fontsize={size}:fontcolor={t.get('color', 'white')}:x=(w-text_w)/2:y={y}:"
             f"line_spacing={int(size * 0.25)}:text_align=center:"
             f"enable='between(t,{t['start']},{t['end']})'")
        if t.get("box", True):
            f += f":box=1:boxcolor={t.get('boxcolor', 'black@0.6')}:boxborderw={int(22 * s)}"
        else:
            f += f":borderw={max(2, int(5 * s))}:bordercolor=black"
        filters.append(f)
    return filters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edl")
    ap.add_argument("--preview", action="store_true", help="nửa độ phân giải, mã hóa nhanh")
    ap.add_argument("--format", choices=list(FORMATS))
    ap.add_argument("--out")
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    with open(args.edl, encoding="utf-8") as fh:
        edl = json.load(fh)
    base_dir = os.path.dirname(os.path.abspath(args.edl))
    fmt = args.format or edl.get("format", "9:16")
    W, H = FORMATS[fmt]
    if args.preview:
        W, H = W // 2 // 2 * 2, H // 2 // 2 * 2
    fps = int(edl.get("fps", 30))
    enc = (["-c:v", "libx264", "-preset", "ultrafast", "-crf", "28"] if args.preview
           else ["-c:v", "libx264", "-preset", "medium", "-crf", "18"])
    font = edl.get("font") or next((f for f in FONT_CANDIDATES if os.path.exists(f)), None)

    out_path = args.out or edl.get("output", "out/video.mp4")
    if args.preview:
        root, ext = os.path.splitext(out_path)
        out_path = f"{root}_preview{ext}"
    out_path = os.path.join(base_dir, out_path) if not os.path.isabs(out_path) else out_path
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    work = tempfile.mkdtemp(prefix="edl_")
    try:
        # 1) Chuẩn hóa từng clip về cùng khung, fps, âm thanh → nối không lệch tiếng.
        segs = []
        for i, clip in enumerate(edl["clips"]):
            seg, d = render_segment(i, clip, base_dir, work, W, H, fps, enc)
            segs.append(seg)
            print(f"  clip {i + 1}/{len(edl['clips'])}: {clip['src']} → {d:.2f}s")
        listfile = os.path.join(work, "list.txt")
        with open(listfile, "w") as fh:
            fh.writelines(f"file '{s}'\n" for s in segs)
        base = os.path.join(work, "base.mp4")
        run(["ffmpeg", "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", base])
        T = duration_of(base)

        # 2) Lớp chữ, phụ đề, logo + trộn voice/nhạc/chuẩn hóa âm lượng.
        inputs = ["-i", base]
        idx = 1
        vchain = ["[0:v]null"]
        if edl.get("captions"):
            cap = os.path.join(base_dir, edl["captions"])
            ext = os.path.splitext(cap)[1].lower()
            local = os.path.join(work, "captions" + ext)
            shutil.copy(cap, local)
            if ext == ".ass":
                vchain.append("ass=captions.ass")
            else:
                vchain.append("subtitles=captions.srt:force_style='FontName=DejaVu Sans,Bold=1,"
                              "FontSize=14,Outline=2,MarginV=60'")
        if edl.get("texts"):
            if not font:
                sys.exit("Không tìm thấy font cho chữ overlay — đặt \"font\": \"/đường/dẫn/font.ttf\" trong EDL.")
            vchain += text_filters(edl["texts"], work, W, H, font)
        fc = [",".join(vchain) + "[vt]"]
        vlast = "[vt]"
        if edl.get("watermark"):
            wm = edl["watermark"]
            inputs += ["-i", os.path.join(base_dir, wm["src"])]
            ww = int(W * float(wm.get("scale", 0.15)))
            m = int(W * 0.04)
            pos = {"top-right": f"W-w-{m}:{m}", "top-left": f"{m}:{m}",
                   "bottom-right": f"W-w-{m}:H-h-{m}", "bottom-left": f"{m}:H-h-{m}"}
            fc.append(f"[{idx}:v]scale={ww}:-1,format=rgba,colorchannelmixer=aa={wm.get('opacity', 0.85)}[wm];"
                      f"{vlast}[wm]overlay={pos.get(wm.get('position', 'top-right'))}[vw]")
            vlast, idx = "[vw]", idx + 1

        stereo = "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
        mix = [f"[0:a]{stereo},volume={edl.get('clip_audio_volume', 1.0)}[base]"]
        mix_inputs = ["[base]"]
        key = None
        if edl.get("voiceover"):
            vo = edl["voiceover"]
            vo = vo if isinstance(vo, dict) else {"src": vo}
            inputs += ["-i", os.path.join(base_dir, vo["src"])]
            delay = int(float(vo.get("start", 0)) * 1000)
            mix.append(f"[{idx}:a]{stereo},adelay={delay}|{delay},volume={vo.get('volume', 1.0)},asplit=2[vo][vokey]")
            mix_inputs.append("[vo]")
            key, idx = "[vokey]", idx + 1
        if edl.get("music"):
            mu = edl["music"]
            mu = mu if isinstance(mu, dict) else {"src": mu}
            inputs += ["-stream_loop", "-1", "-i", os.path.join(base_dir, mu["src"])]
            fade = min(1.5, T / 4)
            mix.append(f"[{idx}:a]{stereo},atrim=0:{T:.3f},volume={mu.get('volume', 0.15)},"
                       f"afade=t=out:st={T - fade:.3f}:d={fade:.3f}[mraw]")
            if mu.get("duck", True):
                if key is None:
                    mix[0] = mix[0].replace("[base]", ",asplit=2[base][basekey]")
                    key = "[basekey]"
                mix.append(f"[mraw]{key}sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[mu]")
            else:
                mix.append("[mraw]anull[mu]")
                if key:
                    mix.append(f"{key}anullsink")
            mix_inputs.append("[mu]")
            idx += 1
        elif key:
            mix.append(f"{key}anullsink")
        lufs = edl.get("loudness", -14)
        mix.append(f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=first:normalize=0,"
                   f"loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample=48000[aout]")
        fc += mix

        cmd = ["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(fc),
               "-map", vlast, "-map", "[aout]", "-t", f"{T:.3f}", *enc, "-r", str(fps),
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out_path]
        run(cmd, cwd=work)

        # loudnorm 1 lượt hay hụt với clip ngắn → đo lại và bù gain cho sát mục tiêu (±0.5 LU).
        measured = measure_lufs(out_path)
        if measured is not None and abs(measured - lufs) > 0.5:
            tmp = os.path.join(work, "gain.mp4")
            run(["ffmpeg", "-y", "-hide_banner", "-i", out_path, "-c:v", "copy",
                 "-af", f"volume={lufs - measured:.2f}dB,alimiter=limit=0.84:level=false",
                 "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
            shutil.move(tmp, out_path)
            measured = measure_lufs(out_path)
        print(f"  âm lượng: {measured} LUFS (mục tiêu {lufs})")
        print(f"✓ Xuất xong: {out_path} ({T:.1f}s, {W}x{H}, {fps}fps)")
    finally:
        if args.keep_temp:
            print(f"  file tạm: {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
