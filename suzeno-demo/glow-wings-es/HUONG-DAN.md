# Suzeno · Glow Wings: trang bán tiếng Tây Ban Nha

- Bản xem trước: https://claude.ai/artifact/4y6vxtT76xPSCr1oZPjVkH
- Link sau khi publish: **https://suzeno.com/products/glow-wings?view=glow-wings-es**
- `suzeno-theme-glow-wings-es.zip`: theme đang chạy (trang chủ mới) cộng thêm trang tiếng Tây Ban Nha. Chỉ dùng khi muốn tải lên thủ công.

> **Đã tải lên Shopify (26/11/2026):** theme **"suzeno · Glow Wings ES (review this)"**, chưa publish. Theme này là bản sao theme đang chạy, thêm 10 file bên dưới; cả 10 file đã đối chiếu checksum. Bạn chỉ cần Preview rồi Publish, không cần tải zip.

## Cách hoạt động
- Vẫn là **cùng một sản phẩm** Glow Wings: cùng giá $36.95, cùng 6 kiểu, cùng tồn kho, cùng 2 discount gói ($4.50/cái khi mua 2, $7/cái khi mua 3).
- Thêm `?view=glow-wings-es` vào cuối link sản phẩm thì Shopify hiển thị template `product.glow-wings-es`. Không cần tạo sản phẩm thứ hai.
- Nội dung viết bằng tiếng Tây Ban Nha Mỹ Latinh, xưng *tú*, nhắm tới người nói tiếng Tây Ban Nha ở Mỹ và Mỹ Latinh. Gồm: tiêu đề phụ, gói giá, mô tả, cách hoạt động, 3 bước, 8 câu FAQ, form liên hệ, tra cứu đơn (17track bản tiếng Tây Ban Nha).
- Trên trang tiếng Tây Ban Nha, header, thanh chữ chạy, giỏ hàng, menu và footer cũng tự chuyển sang tiếng Tây Ban Nha. Các trang tiếng Anh không đổi.

## File đã thay đổi
| File | Thay đổi |
|---|---|
| `templates/product.glow-wings-es.json` | Template mới, toàn bộ nội dung tiếng Tây Ban Nha |
| `sections/sz-product.liquid`, `assets/sz-product.js` | Thêm các ô chữ nút và gói giá (Add to cart, You save, Item…) để dịch. Mặc định vẫn là tiếng Anh |
| `sections/sz-faq-contact.liquid` | Thêm các ô chữ cho form liên hệ và tra cứu đơn |
| `sections/header.liquid`, `sections/footer.liquid` | Thêm chữ thông báo, chữ chạy và newsletter bản tiếng Tây Ban Nha (sửa được trong Customize → Header/Footer → *Spanish pages*) |
| `snippets/cart-drawer.liquid`, `assets/suzeno.js`, `layout/theme.liquid`, `config/settings_schema.json` | Giỏ hàng, thông báo "Agregado al carrito", `lang="es"`, dòng chữ dưới tổng tiền (Theme settings → Cart) |

## Cần làm
1. Online Store → Themes → **"suzeno · Glow Wings ES (review this)"** → **Preview**.
2. Trong Preview, mở `/products/glow-wings?view=glow-wings-es`. Kiểm tra trên điện thoại: chọn gói 2 cái, chọn 2 kiểu khác nhau, thêm vào giỏ.
3. Mở `/products/glow-wings` (không có `?view`) và trang chủ để chắc chắn bản tiếng Anh vẫn như cũ.
4. Nếu ổn, bấm **Publish**.

## Lưu ý
- **Trang thanh toán vẫn hiện tiếng Anh.** Muốn checkout bằng tiếng Tây Ban Nha: Settings → **Languages** → Add language → *Spanish* → Publish. Shopify tự dịch các trang thanh toán. Sau đó link `suzeno.com/es/products/glow-wings?view=glow-wings-es` sẽ hiện cả trang lẫn checkout bằng tiếng Tây Ban Nha.
- **Tên menu** (Shop All, Contact…) và **tên kiểu** (Rainbow Butterfly, Golden Fairy…) vẫn là tiếng Anh, vì đó là dữ liệu của store, không phải của theme. Có thể dịch bằng app *Translate & Adapt* sau khi bật Spanish.
- Header trên trang tiếng Tây Ban Nha ghi "OFERTAS NAVIDEÑAS TERMINAN EN" kèm đồng hồ đếm ngược tự reset lúc 0 giờ. Nếu ưu đãi không thật sự hết hạn, nên tắt đồng hồ (Customize → Header) để tránh quảng cáo gây hiểu lầm.
- Thanh chữ chạy có câu "PIDE ANTES DEL 5 DE DIC. PARA RECIBIR EN NAVIDAD (EE. UU.)". Sau ngày 5/12, xóa câu này trong Customize → Header → *Scrolling text (Spanish)*.
- Chạy quảng cáo tiếng Tây Ban Nha: dùng link có `?view=glow-wings-es` và thêm UTM, ví dụ `?view=glow-wings-es&utm_source=instagram&utm_campaign=glowwings_es_v1`.
- Sửa nội dung: Customize → chọn template **product · glow-wings-es** ở menu trên cùng → sửa từng section như trang tiếng Anh.
