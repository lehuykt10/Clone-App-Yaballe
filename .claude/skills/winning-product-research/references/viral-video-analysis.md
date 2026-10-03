# Giải mã video viral bằng AI

## 1. Bảng Viral Library (thu thập)

| # | Nền tảng | Link | View | Like | Comment | Share/Save | Ngày đăng | Follower kênh | Sản phẩm | Giá | Hook 3 giây đầu | Format |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Chỉ số phụ cần tính:
- **Viral ratio** = View / Follower (≥ 5 là sản phẩm/nội dung tự lan truyền).
- **Engagement** = (Like + Comment + Share) / View (≥ 5% tốt, ≥ 10% rất tốt).
- **Save/Share rate** = (Save + Share) / View — cao nghĩa là khách "để dành mua sau".
- **Purchase-intent rate** = comment ý định mua / tổng comment (≥ 5% mạnh).

## 2. Lấy transcript & comment

- YouTube: phụ đề tự động (nút "Show transcript"), hoặc `yt-dlp --write-auto-sub --skip-download <url>`.
- TikTok/Reels: tải video bằng công cụ hợp lệ, chuyển giọng nói thành chữ bằng Whisper hoặc tính năng transcript của AI; comment có thể xuất bằng extension/công cụ scrape (tuân thủ điều khoản nền tảng).
- Chỉ dùng để **phân tích**, không đăng lại nội dung của người khác.

## 3. Prompt phân tích video YouTube dài (review / so sánh)

```
Bạn là chuyên gia research sản phẩm cho brand DTC. Dưới đây là transcript video YouTube
"[tiêu đề]" ([số view] view) trong ngách [ngách].

Hãy trích xuất và trả về dạng bảng:
1. Các sản phẩm được nhắc đến: tên, giá, điểm khen, điểm chê.
2. Tiêu chí mua hàng mà người nói dùng để đánh giá (xếp theo mức độ quan trọng).
3. Nỗi đau/khó chịu của người dùng được nhắc đến (trích nguyên câu).
4. "Sản phẩm lý tưởng" mà người nói mô tả nhưng chưa tồn tại.
5. 5 khoảng trống biến thể (thuộc tính khách muốn mà chưa sản phẩm nào có đủ).
6. Câu nói/ngôn từ có thể dùng làm hook quảng cáo.

Transcript:
[dán transcript]
```

## 4. Prompt giải mã video ngắn viral (TikTok / Reels / Shorts)

```
Phân tích video ngắn viral sau ([view] view, [comment] comment) bán sản phẩm [tên].
Transcript + mô tả cảnh: [dán]

Trả về:
- HOOK (0–3s): hình ảnh gì, câu gì, loại hook (vấn đề / kết quả / tò mò / phản bác / POV / ASMR).
- CẤU TRÚC theo giây: hook → vấn đề → demo → bằng chứng → CTA.
- GÓC BÁN chính (angle): tiết kiệm thời gian, đẹp hơn, đỡ đau, đáng tiền, quà tặng, nhận diện bản thân…
- CẢM XÚC chủ đạo và "khoảnh khắc wow".
- Vì sao video này lan truyền (giả thuyết dựa trên cấu trúc).
- 3 kịch bản MỚI dùng cùng cấu trúc nhưng cho sản phẩm [sản phẩm biến thể của tôi],
  thay hoàn toàn lời thoại, bối cảnh và nhân vật (không sao chép).
```

## 5. Prompt phân loại comment (Purchase-Intent Mining)

```
Dưới đây là [N] comment từ các video viral về [sản phẩm]. Phân loại mỗi comment vào:
A. Ý định mua (hỏi link, giá, đã đặt hàng)
B. Hỏi biến thể (màu, size, chất liệu, phiên bản khác)
C. Phản đối / nghi ngờ (đắt, chất lượng, không hiệu quả)
D. Nỗi đau / bối cảnh sử dụng
E. Khác

Rồi trả về:
- Tỷ lệ % mỗi nhóm.
- Top 10 yêu cầu biến thể (nhóm B) kèm số lần lặp lại.
- Top 10 phản đối (nhóm C) → cách xử lý trên landing page / video.
- 10 câu nguyên văn hay nhất để làm hook hoặc tiêu đề.

Comment:
[dán]
```

## 6. Tổng hợp thành Angle Map & Pain Map

**Angle Map**

| Góc bán | Số video dùng | Tổng view | View TB | Ví dụ hook | Đã bão hòa? |
|---|---|---|---|---|---|

**Pain Map**

| Nỗi đau | Nguồn (review/comment/YouTube) | Tần suất | Đối thủ đã giải quyết? | Cơ hội biến thể |
|---|---|---|---|---|

Quy tắc chọn: ưu tiên **góc bán có view TB cao nhưng ít video dùng** và **nỗi đau tần suất cao mà chưa ai giải quyết**.
