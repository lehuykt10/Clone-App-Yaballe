# Cấu trúc file timeline (EDL) cho `scripts/render_edl.py`

File JSON mô tả toàn bộ bản dựng. Đường dẫn tương đối tính từ thư mục chứa file EDL. Mẫu đầy đủ: `assets/edl-example.json`.

| Trường | Kiểu | Mặc định | Ý nghĩa |
|---|---|---|---|
| `output` | chuỗi | `out/video.mp4` | File xuất. `--preview` tự thêm hậu tố `_preview` |
| `format` | `9:16` `16:9` `1:1` `4:5` | `9:16` | Khung hình, ra 1080×1920 / 1920×1080 / 1080×1080 / 1080×1350 |
| `fps` | số | 30 | Khung hình/giây đầu ra (upscale 60fps làm ở Topaz, không ở đây) |
| `clips` | mảng | — | Các cảnh theo đúng thứ tự xuất hiện, nối bằng cắt thẳng (hard cut) |
| `texts` | mảng | — | Chữ overlay (hook, CTA, nhãn) |
| `captions` | `.ass` hoặc `.srt` | — | Phụ đề đốt cứng vào hình. `.ass` từ `make_captions.py` đẹp hơn |
| `voiceover` | chuỗi hoặc `{src,start,volume}` | — | Giọng đọc; `start` = giây bắt đầu |
| `music` | chuỗi hoặc `{src,volume,duck}` | volume 0.15, duck true | Nhạc nền, tự lặp đủ độ dài, tự fade cuối; `duck` = tự hạ khi có giọng |
| `clip_audio_volume` | số | 1.0 | Âm lượng tiếng gốc của các clip (sau khi đã nhân `volume` từng clip) |
| `watermark` | `{src,position,scale,opacity}` | top-right, 0.15, 0.85 | Logo thương hiệu |
| `loudness` | số LUFS | -14 | Mục tiêu âm lượng (TikTok/Reels/YouTube đều quanh -14) |
| `font` | đường dẫn .ttf | DejaVu Sans Bold | Font cho chữ overlay; phải có dấu tiếng Việt |

## Mỗi phần tử trong `clips`

| Trường | Áp dụng | Ý nghĩa |
|---|---|---|
| `src` | tất cả | File video hoặc ảnh (.png/.jpg/.webp) |
| `in`, `out` | video | Giây bắt đầu/kết thúc lấy từ nguồn. Bỏ `out` = tới hết |
| `duration` | ảnh | Số giây hiển thị (mặc định 3) |
| `fit` | tất cả | `fill` (phóng + cắt cho kín khung, mặc định) · `fit` (viền đen) · `blur` (nền mờ — dùng khi đưa clip ngang vào khung dọc mà không muốn mất chi tiết) |
| `zoom` | fill | >1 để "punch-in", vd 1.08–1.15. Dùng xen kẽ ở cảnh nói liền để che vết cắt (jump cut) |
| `speed` | video | 1.25–1.5 làm nhịp gọn hơn; tiếng tự đổi tốc độ không bị méo giọng |
| `mute` | video | Tắt tiếng gốc (clip NCC có nhạc bản quyền / tiếng ồn) |
| `volume` | video | Âm lượng riêng của clip |
| `kenburns` | ảnh | `in` / `out`: zoom chậm cho ảnh tĩnh đỡ "chết" |

## Mỗi phần tử trong `texts`

| Trường | Mặc định | Ý nghĩa |
|---|---|---|
| `text` | — | Dùng `\n` để xuống dòng. Giữ ≤ 2 dòng, ≤ 7 từ |
| `start`, `end` | — | Giây hiển thị |
| `position` | `top` | `top` (14% chiều cao), `center`, `bottom` (70%), hoặc biểu thức ffmpeg cho y |
| `size` | 72 | Cỡ chữ tính trên khung rộng 1080 (tự co theo khung thật) |
| `box` | true | Nền hộp đen mờ phía sau chữ. `false` = chữ viền đen |
| `color`, `boxcolor` | white, black@0.6 | Màu chữ / hộp |

## Lưu ý kỹ thuật
- Mọi clip được chuẩn hóa về cùng khung/fps/âm thanh trước khi nối → không lệch tiếng khi trộn nguồn khác nhau (AI 24fps, điện thoại 30fps, NCC 25fps…).
- Không có hiệu ứng chuyển cảnh (transition). Với video bán hàng organic, cắt thẳng giữ nhịp tốt hơn; chuyển cảnh "whip" nên nằm sẵn trong chuyển động của clip.
- Thời lượng video = tổng thời lượng các clip. Voice dài hơn sẽ bị cắt → chỉnh clip theo voice, không ngược lại.
- Chữ trong `texts` chỉ chạy trên ffmpeg ≥ 6.1 (cần `text_align`). Bản cũ hơn: xóa tham số `text_align` trong script.
