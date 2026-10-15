# ffmpeg — công thức hay dùng (ngoài render_edl.py)

Chạy trực tiếp khi cần xử lý nguyên liệu trước khi đưa vào EDL.

## Kiểm tra / QA
```bash
# Ảnh tổng các khung tại mốc cụ thể (soi lỗi AI, xem bố cục chữ)
ffmpeg -v error -i out.mp4 -vf "select='eq(n,0)+eq(n,45)+eq(n,150)',scale=360:-2,tile=3x1" -frames:v 1 qa.png
# 1 khung tại giây 2.5
ffmpeg -v error -ss 2.5 -i out.mp4 -frames:v 1 f.png
```
Đọc ảnh `qa.png` bằng công cụ Read để tự xem — đừng giao video khi chưa nhìn ít nhất khung đầu, khung giữa và khung cuối.

## Voice
```bash
# Tìm khoảng lặng (> 0.4s, dưới -35dB) để cắt câu vấp / chỗ ngắt dài
ffmpeg -i vo.wav -af silencedetect=noise=-35dB:d=0.4 -f null - 2>&1 | grep silence_
# Tự bỏ khoảng lặng dài, giữ lại 0.15s cho tự nhiên
ffmpeg -i vo.wav -af "silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-35dB:stop_silence=0.15" vo_tight.wav
# Giảm ồn nền + lọc tiếng ù cho voice thu bằng điện thoại
ffmpeg -i vo.wav -af "highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3" vo_clean.wav
# Tăng tốc voice 1.1x không méo giọng
ffmpeg -i vo.wav -af atempo=1.1 vo_fast.wav
# Tách tiếng từ video
ffmpeg -i talk.mp4 -vn -ac 1 -ar 48000 talk.wav
```

## Nguyên liệu hình
```bash
# Cắt đúng đoạn (re-encode để chính xác từng khung)
ffmpeg -ss 3.2 -to 7.8 -i ncc.mp4 -c:v libx264 -crf 18 -c:a aac cut.mp4
# Crop bỏ dải phụ đề cứng ở đáy video NCC (giữ 82% phía trên)
ffmpeg -i ncc.mp4 -vf "crop=iw:ih*0.82:0:0" -c:a copy ncc_nosub.mp4
# Crop khung dọc 9:16 ở giữa video ngang (làm video tham chiếu chuyển động)
ffmpeg -i wide.mp4 -vf "crop=ih*9/16:ih" -an ref_9x16.mp4
# Ổn định hình quay tay (2 bước)
ffmpeg -i shaky.mp4 -vf vidstabdetect -f null - && ffmpeg -i shaky.mp4 -vf vidstabtransform=smoothing=20,unsharp=5:5:0.8 stable.mp4
```
(`vidstab` chỉ có nếu ffmpeg được build kèm — kiểm tra `ffmpeg -filters | grep vidstab`.)

## Xuất phụ
```bash
# GIF/WebP ngắn cho đầu trang sản phẩm Shopify (lấy từ cảnh viral)
ffmpeg -ss 1 -t 4 -i out.mp4 -vf "fps=15,scale=600:-2:flags=lanczos" -loop 0 -c:v libwebp -quality 70 hero.webp
# Bản nhẹ để gửi duyệt qua Zalo/Messenger
ffmpeg -i out.mp4 -vf scale=-2:960 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k review.mp4
# Nối các khối đã render (cùng thông số) không encode lại
printf "file 'khoi1.mp4'\nfile 'khoi2.mp4'\n" > list.txt && ffmpeg -f concat -safe 0 -i list.txt -c copy full.mp4
```

## Lỗi thường gặp
| Triệu chứng | Nguyên nhân / cách sửa |
|---|---|
| `No such filter: 'drawtext'` hoặc `'ass'` | ffmpeg build thiếu libfreetype/libass → cài bản đầy đủ (`brew install ffmpeg`, `apt install ffmpeg`) |
| `Option 'text_align' not found` | ffmpeg < 6.1 → nâng cấp, hoặc xóa `text_align=center:` trong `render_edl.py` |
| Chữ tiếng Việt hiện ô vuông | Font không có dấu tiếng Việt → đặt `"font"` trong EDL sang font khác (Be Vietnam Pro, Inter, Arial) |
| Phụ đề ASS sai font | libass dùng tên font hệ thống: `--font "Be Vietnam Pro"` khi chạy make_captions.py, font phải được cài |
| Tiếng lệch hình sau khi nối | Đừng nối file thô bằng `-c copy`; để `render_edl.py` chuẩn hóa từng clip trước |
| Video iPhone bị xoay | ffmpeg tự xoay theo metadata; nếu vẫn sai, thêm `-noautorotate` rồi `transpose=1` |
