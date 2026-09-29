# Hướng dẫn sử dụng AI Agent Thiết Kế Theme Shopify

Bộ AI Agent này chạy trong **Claude Code** trên máy tính của bạn. Bạn đưa link website
đối thủ và thông tin sản phẩm, Agent sẽ:

1. Phân tích website đối thủ: bố cục, giá, combo, app, tốc độ, điểm yếu
2. Lập kế hoạch làm tốt hơn đối thủ, **chờ bạn duyệt**
3. Tạo màu sắc, font chữ và toàn bộ nội dung riêng cho thương hiệu của bạn
4. Dựng theme Shopify hoàn chỉnh: trang chủ, trang sản phẩm có **combo mua nhiều giảm giá**,
   chọn màu/size từng sản phẩm, **thời gian giao hàng theo nước của khách**, thanh "Add to cart"
   bám theo màn hình, FAQ chuẩn Google, bảng so sánh, bảng size…
5. Đưa theme lên store của bạn ở dạng **bản nháp** để bạn xem trước
6. Tạo sản phẩm, trang, menu, mã giảm giá (nếu kết nối Shopify)
7. Viết các trang chính sách chuẩn quảng cáo Facebook và Google
8. Kiểm tra toàn bộ website, chấm điểm so với đối thủ, liệt kê việc còn phải làm

Dùng được cho **mọi ngách**: thú cưng, làm đẹp, thời trang, trang sức, nhà cửa, bếp, đồ công
nghệ, thể thao, mẹ & bé, du lịch, ô tô, quà cá nhân hoá… và cả ngách khác.

> **Bạn luôn là người quyết định.** Agent dừng lại xin ý kiến ở các bước quan trọng và
> **không bao giờ tự xuất bản (Publish) theme**.

---

## Phần 1. Chuẩn bị tài khoản

| Tài khoản | Bắt buộc? | Ghi chú |
|---|---|---|
| **Claude** (claude.ai) gói **Pro** hoặc **Max** | Bắt buộc | Claude Code cần gói trả phí (hoặc tài khoản API Anthropic Console) |
| **Shopify** | Bắt buộc | Store đang dùng thử hoặc có gói. Nên đổi **tiền tệ** (Settings → Store details → Store currency) **trước** khi tạo sản phẩm |
| GitHub | Không bắt buộc | Để sao lưu dự án lên mạng |

Máy tính: **Windows 10/11** hoặc **macOS 12 trở lên**, còn trống khoảng 5 GB, có Internet.

---

## Phần 2. Cài đặt (làm 1 lần cho mỗi máy)

### 2.1. Giải nén bộ Agent

1. Tạo thư mục **không dấu, không khoảng trắng**, không nằm trong OneDrive. Ví dụ:
   - Windows: `C:\Shopify\ten-thuong-hieu`
   - macOS: `~/Shopify/ten-thuong-hieu`
2. Giải nén file `shopify-theme-agent.zip` vào đó. Trong thư mục phải thấy trực tiếp các file
   `CLAUDE.md`, `HUONG-DAN.html` và thư mục `.claude` (thư mục ẩn), `setup`.

> Mỗi thương hiệu / store nên dùng **một thư mục riêng**: giải nén lại file zip vào thư mục mới.
> Giữ file zip gốc để dùng cho dự án sau.

> **Thư mục `.claude` bị ẩn?** Windows: File Explorer → View → Show → Hidden items.
> macOS: trong Finder bấm `Cmd + Shift + .`

### 2.2. Cài phần mềm tự động

**Windows**

1. Mở thư mục dự án trong File Explorer.
2. Bấm vào thanh địa chỉ phía trên, gõ `powershell` rồi Enter. Cửa sổ PowerShell mở đúng thư mục đó.
3. Dán lệnh sau rồi Enter:
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1
   ```
4. Nếu Windows hỏi "Do you want to allow this app to make changes…", chọn **Yes**.
   Quá trình cài mất 5–15 phút (Node.js, Python, Git, Shopify CLI, trình duyệt Chromium, Claude Code).
5. Cài xong, **đóng PowerShell và mở lại** (bước 1–2) để máy nhận phần mềm mới.
6. Kiểm tra lại:
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1 -CheckOnly
   ```
   Tất cả phải hiện `[OK]`.

**macOS**

1. Mở **Terminal** (Cmd + Space, gõ Terminal).
2. Gõ `cd ` (có dấu cách), kéo thư mục dự án thả vào cửa sổ Terminal, Enter.
3. Chạy:
   ```bash
   bash setup/setup-mac.sh
   ```
   Máy có thể hỏi mật khẩu đăng nhập Mac (gõ không hiện chữ, cứ gõ rồi Enter).
4. Mở cửa sổ Terminal mới, kiểm tra: `bash setup/setup-mac.sh --check`

<details>
<summary>Cài tay (nếu script lỗi)</summary>

| Phần mềm | Tải | Kiểm tra |
|---|---|---|
| Node.js LTS (≥ 20) | https://nodejs.org | `node -v` |
| Python 3.10+ (Windows: tích **Add python.exe to PATH**) | https://www.python.org | `py --version` / `python3 --version` |
| Git | https://git-scm.com | `git --version` |
| Shopify CLI | `npm install -g @shopify/cli@latest` | `shopify version` |
| Playwright + Chromium | `npm install -g playwright` rồi `npx playwright install chromium` | `npx playwright --version` |
| Claude Code | https://claude.com/claude-code (hoặc `npm install -g @anthropic-ai/claude-code`) | `claude --version` |
</details>

### 2.3. Đăng nhập Claude Code

Trong PowerShell / Terminal, đang ở thư mục dự án, gõ:
```bash
claude
```
Lần đầu Claude Code mở trình duyệt để đăng nhập tài khoản claude.ai. Đăng nhập xong quay lại
cửa sổ lệnh. Nếu được hỏi **"Do you trust the files in this folder?"** chọn **Yes**.

Kiểm tra Agent đã nhận: gõ `/tro-giup` → phải hiện bảng lệnh tiếng Việt.
Gõ `/agents` → phải thấy 4 agent: competitor-analyst, brand-copywriter, theme-builder, store-auditor.

### 2.4. Đăng nhập Shopify CLI

Mở **cửa sổ lệnh thứ hai** ở thư mục dự án (giữ Claude Code ở cửa sổ đầu), gõ
(thay `ten-store` bằng store của bạn, xem trong Shopify Admin → Settings → Domains):
```bash
shopify theme list --store ten-store.myshopify.com
```
Trình duyệt mở ra → đăng nhập tài khoản **chủ store** (hoặc nhân viên có quyền Themes) →
quay lại, thấy danh sách theme là xong.

### 2.5. (Tuỳ chọn, nên làm) Kết nối Shopify cho Claude

Để Agent **tự tạo** sản phẩm, trang, menu, mã giảm giá:
1. Vào https://claude.ai → ảnh đại diện → **Settings** → **Connectors**.
2. Tìm **Shopify** → **Connect** → đăng nhập store → cho phép.
3. Trong Claude Code gõ `/mcp` → thấy Shopify ở trạng thái connected.

Không kết nối cũng được: Agent sẽ hướng dẫn bạn bấm từng bước trong Shopify Admin.

---

## Phần 3. Làm website từ A đến Z

Mở Claude Code trong thư mục dự án (`claude`), rồi đi lần lượt các lệnh. Có thể gõ yêu cầu
bằng tiếng Việt bình thường thay cho lệnh.

| Bước | Gõ lệnh | Agent làm gì | Bạn làm gì | Thời gian |
|---|---|---|---|---|
| 1 | `/bat-dau` | Kiểm tra máy, hỏi thông tin, tạo hồ sơ thương hiệu | Trả lời câu hỏi | 10 phút |
| 2 | `/phan-tich-doi-thu https://…` | Chụp và phân tích web đối thủ, lập kế hoạch vượt | **Duyệt kế hoạch** | 10–20 phút |
| 3 | `/thuong-hieu` | Màu, font, nội dung, cấu hình combo, thời gian giao | **Duyệt màu và nội dung** | 10–20 phút |
| 4 | `/dung-theme` | Dựng theme hoàn chỉnh, kiểm tra lỗi | Tải ảnh lên Shopify (Agent báo tên file) | 5–10 phút |
| 5 | `/xem-truoc` | Đưa theme lên store dạng bản nháp, gửi link | **Xem trên điện thoại và máy tính** | 5 phút |
| 6 | `/du-lieu-store` | Sản phẩm, trang, menu, mã giảm giá khớp combo | Duyệt sản phẩm | 10–20 phút |
| 7 | `/chinh-sach` | 4 trang chính sách + checklist quảng cáo | Cung cấp địa chỉ, tên pháp lý; dán vào Settings → Policies | 10 phút |
| 8 | `/kiem-tra` | Chấm điểm so với đối thủ, danh sách việc cần sửa | Quyết định sửa gì | 10 phút |
| – | `/sua <yêu cầu>` | Sửa bất kỳ thứ gì | – | tuỳ |
| – | `/tro-giup` | Xem đang ở bước nào, bước tiếp theo | – | – |

Agent ghi tiến độ vào file `PROGRESS.md`. Hôm sau mở lại `claude`, gõ `/tro-giup` là
Agent biết làm tiếp từ đâu.

### Bước 1. `/bat-dau`

Ví dụ:
```
/bat-dau https://www.doi-thu.com/products/san-pham
```
Chuẩn bị sẵn để trả lời:
- Tên thương hiệu, tên miền (nếu có), địa chỉ `ten-store.myshopify.com`
- Sản phẩm: tên, giá bán, các biến thể (màu, size), link nhà cung cấp
- Thị trường (Mỹ, châu Âu, toàn thế giới…), tiền tệ
- **Thời gian giao của nhà cung cấp** theo nước (ví dụ Mỹ 7–14 ngày)
- Thuế nhập khẩu: đã gồm trong giá hay khách tự trả
- Ảnh/video sản phẩm bạn có quyền dùng

### Bước 2. `/phan-tich-doi-thu`

Agent mở web đối thủ bằng trình duyệt ẩn, chụp màn hình máy tính và điện thoại, đo tốc độ,
đọc cấu trúc từng trang và app họ dùng. Kết quả nằm trong thư mục `teardown/`.

Bạn nhận được bản tóm tắt: đối thủ mạnh gì, yếu gì, **10 điểm mình sẽ làm tốt hơn**, sơ đồ
trang. Trả lời "Duyệt" hoặc yêu cầu sửa.

> Nếu web đối thủ chặn: Agent sẽ nhờ bạn chụp màn hình (máy tính + điện thoại) trang chủ,
> trang sản phẩm và kéo thả ảnh vào Claude Code.

### Bước 3. `/thuong-hieu`

Agent đề xuất bảng màu, font chữ, kiểu bo góc, câu tiêu đề, nội dung trang sản phẩm, FAQ,
và **combo** (ví dụ Mua 1 / Mua 2 tiết kiệm $10 / Mua 3 tiết kiệm $24). Mọi thứ được lưu vào
file `brand/brand.json`. Bạn có thể nói: "đổi màu nút sang xanh lá", "combo 2 giảm 15%"…

Những chỗ đánh dấu ❓ là thông tin Agent phải giả định: hãy trả lời để nội dung chính xác.

### Bước 4. `/dung-theme` và tải ảnh

Agent tải theme **Dawn** (theme chính thức, miễn phí, nhanh nhất của Shopify), cài thêm
các section bán hàng và dựng toàn bộ trang.

**Tải ảnh lên Shopify:** Shopify Admin → **Content** → **Files** → **Upload files**.
Đặt tên file không dấu, ví dụ `hero-1.jpg`. Gửi tên file cho Agent, Agent sẽ gắn vào đúng chỗ.
Kích thước gợi ý: ảnh đầu trang 2400×1200, ảnh sản phẩm vuông 2048×2048, ảnh minh hoạ 1600×1200.

Ảnh sản phẩm (gallery) thì tải trong **Products** → chọn sản phẩm → **Media**.

### Bước 5. `/xem-truoc`

Agent đẩy theme lên store ở dạng **Unpublished** (khách không thấy) và gửi link dạng
`https://ten-store.myshopify.com/?preview_theme_id=123456`.

Kiểm tra trên điện thoại: bấm chọn combo, đổi màu từng sản phẩm, bấm Add to cart, xem giỏ hàng,
xem dòng thời gian giao hàng, mở FAQ.

**Xuất bản:** khi đã hài lòng, vào **Online Store** → **Themes** → ở theme mới bấm **…** →
**Publish**. (Agent không bao giờ tự làm bước này.)

### Bước 6. `/du-lieu-store`

- Tạo/cập nhật sản phẩm đúng đường dẫn (handle) mà theme dùng
- **Tạo mã giảm giá tự động khớp combo**. Rất quan trọng: combo trên trang chỉ *hiển thị* giá;
  nếu không có mã giảm giá tự động, giỏ hàng sẽ tính **giá đầy đủ**
- Mã chào mừng (ví dụ `WELCOME10`) hiện ra ngay sau khi khách đăng ký email ở trang chủ
- Trang About, FAQ, How it works, Contact, Track order + menu

Nên tự bật thêm: **Marketing** → **Automations** → **Welcome new subscribers** (gửi mã qua email).

### Bước 7. `/chinh-sach`

Agent viết 4 trang: Refund, Shipping, Terms of Service, Contact information, khớp đúng với
cài đặt ship, thuế, thời gian giao. Sau đó bạn dán từng nội dung vào
**Settings** → **Policies** (bấm nút `<>` trong khung soạn thảo trước khi dán).

### Bước 8. `/kiem-tra`

Agent kiểm tra như một chuyên gia: tốc độ, hiển thị trên điện thoại, SEO, câu chữ có vi phạm
chính sách quảng cáo không, thông tin có mâu thuẫn không, và chấm điểm so với đối thủ. Kết quả:
🔴 phải sửa trước khi chạy quảng cáo · 🟡 giúp tăng tỷ lệ mua · ⚪ nên làm thêm.

---

## Phần 4. Sửa website sau khi đã xuất bản

Không sửa trực tiếp theme đang chạy. Làm theo 4 bước:
1. **Online Store** → **Themes** → theme đang chạy → **…** → **Duplicate** (tạo bản sao).
2. Trong Claude Code: `/sua đổi thời gian giao Mỹ thành 8–15 ngày` (hoặc yêu cầu bất kỳ).
3. `/xem-truoc` → Agent đẩy lên **bản sao** và gửi link xem trước.
4. Hài lòng thì **Publish** bản sao.

Ví dụ yêu cầu:
- `/sua thêm combo 4 sản phẩm giảm 30%`
- `/sua đổi tông màu sang pastel hồng, bo góc tròn hơn`
- `/sua thêm bảng size cho áo: S, M, L, XL với số đo ngực và dài áo`
- `/sua thêm câu hỏi FAQ: có giao hàng đến Canada không?`
- `/sua bỏ phần so sánh, thêm section video hướng dẫn`

---

## Phần 5. Lỗi thường gặp

| Lỗi | Cách xử lý |
|---|---|
| `running scripts is disabled on this system` | Dùng đúng lệnh `powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1` |
| `'claude' / 'shopify' / 'node' is not recognized` | Đóng hết cửa sổ lệnh, mở lại. Vẫn lỗi: khởi động lại máy |
| Gõ `python` mở Microsoft Store | Dùng `py` thay cho `python`. Hoặc Settings → Apps → Advanced app settings → App execution aliases → tắt python.exe và python3.exe |
| `SSL ... bad record mac` hoặc lỗi mạng khi `shopify theme push` | Tắt VPN/phần mềm diệt virus quét HTTPS rồi thử lại. Vẫn lỗi: Agent tạo file `dist/theme.zip`, bạn tải lên ở **Online Store** → **Themes** → **Add theme** → **Upload zip file** |
| Shopify CLI đăng nhập nhầm tài khoản | `shopify auth logout` rồi chạy lại lệnh `shopify theme list --store …` |
| `Cannot find module 'playwright'` / thiếu trình duyệt | `npm install -g playwright` rồi `npx playwright install chromium` |
| Web đối thủ chặn, ảnh chụp trắng | Tự chụp màn hình trang đối thủ và kéo thả vào Claude Code |
| Giỏ hàng không trừ tiền combo | Chưa có mã giảm giá tự động khớp combo → `/du-lieu-store` |
| Ảnh không hiện trên trang | Tên file trong brand.json phải trùng tên trong Content → Files (kể cả .jpg/.png) |
| Thời gian giao không đổi theo nước | Bật Markets cho các nước đó và giữ "country selector" ở header |
| Link sản phẩm báo 404 | Handle sản phẩm phải trùng `product.handle` trong brand.json; không dùng ký tự ™ hay dấu |
| Thư mục nằm trong OneDrive, lỗi đường dẫn | Chuyển dự án ra `C:\Shopify\...` |
| Claude Code hỏi quyền chạy lệnh | Đọc lệnh; lệnh an toàn chọn **Yes**. Lệnh `shopify theme push/publish` luôn được hỏi lại để bảo vệ bạn |

---

## Phần 6. Quy tắc bắt buộc (để không bị khoá tài khoản)

1. **Chỉ học bố cục và chiến lược bán hàng của đối thủ.** Không sao chép chữ, ảnh, video, logo,
   đánh giá, code của họ: dễ bị DMCA gỡ store, khoá tài khoản quảng cáo và cổng thanh toán.
2. **Không đánh giá giả**, không "10.000 khách hàng" khi chưa có, không đồng hồ đếm ngược giả,
   không giá gạch (compare-at) chưa từng bán.
3. **Không nói quá công dụng** (chữa bệnh, giảm cân, an toàn tuyệt đối…) khi không có giấy tờ.
   Agent có danh sách từ cấm theo từng ngách.
4. **Thời gian giao hàng** = thời gian nhà cung cấp + 2–3 ngày dự phòng, ghi giống nhau ở
   trang sản phẩm, FAQ và chính sách.
5. Không gửi mật khẩu, mã `shptka_…` hay file `.env` cho ai, không đưa lên GitHub.

---

## Phần 7. Câu hỏi thường gặp

**Chi phí?** Gói Claude Pro/Max + gói Shopify. Theme Dawn và bộ Agent miễn phí.

**Dùng cho theme trả phí khác Dawn được không?** Phân tích đối thủ, nội dung, chính sách,
kiểm tra thì được. Phần tự dựng theme (combo, thời gian giao…) được thiết kế cho Dawn; với theme
khác Agent sẽ hướng dẫn làm tương tự bằng tay.

**Store nhiều sản phẩm?** Được. Theme áp dụng cho mọi sản phẩm; trang chủ nổi bật 1 sản phẩm
chính (có thể đổi trong theme editor thành bộ sưu tập).

**Bán thị trường không nói tiếng Anh?** Nói với Agent ở `/bat-dau` (ví dụ: bán ở Đức, tiếng Đức).
Nội dung sẽ viết bằng ngôn ngữ đó.

**Sửa bằng tay trong Theme Editor được không?** Được, nhưng lần sau Agent dựng lại từ
`brand/brand.json` sẽ ghi đè nội dung các trang. Tốt nhất: nói với Agent để sửa trong brand.json.

**Làm store thứ hai?** Giải nén file zip vào thư mục mới và bắt đầu lại từ `/bat-dau`.

---

## Phần 8. Cấu trúc thư mục

```
ten-thuong-hieu/
├── CLAUDE.md            "bộ não" của Agent (quy trình, quy tắc)
├── HUONG-DAN.html       tài liệu này
├── PROGRESS.md          tiến độ dự án (Agent tự ghi)
├── setup/               script cài đặt Windows / macOS
├── brand/               hồ sơ thương hiệu, nội dung, brand.json, chính sách
├── teardown/            phân tích đối thủ, kế hoạch, bảng điểm
├── theme/               theme Shopify (Agent tạo ở bước 4)
├── dist/                file theme.zip để tải lên tay (khi cần)
└── .claude/
    ├── agents/          4 agent chuyên môn
    ├── commands/        10 lệnh tắt tiếng Việt
    ├── skills/          kiến thức: quy trình clone, bộ theme, playbook ngách, chính sách
    └── settings.json    quyền chạy lệnh an toàn
```
