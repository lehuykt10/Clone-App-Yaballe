# Bộ skill tạo website Shopify vượt đối thủ (cài cho Claude Code trên máy tính)

Gồm 2 skill dùng chung với nhau:

| Skill | Công dụng |
|---|---|
| `shopify-competitor-clone` | Quy trình tổng quát: phân tích **bất kỳ** website đối thủ → lập kế hoạch vượt → dựng store Shopify mới (theme Dawn + Shopify CLI + Shopify connector) → chấm điểm so với đối thủ |
| `pet-hoodie-store` | Skill ngách cho store hoodie bế thú cưng (đối thủ huggiecat.com): bản phân tích đối thủ, sơ đồ store, và các section dựng sẵn (gói mua nhiều giảm giá, nút mua cố định, bảng size, bảng so sánh, FAQ) |

---

## 1. Cài phần mềm (làm 1 lần)

| Phần mềm | Cách cài | Kiểm tra |
|---|---|---|
| Node.js 20+ | https://nodejs.org (bản LTS) | `node -v` |
| Python 3 | https://python.org (Windows: tích "Add to PATH") | `python3 --version` (Windows: `py --version`) |
| Git | https://git-scm.com | `git --version` |
| Claude Code | `npm install -g @anthropic-ai/claude-code` | `claude --version` |
| Shopify CLI | `npm install -g @shopify/cli@latest` | `shopify version` |
| Playwright + Chromium (cho script phân tích đối thủ) | `npm install -g playwright` rồi `npx playwright install chromium` | `npx playwright --version` |

## 2. Cài skill

Giải nén file zip, rồi chép **2 thư mục skill** vào một trong hai chỗ:

**Cách A: dùng cho mọi dự án (khuyên dùng)**
- macOS / Linux: `~/.claude/skills/`
- Windows: `C:\Users\<tên bạn>\.claude\skills\`

```bash
# macOS / Linux
mkdir -p ~/.claude/skills
cp -r shopify-competitor-clone pet-hoodie-store ~/.claude/skills/
```
```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\.claude\skills"
Copy-Item -Recurse shopify-competitor-clone, pet-hoodie-store "$HOME\.claude\skills\"
```

**Cách B: chỉ cho 1 dự án**: chép vào `<thư mục dự án>/.claude/skills/`.

Cấu trúc đúng sau khi chép:
```
~/.claude/skills/
├── shopify-competitor-clone/SKILL.md
└── pet-hoodie-store/SKILL.md
```

Mở Claude Code và gõ `/skills` để thấy 2 skill trong danh sách.

> Nếu dùng Cách A, trong các lệnh của skill hãy thay đường dẫn
> `.claude/skills/...` bằng `~/.claude/skills/...`. Claude tự làm việc này khi biết skill nằm ở đâu.

## 3. Chuẩn bị Shopify

1. Tạo store Shopify (hoặc dev store miễn phí tại partners.shopify.com).
2. Cài app **Theme Access** → *Create password* → lấy mật khẩu `shptka_...` trong email.
3. Tạo file `.env` trong thư mục dự án (**không** đưa lên GitHub):
   ```
   SHOPIFY_FLAG_STORE=ten-store.myshopify.com
   SHOPIFY_CLI_THEME_TOKEN=shptka_xxxxxxxx
   ```
   Trên máy tính cá nhân cũng có thể bỏ qua bước này và đăng nhập bằng trình duyệt: `shopify theme dev --store ten-store.myshopify.com`
4. Kết nối Shopify để Claude tạo sản phẩm, collection, trang, menu, mã giảm giá:
   - Kết nối **Shopify** tại claude.ai → Settings → Connectors, rồi đăng nhập Claude Code bằng
     cùng tài khoản claude.ai (`claude` → `/login`). Gõ `/mcp` để kiểm tra Shopify đã hiện chưa.
   - (Tuỳ chọn) Thêm máy chủ tài liệu dành cho lập trình viên của Shopify để Claude tra tài liệu và API chính xác hơn:
     `claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest`
   - Không có kết nối thì Claude hướng dẫn bạn làm các bước đó trong Shopify Admin.

## 4. Bắt đầu làm việc

```bash
mkdir my-pet-store && cd my-pet-store
git init
claude
```
Gõ vào Claude Code, ví dụ:

```
Dùng skill shopify-competitor-clone và pet-hoodie-store.
Phân tích đối thủ https://huggiecat.com/products/pet-tote-carier-hoodie
và dựng store mới cho thương hiệu <TÊN> tại <store>.myshopify.com.
```

Claude sẽ làm theo thứ tự:
1. Chạy script phân tích đối thủ: ảnh chụp, cấu trúc trang, giá, app, tốc độ tải
2. Viết kế hoạch vượt đối thủ → **dừng chờ bạn duyệt**
3. Tạo bộ nhận diện và nội dung riêng (không sao chép chữ/ảnh của đối thủ)
4. Tải theme Dawn, cài các section dựng sẵn, dựng trang
5. Đẩy lên theme chưa xuất bản và gửi bạn link xem trước
6. Chấm điểm so với đối thủ → **dừng chờ bạn duyệt** → chỉ publish khi bạn đồng ý

## 5. Lưu ý
- Chỉ sao chép **bố cục và chiến lược bán hàng**. Không sao chép chữ, ảnh, logo, đánh giá hay code của đối thủ (dễ bị DMCA gỡ store, khóa tài khoản quảng cáo và cổng thanh toán).
- Gói "mua nhiều giảm giá" chỉ hiển thị giá. Phải tạo mã giảm giá tự động trong Shopify cùng mức % thì giỏ hàng mới trừ tiền thật.
- Không bao giờ đưa `shptka_...` hay file `.env` lên GitHub.
