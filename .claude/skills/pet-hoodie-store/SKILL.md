---
name: pet-hoodie-store
description: Niche playbook for building a one-product Shopify store selling a pet carrier hoodie (hoodie with a front pouch for cats and small dogs), modelled on and built to beat huggiecat.com and thehuggiez.com. Ships ready-made Dawn sections (quantity breaks, sticky add-to-cart, size guide, comparison table, FAQ with JSON-LD), an installer, the store blueprint and the competitor teardown. Use together with shopify-competitor-clone whenever the user mentions huggiecat, pet/cat carrier hoodie, pet pouch hoodie, or wants a store "like huggiecat but better".
---

# 🐱 Pet Carrier Hoodie Store: niche playbook

This skill is the **niche layer** on top of `shopify-competitor-clone`
(general workflow, capture script, legal guardrails, build guide). Follow that
skill's phases and use this one for the niche-specific parts:

| Phase (shopify-competitor-clone) | Use from this skill |
|---|---|
| 1–2 Capture and teardown | `references/competitor-huggiecat.md` (start here, complete it after capture) |
| 2 Plan | `references/store-blueprint.md` (sitemap, section order, beat-them targets) |
| 3 Brand and copy | Blueprint → "Copy angles" and "Compliance" |
| 5 Build theme | `scripts/install_sections.py` + `theme/` sections |
| 6 Store data | Blueprint → "Discounts for quantity breaks" |

Talk to the owner in **Vietnamese**. Store content is in **English**.

## Competitors
- Main: https://huggiecat.com/products/pet-tote-carier-hoodie
- Secondary: https://www.thehuggiez.com/products/huggiez-pet-hoodie
- Price anchors: Amazon/Etsy/Walmart "cat carrier hoodie"

The teardown is **partial**: the cloud network policy blocked the site. First
step in a new session: try the capture. If it's blocked, ask the owner to allow
`huggiecat.com` and `thehuggiez.com` in the environment's Network access.

## Ready-made theme parts (`theme/`)
| File | What it does |
|---|---|
| `snippets/quantity-breaks.liquid` + `main-product-block.json` | "Buy 1 / 2 (−10%) / 3 (−15%)" selector inside the product form; updates prices on variant change; sets the form quantity. Replaces the `quantity_selector` block |
| `sections/sticky-atc.liquid` | Sticky add-to-cart bar once the main button scrolls away; clicks the real button so the cart drawer and bundles still work |
| `sections/size-guide.liquid` | Editable table: size, chest, length, max pet weight |
| `sections/comparison-table.liquid` | Us vs "regular carrier" ✓/✕ table (never name real brands) |
| `sections/faq-accordion.liquid` | `<details>` accordion + FAQPage JSON-LD |

Also use `benefits-grid` from `shopify-competitor-clone/templates/section-template.liquid`.

Install into a Dawn theme (idempotent):
```bash
python3 .claude/skills/pet-hoodie-store/scripts/install_sections.py theme
shopify theme check --path theme      # must add 0 new offenses
```
Then in `templates/product.json`: add the `quantity_breaks` block to
`main` (before `buy_buttons`), remove `quantity_selector`, and add the
sections in the blueprint's PDP order. Put all copy in the JSON settings.

**Quantity breaks display prices only.** Always create the matching automatic
discounts (blueprint → Discounts) and test the cart before launch.

## Owner inputs still needed (hỏi chủ store)
- Tên thương hiệu, tên miền, store `xxx.myshopify.com`
- Nhà cung cấp, giá vốn, giá bán, màu và size thực tế, bảng số đo
- Ảnh/video sản phẩm có quyền sử dụng (tự quay với thú cưng thật là tốt nhất)
- Thời gian giao hàng thực tế, chính sách đổi trả
- Theme Access token + Shopify connector + mở quyền mạng (xem shopify-competitor-clone/references/shopify-build.md)

## Tested
- `install_sections.py` on Dawn 16.0.0: `shopify theme check` reports 0 new offenses
- quantity-breaks JS (Playwright): selecting a tier sets the form quantity; a
  variant-change event reprices all tiers (e.g. $50 → 2× −10% = $90.00)
