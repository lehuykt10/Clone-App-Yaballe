# Zenligo Baby: theme

Theme Dawn 16 + Shopify Theme Kit, dựng từ `brand/brand.json`.

Dựng lại sau khi sửa brand.json (chạy ở thư mục này):
```bash
python ../../kits/shopify-theme-agent/.claude/skills/shopify-theme-kit/scripts/new_theme.py      # lần đầu
python ../../kits/shopify-theme-agent/.claude/skills/shopify-theme-kit/scripts/build_store.py
shopify theme check --path theme
python ../../kits/shopify-theme-agent/.claude/skills/shopify-theme-kit/scripts/zip_theme.py --out dist/zenligo-baby-theme.zip
```

## Việc chủ store cần làm trong Shopify Admin
1. Online Store → Themes → Add theme → Upload zip file → `zenligo-baby-theme.zip` (không Publish ngay; bấm Customize để xem).
2. Pages: tạo About (template `page.about`), FAQ (`page.faq`), How it works (`page.how-it-works`), Track your order, Contact (`page.contact`).
3. Navigation: main menu (Home, Shop all → /collections/all, How it works, FAQ, Contact); footer menu (chính sách + Track order + Contact).
4. Discounts → Automatic discount → Amount off products: 10% khi mua tối thiểu 2 sản phẩm; 15% khi tối thiểu 3 (khớp combo trên trang sản phẩm).
5. Discount code `WELCOME10`: 10%, mỗi khách 1 lần, không cộng dồn với giảm giá combo.
6. Gỡ nội dung cũ của ngách máy massage mắt (sản phẩm, trang, chính sách, menu).

## Cần xác nhận (❓)
- Thời gian giao thật của nhà cung cấp (đang để US 9–17, CA/UK/AU 10–20, khác 12–25, châu Phi/Nam Mỹ 15–35 ngày).
- Email hỗ trợ support@zenligo.com có hoạt động không.
- Thuế nhập khẩu: đã gồm trong giá hay chưa (đang không ghi gì về thuế).
