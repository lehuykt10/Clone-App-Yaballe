---
description: Tạo/cập nhật sản phẩm, trang, menu, mã giảm giá khớp với theme
---
Goal: the Shopify store data matches the theme (product handle, bundle discounts, pages with templates,
menus, welcome code).

1. If Shopify connector tools (`mcp__Shopify__*` / GraphQL tools) are available: `get-shop-info` first and
   confirm the domain with the student (hard rule 5). Always follow graphql_schema → validate → execute.
   If not available: produce a Vietnamese click-by-click guide for each item below instead.
2. Product: handle = brand.json `product.handle` (never ™ or accents), options/variants, price, real
   compare-at only, SEO title/description from copy, status DRAFT until the student approves, publish to
   Online Store sales channel, alt text for images. Colour option: tell the student how to set native
   swatch colours, or add names to `snippets/bundle-picker-color.liquid`.
3. **Automatic discounts that match the bundle tiers** (one per tier with discount > 0):
   amount mode → "$X off each item, minimum quantity N, applies to this product";
   percent mode → "X% off, minimum quantity N". Explain that without them the cart charges full price.
4. Welcome code from brand.json `newsletter.welcome_code` (10 %, once per customer, not combinable with
   bundle discounts) + tell the student to add it to Marketing → Automations → Welcome new subscribers.
5. Pages with template suffix: about (`about`), faq (`faq`), how-it-works (`how-it-works`),
   contact (`contact`), track-order. Menus: main (Home, Shop/product, How it works, FAQ, Contact),
   footer (policies, Track order, Contact).
6. Shipping zones / markets / taxes: read-only check; if they don't match brand.json delivery and the
   policies, tell the student exactly what to change in Settings.
7. Update PROGRESS.md with all IDs. Next: `/chinh-sach`.
