# 🧱 Shopify build guide

## Setup (student / owner computer)

### 1. Owner prerequisites (hướng dẫn chủ store, tiếng Việt)
1. Tạo store Shopify (hoặc dev store miễn phí từ Shopify Partners). Đổi tiền tệ
   (Settings → Store details → Store currency) **trước** khi tạo sản phẩm.
2. Cài phần mềm bằng `setup/setup-windows.ps1` hoặc `setup/setup-mac.sh` (xem HUONG-DAN).
3. Đăng nhập Shopify CLI lần đầu: lệnh `shopify theme list --store <store>.myshopify.com`
   mở trình duyệt, đăng nhập tài khoản chủ store (hoặc staff có quyền Themes).
4. (Tuỳ chọn) Kết nối **Shopify connector** tại claude.ai → Settings → Connectors để
   Claude tạo sản phẩm, trang, menu, mã giảm giá. Không có connector thì Claude viết
   hướng dẫn bấm từng bước trong Shopify Admin.

Theme Access password (`shptka_...`) is only needed on machines without a browser
(cloud sessions, CI). Never commit it, never echo it into logs or files.

### 2. CLI
```bash
shopify version
shopify theme list --store <store>.myshopify.com   # first run opens the browser login
```

### 3. Theme source
New theme (Dawn v16 + the Shopify Theme Kit, recommended):
```bash
python .claude/skills/shopify-theme-kit/scripts/new_theme.py
```
Existing theme the owner already paid for:
```bash
shopify theme pull --theme <ID> --path theme --store <store>.myshopify.com
```
(The kit's installer only supports Dawn-based themes. For other themes, build the
same sections by hand from `shopify-theme-kit/templates/section-template.liquid`.)

### 4. Dev loop
```bash
shopify theme check --path theme                                   # lint (fix all errors)
shopify theme push --path theme --unpublished --json --store <store>.myshopify.com   # first push → note "id"
shopify theme push --path theme --theme <ID> --store <store>.myshopify.com           # later pushes
```
Preview URL: `https://<store>.myshopify.com/?preview_theme_id=<ID>`.
`shopify theme dev --path theme --store <store>.myshopify.com` gives a live local
preview at http://127.0.0.1:9292 while editing.

If push fails (SSL "bad record mac", proxy, antivirus): make a zip with
`python .claude/skills/shopify-theme-kit/scripts/zip_theme.py` and upload it in
Admin → Online Store → Themes → Add theme → Upload zip file.

Never push to the live theme. Publish only on the owner's explicit OK:
`shopify theme publish --theme <ID> --store <store>.myshopify.com`.

### 5. Editing a theme that is already live
Pushing to the live theme is risky. Workflow: owner clicks **Duplicate** on the live
theme → push/upload changes into the copy → owner previews → owner clicks Publish.

---

## Build

### Theme anatomy (Dawn)
```
theme/
├── config/settings_schema.json   # global setting definitions
├── config/settings_data.json     # global values: colours, fonts, etc. ← design tokens go here
├── layout/theme.liquid           # <head>, header/footer groups
├── sections/*.liquid             # reusable blocks with {% schema %}
├── snippets/*.liquid             # partials
├── templates/*.json              # which sections each page uses, and their settings
├── assets/                       # css/js/images
└── locales/en.default.json       # UI strings
```

### Design tokens → settings_data.json
Dawn uses **colour schemes** (`scheme-1`…`scheme-5`). Map brand tokens:
- scheme-1: background / text / primary button (brand primary) / button label
- scheme-2: alt background for alternating sections
- scheme-3: inverse (dark) for hero/footer
- scheme-4: accent (sale/badge) scheme
Typography: `type_header_font`, `type_body_font` use Shopify font handles
(e.g. `assistant_n4`, `playfair_display_n7`). Check the handle exists in
Shopify's font library. Also set `buttons_radius`, `card_style`,
`page_width`, `spacing_sections`.

### Templates
- Put every section's content in `templates/*.json` settings (editable in the theme editor)
- Alternate templates for special pages: `templates/product.landing.json`,
  `templates/page.about.json`, `templates/page.faq.json`; assign them via the
  product/page `templateSuffix` (GraphQL) or in Admin
- Keep the home page ≤ 10 sections. Each section needs a clear job from the plan.

### Custom sections
Start from `.claude/skills/shopify-theme-kit/templates/section-template.liquid`. Rules:
- Scoped CSS in `{% style %}` using `#shopify-section-{{ section.id }}`, or
  a small `assets/section-<name>.css` loaded with `stylesheet_tag`
- Images: `{{ image | image_url: width: 1500 | image_tag: widths: '375,750,1100,1500', sizes: '100vw', loading: 'lazy' }}`.
  For the first section on a page use `loading: 'eager', fetchpriority: 'high'`
- No jQuery, no external CDNs; vanilla JS in `assets/`, deferred
- Every setting has a sensible `default`; include `presets` so it can be added in the editor
- Text settings are `inline_richtext` / `richtext`; translatable UI strings go in `locales`
- Accessibility: semantic headings, `alt` from `image.alt`, buttons are `<button>` or `<a>`

Common sections to build when Dawn lacks them:
| Section | Purpose |
|---|---|
| `benefits-grid` | Icons + short benefit statements |
| `comparison-table` | Us vs "typical alternatives" |
| `bundle-picker` | Quantity breaks on PDP (adds variant qty via `/cart/add.js`) |
| `sticky-atc` | Mobile sticky add-to-cart on PDP |
| `ugc-strip` | Customer photos (real, with permission) |
| `faq-accordion` | `<details>` + FAQPage JSON-LD |
| `trust-badges` | Guarantee, shipping, secure payment |
| `free-shipping-bar` | Cart drawer progress bar using `cart.total_price` |

### JSON-LD
Dawn outputs Product JSON-LD on PDP. Add Organization (in `layout/theme.liquid`)
and FAQPage (in `faq-accordion`), BreadcrumbList on collection/product.
Validate with Google's Rich Results Test once live.

---

## Store data via Shopify connector

Load tools: `ToolSearch("select:mcp__Shopify__get-shop-info,mcp__Shopify__create-product,...")`.
Always `get-shop-info` first and confirm the store name with the owner.

### Built-in tools (preferred)
| Task | Tool |
|---|---|
| Products | `create-product` (status `DRAFT`), `update-product` |
| Collections | `create-collection` (smart rules by TAG/TYPE), `add-to-collection` |
| Discounts | `create-discount` (ask the owner for start date and audience) |
| Go live | `bulk-update-product-status` → ACTIVE after owner review |
| Inventory | `set-inventory` (only when tracked) |

Product images must be **public HTTPS URLs the owner has rights to**. Local
files can't be uploaded by the connector. Ask the owner to upload to Shopify
Files (Admin → Content → Files) and share the URLs.

### GraphQL recipes (always run `graphql_schema` → `validate_graphql_codeblocks` first; the schema is the source of truth)
Page:
```graphql
mutation($page: PageCreateInput!) {
  pageCreate(page: $page) { page { id handle } userErrors { field message } }
}
# variables: { "page": { "title": "About Us", "handle": "about", "body": "<p>…</p>", "isPublished": false, "templateSuffix": "about" } }
```
Menu:
```graphql
mutation($title: String!, $handle: String!, $items: [MenuItemCreateInput!]!) {
  menuCreate(title: $title, handle: $handle, items: $items) { menu { id } userErrors { field message } }
}
# items: [{ "title": "Shop", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/…" },
#         { "title": "About", "type": "PAGE", "resourceId": "gid://shopify/Page/…" }]
```
The main menu already exists (`main-menu`), so use `menuUpdate` with its ID
(query `menus(first: 10)` to find it).

SEO on products: `productUpdate(product: { id, seo: { title, description } })`.
Metafields (e.g. PDP FAQ, ingredients): `metafieldsSet(metafields: [{ ownerId, namespace: "custom", key, type, value }])`.

---

## QA
1. `shopify theme check`: 0 errors
2. Capture script on the preview URL → compare with competitor (scorecard)
3. Read mobile screenshots of every page and fix overflow, overlapping, tiny text
4. Click-test the flow: home → collection → PDP → variant → ATC → cart drawer → checkout button (don't place orders; the owner runs the test order)
5. `grep -ri "<competitor brand>" theme/` returns nothing
