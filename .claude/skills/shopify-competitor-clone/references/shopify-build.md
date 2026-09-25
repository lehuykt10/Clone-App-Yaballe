# 🧱 Shopify build guide

## Setup

### 1. Owner prerequisites (hướng dẫn chủ store, tiếng Việt)
1. Tạo store Shopify (hoặc dùng dev store từ Shopify Partners).
2. Cài app **Theme Access** (của Shopify) → *Create password* → nhập email →
   mở email lấy mật khẩu dạng `shptka_...`.
3. Trong Claude Code on the web: environment → **Edit** → thêm biến môi trường:
   - `SHOPIFY_FLAG_STORE=<store>.myshopify.com`
   - `SHOPIFY_CLI_THEME_TOKEN=shptka_...`
4. Network access: cho phép `*.myshopify.com`, `<store-domain>`, domain đối thủ
   (hoặc chọn mức truy cập rộng hơn).
5. Kết nối **Shopify connector** tại claude.ai → Settings → Connectors (để
   Claude tạo sản phẩm, collection, trang, menu, mã giảm giá).
6. Tạo một **repo GitHub riêng** cho theme và mở session Claude Code trên repo đó.
   Copy thư mục `.claude/skills/shopify-competitor-clone/` vào repo mới
   (hoặc vào `~/.claude/skills/` để dùng cho mọi dự án).

Never commit the token. Never echo it into logs or files.

### 2. CLI
```bash
npm i -g @shopify/cli@latest            # provides `shopify`
shopify version
# Flags fall back to SHOPIFY_FLAG_STORE / SHOPIFY_CLI_THEME_TOKEN automatically
shopify theme list
```

### 3. Theme source
New theme from Dawn (MIT-licensed, fast, well-maintained):
```bash
shopify theme init theme --clone-url https://github.com/Shopify/dawn.git
cd theme && rm -rf .git   # keep it inside the brand repo's history instead
```
Existing theme the owner already paid for:
```bash
shopify theme pull --theme <ID> --path theme
```

### 4. Dev loop
```bash
shopify theme check --path theme                       # lint (fix all errors)
shopify theme push --path theme --unpublished --json   # first push → note "id"
shopify theme push --path theme --theme <ID>           # later pushes
shopify theme share --path theme                       # shareable preview link
```
`shopify theme dev` needs an interactive browser login and is not suited to
cloud sessions. Use push + preview URL
`https://<store>.myshopify.com/?preview_theme_id=<ID>`.

Never push to the live theme. Publish only on the owner's explicit OK:
`shopify theme publish --theme <ID>`.

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
Start from `templates/section-template.liquid`. Rules:
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
