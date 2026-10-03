# 18 phương pháp tìm sản phẩm winning trong ngách đã có doanh số

Quy tắc: **một sản phẩm chỉ được coi là "đã chứng minh" khi có ≥ 3 tín hiệu từ ít nhất 2 nhóm khác nhau** (ví dụ: video viral + ads chạy lâu + review tăng đều).

---

## Nhóm A — Tín hiệu mạng xã hội (nhu cầu cảm xúc, tốc độ lan truyền)

### 1. Săn video viral theo ngưỡng view
- Tìm trên TikTok, Instagram Reels, YouTube Shorts bằng từ khóa ngách + từ khóa mua sắm: `yoga must haves`, `pilates at home`, `tiktok made me buy it`, `amazon finds fitness`, `gym essentials`.
- Lọc: ≥ 100K view, đăng trong 90 ngày, tài khoản < 50K follower (view cao trên kênh nhỏ = **sản phẩm** viral, không phải **người** viral).
- Ghi vào bảng Viral Library (mẫu trong `viral-video-analysis.md`).

### 2. Đào comment có ý định mua (Purchase-Intent Mining)
- Từ khóa vàng trong comment: "link?", "where did you get", "need this", "just ordered", "add to cart", "does it come in…", "is it worth it", "mua ở đâu", "xin link".
- **Tỷ lệ comment ý định mua / tổng comment ≥ 5%** = tín hiệu mạnh.
- Comment dạng "does it come in [màu/size/chất liệu]?" = **gợi ý biến thể miễn phí**.

### 3. Phân tích video YouTube dài bằng AI
- Video review/so sánh 10–30 phút có view cao (≥ 100K) chứa: tiêu chí khách hàng dùng để chọn, điểm yếu từng sản phẩm, giá kỳ vọng.
- Lấy transcript → đưa AI phân tích (prompt ở `viral-video-analysis.md`).
- Đặc biệt giá trị: video "I tested 10 yoga mats", "best/worst…", "honest review after 6 months".

### 4. Theo dõi tốc độ hashtag / âm thanh / trend
- TikTok Creative Center → Trends (hashtags, songs, creators) và **Top Ads / Top Products** lọc theo ngành & quốc gia.
- Tìm hashtag đang tăng nhanh nhưng chưa bão hòa (ví dụ: `#wallpilates`, `#somaticexercise`, `#pilatesprincess` từng là các trend như vậy).

### 5. Thư viện quảng cáo (Ad Library) — tín hiệu "đang có lãi"
- Meta Ad Library, TikTok Top Ads: **quảng cáo chạy liên tục ≥ 30 ngày, nhiều biến thể creative** = nhà bán đang có lãi.
- Một brand chạy 20+ creative cho cùng 1 sản phẩm = sản phẩm đã được chứng minh.

### 6. Công cụ dữ liệu TikTok Shop
- Kalodata, FastMoss, Shoplus, EchoTik (và tương tự): xem doanh số ước tính theo ngày, video bán hàng tốt nhất, creator mang doanh số.
- Tìm sản phẩm **doanh số tăng nhưng ít shop bán** (cạnh tranh thấp).

### 7. Pinterest Trends & Instagram Explore
- Pinterest dẫn trước 3–6 tháng với ngách thẩm mỹ (home yoga studio, athleisure, wellness decor).

---

## Nhóm B — Dữ liệu sàn thương mại (bằng chứng có người trả tiền)

### 8. Amazon Best Sellers / Movers & Shakers / New Releases
- Theo dõi category ngách hằng tuần; Movers & Shakers = sản phẩm tăng BSR mạnh trong 24h.
- Công cụ: Helium 10, Jungle Scout, Keepa (lịch sử BSR & giá).
- Tiêu chí tốt: top 10 có ≥ 3 listing **< 500 review** nhưng doanh thu cao → ngách chưa bị khóa bởi ông lớn.

### 9. Review mining 1–3★ (mỏ vàng cho biến thể)
- Đọc 100–300 review xấu của 5 đối thủ top → gom nhóm nỗi đau ("trơn khi đổ mồ hôi", "mùi cao su", "quá mỏng cho đầu gối", "khó cuộn").
- Mỗi nỗi đau lặp lại ≥ 10 lần = **một cơ hội biến thể**.

### 10. AliExpress / 1688 / Alibaba order velocity
- Sắp xếp theo "orders", xem sản phẩm mới có đơn tăng nhanh. 1688 thường đi trước AliExpress vài tuần.
- Dùng để tìm nhà máy đã sản xuất sẵn khuôn gần giống biến thể bạn muốn.

### 11. Spy store Shopify
- Tìm store đối thủ (từ ads, video) → dùng công cụ như Koala Inspector, PPSPY, Shopify "/products.json" công khai, Similarweb để ước lượng traffic & sản phẩm mới.
- Store mở < 6 tháng mà traffic tăng mạnh = đang có sản phẩm thắng.

### 12. Kickstarter / Indiegogo / Product Hunt
- Chiến dịch gọi vốn thành công = nhu cầu đã được trả tiền trước. Thường chưa có hàng phổ thông giá tốt → cơ hội cho phiên bản dễ tiếp cận hơn (không sao chép thiết kế có bằng sáng chế).

---

## Nhóm C — Nhu cầu & cộng đồng (hiểu "vì sao" khách mua)

### 13. Google Trends / Exploding Topics / Glimpse
- Xác nhận xu hướng tăng bền (đường đi lên 12–24 tháng), không phải spike 2 tuần.
- So sánh nhiều từ khóa con trong ngách để tìm ngách con đang lên.

### 14. Reddit, Facebook Groups, Discord, Quora
- r/yoga, r/pilates, r/homegym, r/xxfitness… Tìm câu hỏi lặp lại: "Is there a product that…", "I wish…", "What do you use for…".
- Đây là nơi tìm **ngôn ngữ thật của khách** để viết hook & landing page.

### 15. Chênh lệch thị trường (Cross-market Arbitrage)
- Trend thường đi: Douyin/Xiaohongshu (Trung Quốc) → Hàn/Nhật → TikTok US → EU/Úc → Đông Nam Á.
- Sản phẩm viral ở thị trường A 3–6 tháng trước nhưng chưa có ở thị trường B = cửa sổ cơ hội.

### 16. Chuyên gia & creator trong ngách
- Theo dõi huấn luyện viên yoga/pilates, physiotherapist: họ dùng/đề xuất đạo cụ gì? Đạo cụ chuyên nghiệp → phiên bản dùng tại nhà là công thức kinh điển.

---

## Nhóm D — Tư duy chiến lược

### 17. Bản đồ khoảng trống biến thể (Variant Gap Map)
- Lập ma trận: trục 1 = thuộc tính (chất liệu, kích thước, màu, tính năng, đối tượng), trục 2 = sản phẩm đối thủ. Ô trống mà comment/review đang đòi = sản phẩm của bạn. (Chi tiết `variant-creation.md`.)

### 18. Lịch mùa vụ & sự kiện
- Ngách fitness: đỉnh tháng 1 (New Year), tháng 5–6 (summer body), Black Friday. Ra sản phẩm **trước** đỉnh 6–8 tuần để tích review và nội dung.

---

## Gợi ý kết hợp theo ngân sách

| Ngân sách | Phương pháp nên dùng |
|---|---|
| $0 | 1, 2, 3, 4, 9, 13, 14 (thủ công + AI miễn phí) |
| $100–300/tháng | thêm 5, 6, 8 (Kalodata/FastMoss, Helium 10/Jungle Scout bản cơ bản) |
| $500+/tháng | thêm 11, 15 + thuê agent/VA ở Trung Quốc kiểm tra 1688 & Douyin |
