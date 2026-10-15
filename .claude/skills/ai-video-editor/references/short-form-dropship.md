# Chế độ A — Video ngắn bán hàng organic (TikTok · Reels · Shorts · Facebook)

Mục tiêu của bản dựng: người xem **dừng lướt trong 1,5 giây đầu**, hiểu sản phẩm giải quyết gì trong ~5 giây, và nhìn rõ sản phẩm thật ở cuối. Bản dựng không cứu được concept yếu — nếu hook không có wow bằng mắt, quay lại skill `ai-video-director`.

## Thông số xuất
- 1080×1920, 9:16, 30fps (Topaz 60fps nếu đã upscale), H.264, AAC 48kHz, ~-14 LUFS.
- Độ dài: 7–15s cho video demo/wow; 20–35s cho vấn đề → giải pháp có voice. Dài hơn chỉ khi giữ chân tốt.
- **Vùng an toàn**: không đặt chữ/sản phẩm quan trọng ở 20% dưới đáy (caption + nút mua), 15% mép phải (nút like/share), 10% trên cùng. `position: top` (14%) và phụ đề ở 30% từ đáy đã nằm trong vùng an toàn.

## Cấu trúc nhịp mặc định (≈12s, không voice)
| Thời gian | Nội dung | Chữ overlay |
|---|---|---|
| 0–1,5s | Wow / vấn đề thấy bằng mắt, chuyển động mạnh ngay khung đầu (không mở bằng logo, không fade-in) | Text hook ≤ 7 từ |
| 1,5–5s | Sản phẩm xử lý vấn đề | — hoặc nhãn lợi ích 2–3 từ |
| 5–10s | 2–3 góc dùng thực tế, mỗi cắt 1–2s | — |
| 10–12s | Cảnh thật sản phẩm rõ nét (≥1s) | CTA nhẹ: "Link ở bio" |

Có voice: dựng theo voice. Mỗi câu voice ≈ một cảnh; cắt hình đúng lúc chuyển ý, không cắt giữa từ.

## Quy tắc dựng
- **Cắt khi đang chuyển động**, không cắt khi hình đứng yên. Vệt nhòe giữa 2 cảnh = điểm cắt đẹp.
- Không cảnh nào > 3s trong 10s đầu. Clip AI 4s thường chỉ dùng 1,5–2,5s đẹp nhất — dùng `probe.py --scenes` và xem khung để chọn `in/out`.
- Clip NCC ngang → `fit: blur` (giữ trọn sản phẩm) hoặc `fill` + chọn đoạn sản phẩm ở giữa khung.
- Tắt tiếng clip NCC (`mute`) — hay dính nhạc bản quyền hoặc tiếng Trung.
- Speed 1.2–1.5 cho cảnh thao tác chậm (mở hộp, lắp ráp).
- Chữ do ffmpeg vẽ, **không để AI sinh chữ trong hình** (AI viết sai chính tả).
- Phụ đề kiểu shorts 2–3 từ/cụm, tô màu từ đang đọc — hơn 80% người xem tắt tiếng ở lần xem đầu trên Facebook/Reels.
- Logo nhỏ góc trên phải, đục 85%. Không intro/outro thương hiệu.

## Âm thanh
- Nhạc thịnh hành tốt nhất là **thêm trong app khi đăng** (thư viện nhạc thương mại của TikTok/Meta) — không đốt nhạc có bản quyền vào file. Trong file chỉ để nhạc royalty-free hoặc không nhạc.
- Có voice: nhạc 0.10–0.18, bật `duck`.
- Tiếng động thật (ASMR: tiếng click, mở hộp) giữ lại ở `clip_audio_volume` 0.6–1.0 — thường giữ chân tốt hơn nhạc.

## Split-test: 1 bản dựng → nhiều biến thể
Giữ nguyên lõi concept, mỗi biến thể đổi **1–2 yếu tố** để biết yếu tố nào thắng. Mỗi biến thể = 1 file EDL copy rồi sửa (đặt tên `sp01_v2_hookB.json`…).
1. Text hook khác (đổi `texts[0].text`).
2. Cảnh mở đầu khác (đổi thứ tự `clips`, đưa cảnh wow mạnh nhất lên đầu).
3. Có voice / không voice.
4. Độ dài: bản 8s vs bản 15s (bỏ bớt clip giữa).
5. Thị trường: US/EU — cùng EDL, thay ảnh/clip bối cảnh.
Đặt tên file có mã biến thể và dùng cùng mã đó cho UTM, để nhật ký đạo diễn nối được view → đơn hàng.

## Kiểm tra trước khi giao (QA)
- [ ] Khung đầu tiên đã có chuyển động và chủ thể rõ (xem khung 0 bằng ảnh tổng)
- [ ] Không chữ nào nằm trong vùng bị UI che
- [ ] Chính tả chữ overlay + phụ đề (đặc biệt dấu tiếng Việt / chính tả tiếng Anh cho thị trường US)
- [ ] Không lỗi AI lộ (tay, mặt, sản phẩm biến dạng) trong các khung đã chọn
- [ ] Sản phẩm thật xuất hiện rõ ≥ 1s, đúng màu/biến thể đang bán
- [ ] Không lời hứa y tế / "an toàn tuyệt đối"; không trình bày nhân vật AI như khách hàng thật
- [ ] Âm lượng ≈ -14 LUFS, không vỡ tiếng
- [ ] Gắn nhãn nội dung AI khi đăng nếu hình trông như thật (TikTok "AI-generated", Meta "AI info")
