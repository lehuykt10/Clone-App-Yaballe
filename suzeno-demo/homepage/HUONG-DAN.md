# Suzeno: trang chủ mới (nhiều sản phẩm)

- Bản xem trước: https://claude.ai/artifact/WKRMYrXkweNmgNLdZgtH9v
- `suzeno-theme-homepage.zip`: theme đang chạy (`suzeno-theme-glow-wings`, đã đối chiếu checksum ngày 25/11) + trang chủ mới.
  Tất cả trang sản phẩm (Glow Wings, Puddle Suit, hoodie…) giữ nguyên.

## Trang chủ mới gồm
| # | Section | Nội dung | Sửa trong Customize |
|---|---|---|---|
| 1 | **Hero banner** (mới) | Ảnh Glow Wings trên tuyết, tiêu đề "Gifts for the pets who make us smile", nút *Shop gifts* (cuộn xuống lưới) + *Meet Glow Wings* | Đổi ảnh, chữ, nút, độ tối lớp phủ |
| 2 | **Product grid** (mới) | 4 sản phẩm đang bán: Glow Wings (nhãn *New*), Cuddle Hoodie (*Christmas*), Burrow Hoodie, Puddle Suit. Rê chuột thấy ảnh thứ 2. Nút *Shop all products* → /collections/shop-all | Thêm/bớt/đổi sản phẩm (tối đa 12), đổi nhãn |
| 3 | Image with story | Glow Wings: "Dark evenings, but your dog still *shines*" + nút *Shop Glow Wings* | Có thêm ô nút bấm |
| 4 | Image with story | Hoodie có túi thú cưng + nút *Shop hoodies* | |
| 5 | Steps or benefits | 4 cam kết: free shipping, đã gồm thuế, 30-day guarantee, hỗ trợ trong 1 ngày làm việc | |
| 6 | FAQ and contact | 5 câu hỏi chung (hạn Giáng sinh Dec 5, thời gian giao, thuế, đổi trả, gói giảm giá) + form liên hệ + tra cứu đơn | |

Code mới: `sections/sz-hero.liquid`, `sections/sz-product-grid.liquid`, thêm nút cho `sections/sz-story.liquid`,
nâng cấp `snippets/product-card.liquid` (nhãn + ảnh thứ 2, trang collection cũng được dùng), CSS riêng `assets/sz-home.css` (nạp trong `layout/theme.liquid`; `suzeno.css` giữ nguyên).

> **Đã tải lên Shopify (25/11/2026):** theme **"suzeno · homepage (review this)"** (chưa publish) = bản sao theme đang chạy + 7 file trên, đã đối chiếu checksum. Chỉ cần Preview rồi Publish; không cần tải zip.

## Cài đặt
1. Online Store → Themes → **Add theme → Upload zip file** → `suzeno-theme-homepage.zip`.
2. Bấm **Preview**, kiểm tra trên điện thoại và máy tính → **Publish**.
3. Nếu sau khi tải zip lên, ảnh hero hoặc ảnh hoodie không hiện: Customize → chọn section → chọn lại ảnh từ Files.

## Nên làm thêm trong Shopify Admin (không thuộc theme)
- **Menu chính** (Content → Menus → Main menu): `Shop All` · `Glow Wings` · `Hoodies` · `Christmas` · `Contact`.
- **SEO trang chủ** (Online Store → Preferences):
  - Title: `Suzeno | Pet Gifts, Dog Hoodies & Night Walk Lights`
  - Meta description: `Cozy pet pouch hoodies, full-body dog raincoats and glowing night walk lights. Free worldwide shipping, taxes included, 30-day guarantee.`
- **Collection "Shop All"**: đang đếm 10 sản phẩm (gồm cả bản nháp và Unlisted). Khách chỉ thấy sản phẩm Active. Nếu muốn bán lại Paw Kit, Pounce Toy, Star Cape, chuyển chúng sang Active rồi thêm vào lưới trang chủ.
- **Đồng hồ đếm ngược ở header** ("Holiday deals end in", tự reset lúc 0 giờ): nên tắt nếu ưu đãi không thật sự hết hạn.
- **Puddle Suit** đang có giá gạch $42.99. Chỉ để nếu sản phẩm thực sự từng bán ở giá đó.
