# Suzeno · Glow Wings Night Walk Light: hướng dẫn đưa lên website

- Bản xem trước: https://claude.ai/artifact/4pzPSQ48vQqEUKbWdijQjr
- `suzeno-theme-glow-wings.zip`: theme Suzeno hiện tại (`suzeno · product pages DRAFT v2`) cộng thêm template `product.glow-wings.json`
- `suzeno-glow-wings-images.zip`: 7 ảnh đã đặt tên sẵn

## ⚠️ Đọc trước: sản phẩm thật khác ảnh
Đây là **đèn chiếu gắn vòng cổ**, chiếu hình đôi cánh **xuống mặt đất**. Ảnh có đôi cánh sáng lơ lửng bên cạnh chó là ảnh minh họa (rất có thể là ảnh AI).
- Trang đã viết đúng: "projects glowing wings onto the ground", kèm mục **How it looks in real life** và câu FAQ "Will it look like the photos?".
- **Trước khi chạy quảng cáo, phải có video quay thật lúc trời tối** (xin nhà cung cấp, hoặc tự quay khi có mẫu). Nếu khách thấy hàng khác ảnh quá nhiều, tỷ lệ hoàn tiền sẽ cao và dễ bị khiếu nại vì quảng cáo sai sự thật.
- Không dùng 3 ảnh có chữ "Safer Night Walks", "Walk & Shine" và "Butterfly Light For Dogs". Đó là ảnh có chữ của store khác, dùng lại dễ dính bản quyền.

## Bước 1: Tải ảnh lên Files
Shopify Admin → **Content → Files → Upload files** → chọn 7 ảnh trong `suzeno-glow-wings-images.zip` (giải nén trước).
**Giữ nguyên tên file.** Template tìm ảnh theo đúng tên:
- `suzeno-glow-wings-golden-fairy.jpg`: section câu chuyện
- `suzeno-glow-wings-light-device.jpg`: section chấm giải thích chi tiết

## Bước 2: Tạo sản phẩm
Products → Add product:
| Trường | Giá trị |
|---|---|
| Title | Glow Wings Night Walk Light |
| Description | A small light that wraps around your dog's collar and projects glowing wings onto the path around them, with a side light that helps others spot your dog after dark. |
| Media | 6 ảnh kiểu cánh + ảnh thiết bị (`light-device`) |
| Price | $26.95 (đề xuất) · Compare-at: **để trống** |
| Option | Tên option: **Style** (bắt buộc đúng tên để hiện ô chọn màu) |
| Variants | Rainbow Butterfly · Golden Fairy · Pink Dragon · Purple Dragon · Pink Heart Angel · White Angel |
| Ảnh từng variant | Gắn đúng ảnh cho từng variant (khi khách chọn kiểu, ảnh tự đổi) |
| Weight | **0.25 kg** (theo trang 1688: 250 g; hỏi lại NCC đây là cân nặng có hộp hay chưa) |
| URL handle | `glow-wings-light` |
| Theme template | `product.glow-wings` (chỉ hiện sau Bước 3) |

## Bước 3: Đưa template lên theme (chọn 1 trong 2 cách)
**Cách A: tải zip (an toàn, không đụng web đang chạy)**
Online Store → Themes → **Add theme → Upload zip file** → `suzeno-theme-glow-wings.zip` → **Preview**. Duyệt xong mới bấm **Publish**.

**Cách B: chỉ thêm template vào theme đang chạy**
Online Store → Themes → ⋯ → **Edit code** → thư mục `templates` → **Add a new template** → loại *product*, tên `glow-wings` → dán toàn bộ nội dung file `theme/templates/product.glow-wings.json` → Save.

## Bước 4: Giảm giá gói (bắt buộc)
Theme chỉ **hiển thị** giá gói. Để giá lúc thanh toán khớp, tạo 2 discount tự động:
| Gói | Discount |
|---|---|
| 2 lights | Amount off products · **$4.50 off each** · Minimum quantity 2 · áp dụng Glow Wings → $44.90 |
| 3 lights | **$7.00 off each** · Minimum quantity 3 → $59.85 |

Shopify chỉ áp **một** discount tự động có lợi nhất cho mỗi sản phẩm, nên mua 3 cái sẽ nhận $7/cái.

## Bước 5: Điền chỗ tô vàng
Trong theme editor (Customize → chọn trang Glow Wings), sửa các accordion và FAQ đang ghi `⟨XÁC NHẬN VỚI NCC⟩`:
- có kèm cáp sạc không,
- loại pin, thời gian sạc, thời gian sáng mỗi lần sạc,
- cách sạc (USB-C?).

**Không publish khi còn chữ `⟨XÁC NHẬN VỚI NCC⟩`** trên trang.

## Cần hỏi nhà cung cấp (1688)
1. Video quay thật lúc trời tối, cận cảnh hình chiếu trên đường nhựa, cỏ và tuyết.
2. Mỗi đèn là **một hình cố định** hay **đổi được miếng hình** (gobo)? Nếu đổi được, có thể bán "1 đèn + 3 hình" như một biến thể khác biệt.
3. Pin, thời gian sạc, thời gian sáng, có chống nước không.
4. Cân nặng có hộp, và có chứng nhận pin để gửi hàng (MSDS / UN38.3) không.

## Lưu ý về theme Suzeno hiện tại
- Header đang bật **đồng hồ đếm ngược tự reset lúc 0 giờ** ("Holiday deals end in"). Đây là cài đặt sẵn của store; nếu ưu đãi không thật sự hết hạn, nên tắt để tránh rủi ro quảng cáo gây hiểu lầm. Trang Glow Wings đã tắt đồng hồ riêng của trang sản phẩm.
- Trong zip, tôi đã sửa lỗi CSS `.band` thiếu dấu `;` (dải tiêu đề không nhận đúng màu chữ). Nếu dùng Cách B, lỗi này vẫn còn trên theme đang chạy.

## Chính sách của nhà cung cấp (từ mục 购买须知 trên trang 1688)
| # | NCC ghi | Ảnh hưởng tới Suzeno |
|---|---|---|
| 1 | Không nhận trả hàng/hoàn tiền; chỉ đổi khi lỗi chất lượng | Khách đổi ý hoặc không thích: Suzeno tự chịu |
| 2 | Một phần ảnh là **ảnh mạng**, hàng thật theo ảnh thực tế; xin ảnh thật qua chat | Xác nhận ảnh đẹp không phải hàng thật → phải có ảnh/video thật trước khi chạy ads |
| 3 | Không hoàn tiền vì "không giống ảnh mạng" | Nếu khách đòi hoàn vì khác ảnh, Suzeno chịu 100% |
| 4 | Hàng vỡ phải báo trong 3 ngày làm việc sau khi nhận | Kiểm hàng ngay khi nhận (nếu nhập lô) |
| 5 | Sản phẩm **không có bản quyền/bằng sáng chế**, người bán tự kiểm tra | Tự kiểm tra bằng sáng chế/nhãn hiệu ở Mỹ trước khi bán |
| 6 | Giá chưa gồm thuế | Không ảnh hưởng nhiều khi dropship |
