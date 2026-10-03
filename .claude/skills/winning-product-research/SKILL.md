---
name: winning-product-research
description: Quy trình research sản phẩm "winning" cho brand thương mại điện tử — tìm ngách đã có doanh số, giải mã video viral (TikTok, Reels, Shorts, YouTube dài), đào comment có ý định mua, tạo biến thể sản phẩm chưa ai bán và nhân bản format video đã được chứng minh. Dùng skill này khi người dùng hỏi về tìm sản phẩm winning, research ngách, phân tích video viral, tạo biến thể sản phẩm, chấm điểm sản phẩm trước khi test, hoặc case study brand triệu đô.
---

# Winning Product Research — Bộ kỹ năng cho brand triệu đô

## Nguyên tắc cốt lõi

> **Không phát minh nhu cầu — hãy tìm nhu cầu đã được chứng minh rồi bán một phiên bản tốt hơn / khác biệt hơn.**

Một sản phẩm "winning" cho brand phải thỏa đồng thời 4 điều kiện:

1. **Ngách đã có tiền** — có người khác đang bán được (doanh số, quảng cáo chạy lâu, review tăng đều).
2. **Có "khoảnh khắc wow" quay được** — giải thích trong 3 giây bằng hình ảnh, không cần lời.
3. **Có khoảng trống biến thể** — khách đang phàn nàn điều gì đó mà chưa ai sửa.
4. **Unit economics chịu được ads** — giá bán ≥ 3× giá vốn đã ship (landed cost), biên gộp ≥ 60%.

## Quy trình 6 bước (dùng cho mọi ngách)

| Bước | Việc làm | Đầu ra |
|---|---|---|
| 1. Chọn ngách đã chứng minh | Kiểm tra quy mô ngách bằng ≥ 3 nguồn tín hiệu (xem `references/methods.md`) | Ngách + 10–20 sản phẩm đang bán chạy |
| 2. Thu thập video viral | Lấy 30–50 video ≥ 100K view trong 90 ngày gần nhất + 5–10 video YouTube dài view cao | Bảng "Viral Library" |
| 3. Giải mã bằng AI | Transcript + phân tích hook, góc bán, cảm xúc, nỗi đau, comment có ý định mua | Bảng "Angle Map" + "Pain Map" |
| 4. Đào review & comment | Review 1–3★ trên Amazon/TikTok Shop + comment "link?", "where to buy" | Danh sách điểm yếu chưa ai sửa |
| 5. Tạo biến thể | Áp ma trận biến thể (SCAMPER + Pain Map) → 3–5 ý tưởng, chấm điểm | 1–2 sản phẩm để sample |
| 6. Nhân bản format viral | Giữ cấu trúc (hook, nhịp, góc quay) — thay sản phẩm & câu chuyện | 10–20 video test |

Chi tiết từng bước:
- `references/methods.md` — **18 phương pháp** tìm sản phẩm winning, nhóm theo nguồn dữ liệu.
- `references/viral-video-analysis.md` — quy trình + prompt AI phân tích video YouTube dài, Reels, TikTok và comment.
- `references/variant-creation.md` — cách tạo biến thể "chưa ai bán" trong cùng ngách + nhân bản video.
- `references/case-studies.md` — case study các brand/sản phẩm đã làm ra hàng triệu đô và bài học áp dụng.
- `references/scorecard.md` — bảng chấm điểm 100 điểm + công thức tính từ view → đơn hàng.

## Bộ lọc nhanh "5 giây" trước khi đào sâu

Loại ngay nếu sản phẩm:
- Bán đầy ở siêu thị/Walmart với giá rẻ (không có lý do mua online).
- Cần chứng nhận y tế/FDA/pin lithium lớn/chất lỏng dễ cháy mà bạn chưa có năng lực xử lý.
- Dính bằng sáng chế/thương hiệu (kiểm tra Google Patents, USPTO) — biến thể phải **khác về thiết kế**, không sao chép.
- Giá bán < $20 (khó gánh ads) hoặc > $150 (chu kỳ quyết định dài) — trừ khi đã có kênh organic mạnh.
- Không thể quay "trước/sau" hay "đang dùng" trong video ngắn.

## Công thức kinh tế từ video viral (đọc thêm `references/scorecard.md`)

```
Đơn hàng ≈ View × Tỷ lệ click link (CTR) × Tỷ lệ chuyển đổi (CR)
Ví dụ: 100.000 view × 1,5% CTR × 3% CR ≈ 45 đơn / video
       → AOV $45 ≈ $2.000 doanh thu từ 1 video organic
       → 20 video/tháng, 25% đạt ngưỡng 100K view ≈ $10.000/tháng chỉ từ organic
```

CR 2–7% chỉ đạt được khi: landing page khớp đúng lời hứa trong video, có social proof (review có ảnh/video), và giá nằm trong vùng "mua ngay" của ngách.

## Cách Claude làm việc với skill này

1. Hỏi rõ (nếu chưa có): ngách, thị trường (US/EU/VN…), kênh bán (Shopify, TikTok Shop, Amazon, eBay), ngân sách test, năng lực sản xuất (dropship / private label / OEM).
2. Đề xuất ≥ 3 phương pháp research phù hợp nhất từ `references/methods.md` cho trường hợp đó.
3. Khi người dùng đưa link/transcript video → chạy prompt trong `references/viral-video-analysis.md`.
4. Luôn xuất kết quả dạng **bảng** (Viral Library, Angle Map, Pain Map, Variant Matrix, Scorecard).
5. Kết thúc bằng **kế hoạch test 14 ngày** có KPI rõ: hook rate ≥ 30%, CTR ≥ 1%, CR ≥ 2%, CPA ≤ 1/3 AOV.
6. Không khuyến khích sao chép nguyên video, nhạc, hình ảnh của người khác — chỉ học **cấu trúc**. Luôn nhắc kiểm tra bằng sáng chế/nhãn hiệu trước khi sản xuất.
