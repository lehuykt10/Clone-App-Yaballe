# Hướng dẫn cài theme Zenligo Calm (Calm Cap)

Theme được dựng theo đúng khung theme Suzeno (`suzeno · product pages DRAFT v2`): cùng các section `sz-product` (gói mua 1/2, cart drawer), `sz-band`, `sz-story`, `sz-hotspots`, `sz-steps`, `sz-faq-contact`, `sz-testimonials`. Đổi sang nhận diện Zenligo: màu indigo/mist, font Fraunces + Figtree, copy Calm Cap.

- File zip: `zenligo-theme.zip` (gốc repo) · Mã nguồn: thư mục `zenligo-theme/`
- Đã **tắt đồng hồ đếm ngược** (header và trang sản phẩm). Chỉ bật khi có ưu đãi thật có hạn.
- Đã **xoá các dòng "taxes & duties included"** của Suzeno (chưa xác nhận cho Zenligo).
- Đã sửa 1 lỗi CSS có sẵn trong Suzeno: `.band` thiếu dấu `;` (`position:relativecolor:#fff`) làm chữ của dải band không ra màu trắng. Theme Suzeno vẫn còn lỗi này.

## Bước 1 — Tải theme lên (không ảnh hưởng web đang chạy)
Shopify Admin → **Online Store → Themes → Add theme → Upload zip file** → chọn `zenligo-theme.zip`.
Theme mới vào mục chưa xuất bản → bấm **Preview** để xem bản demo. Chỉ **Publish** sau khi duyệt xong.

## Bước 2 — Tạo sản phẩm
Products → Add product:
| Trường | Giá trị |
|---|---|
| Title | Zenligo Calm Cap — 2-in-1 Hot & Cold Head Wrap |
| URL handle | `calm-cap` (bắt buộc đúng, trang chủ đang trỏ vào handle này) |
| Price | $34.99 · Compare-at: **để trống** (không dùng giá gạch ảo) |
| Theme template | `product.calm-cap` |
| Vendor | Zenligo |
| Weight | điền cân nặng thật (gel ~300–400 g) để tính ship |
| Media | thứ tự gợi ý: GIF kéo mũ lên-xuống → nền trắng → Blackout → See-through → nóng/lạnh → kích thước → hộp |

## Bước 3 — Giảm giá gói 2 cái (bắt buộc)
Theme chỉ **hiển thị** giá gói; muốn khách thực trả đúng giá đó phải tạo discount:
Discounts → Create → **Amount off products** → Automatic → tên "Gift pack: 2 Calm Caps" → **$7.50 off each item** → Minimum quantity **2** → áp dụng cho Calm Cap.
→ 2 cái = $54.98 (khớp với số theme hiển thị).

## Bước 4 — Ảnh trong các section (Customize theme)
| Section | Ảnh cần chọn |
|---|---|
| Image with story | Ảnh người đang đeo, chế độ See-through, làm việc máy tính |
| Feature hotspots | Ảnh cận cái mũ (nền trắng) → kéo 4 điểm (Flip-up eye panel, 360° gel, ponytail opening, stretch fabric) cho đúng vị trí |
| Header (theme settings → Brand) | Logo Zenligo + favicon |

Ảnh gửi cho Claude: tôi sẽ tải lên Files và gắn vào sản phẩm/section khi kết nối được store Zenligo.

## Bước 5 — Trang & chính sách
- Settings → Policies: tạo Refund (30 ngày), Shipping, Privacy, Terms.
- Navigation: menu `main-menu` (Shop, FAQ `#faq`, Contact) và `footer` (các policy).
- Email hỗ trợ: theme settings → Brand → `support@zenligo.com` (đổi nếu khác).

## Cần xác nhận với nhà cung cấp trước khi publish
- Cách làm ấm (microwave? bao nhiêu giây?) → sửa accordion "How to chill or warm it" + bước "Warm".
- Thời gian giữ lạnh thực tế (đang ghi 15–20 phút).
- Thời gian giao hàng thật (đang ghi 7–12 ngày làm việc) và hạn đặt kịp Giáng sinh (đang ghi Dec 5).
- Có túi đựng kèm không (đang không ghi).

## Không được làm (rule Zenligo)
- Không ghi "migraine relief", "without painkillers", "clinically proven" ở bất kỳ đâu.
- Không thêm review/đánh giá sao khi chưa có khách thật (section Testimonials tự ẩn khi trống).
- Không dùng ảnh NCC có chữ tuyên bố y tế hoặc logo BANZHIK.
