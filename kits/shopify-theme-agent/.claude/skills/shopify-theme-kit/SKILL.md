---
name: shopify-theme-kit
description: Build a complete, conversion-focused Shopify theme for ANY niche from one brand.json file. Downloads Dawn (pinned), installs ready-made sections (bundle picker / quantity breaks with per-unit variants, sticky add-to-cart, FAQ with JSON-LD, comparison table, benefits grid, size guide) and generates colours, fonts, home page, product page, FAQ/About/How-it-works templates, announcement bar and footer. Use when the user wants to build, rebuild or restyle a Shopify theme, "dựng theme", "tạo theme", "làm trang sản phẩm", or after a competitor teardown is approved.
---

# Shopify Theme Kit

One product store or small catalogue, any niche. The kit turns **`brand/brand.json`**
into a finished Dawn theme in **`theme/`**. Edit the JSON, re-run the build, never
hand-edit the generated templates (they get overwritten).

## Commands (run from the project root)

| Step | Command |
|---|---|
| 1. Get Dawn 16 + install kit | `python .claude/skills/shopify-theme-kit/scripts/new_theme.py` |
| 2. Create brand file | copy `templates/brand.example.json` → `brand/brand.json`, then fill it (see `references/brand-json.md`) |
| 3. Build | `python .claude/skills/shopify-theme-kit/scripts/build_store.py` |
| 4. Check | `shopify theme check --path theme` → must show **only Dawn's own 9 warnings, 0 errors** |
| 5. Preview on the store | `shopify theme push --path theme --unpublished --store <store>.myshopify.com` |
| 5b. If push fails | `python .claude/skills/shopify-theme-kit/scripts/zip_theme.py` → upload `dist/theme.zip` in Admin → Themes |

Windows: use `py` instead of `python` if `python` is not found.
`install_kit.py theme` re-installs the kit into an existing Dawn theme (safe to repeat).

## What the product page gets

Order of blocks in the main product section:
title → rating (review app) → benefit bullets → **bundle picker** (or price + variant
picker + quantity when `bundle.enabled` is false) → Add to cart → **delivery estimate by
visitor country** + payment icons → trust icons (3) → collapsible tabs.

Below it (each only if its key exists in brand.json): how it works → benefits →
story 1 → comparison → story 2 → size guide → FAQ (with FAQPage JSON-LD) → closing
banner → sticky add-to-cart bar (shows the chosen bundle total).

Home page: hero (image + text, or text-only if no image yet) → featured product →
benefits → how it works → extra stories → closing → FAQ subset → newsletter (+ welcome
code shown after signup).

## Rules that keep the store honest (and ad accounts safe)

1. **Bundle prices must be real.** The bundle picker only *displays* discounts. Create
   the same automatic discounts in Shopify (Admin → Discounts, or the connector,
   `/du-lieu-store`): amount mode = "$X off each item, min quantity N"; percent mode =
   "X% off, min quantity N". Otherwise the cart charges full price.
2. **Delivery windows** in `delivery.rules` must match the supplier's real times plus a
   2–3 day buffer, and match the shipping policy page word for word.
3. **No fake social proof.** No invented reviews, "10,000 happy customers", fake stock
   counters or fake countdowns. Rating block stays empty until a review app has real reviews.
4. **Claims:** only claims the owner can prove (certificates for "non-toxic", "FDA",
   "hypoallergenic", "waterproof IP67"…). See the niche playbook for risky claims.
5. **Compare-at prices** only if the product was really sold at that price.
6. Images referenced in brand.json must be uploaded first to Admin → Content → Files;
   use the exact file name (e.g. `hero-1.jpg`).

## Custom sections in `theme/` (editable in the theme editor)

| Section / snippet | Use |
|---|---|
| `snippets/bundle-picker.liquid` (+ block "Bundle picker" in main-product) | 1–3 tiers, per-unit variant dropdown with colour chips, badges, savings, adds several variants to cart in one click |
| `snippets/bundle-picker-color.liquid` | Colour name → chip colour map. Add the shop's colour names here, or set native swatches in Admin |
| `sections/sticky-atc.liquid` | Bar that appears when the main button scrolls away |
| `sections/faq-accordion.liquid` | FAQ + FAQPage structured data |
| `sections/comparison-table.liquid` | "Us vs typical alternatives" (never name a real competitor) |
| `sections/benefits-grid.liquid` | 2–4 column benefits or numbered steps |
| `sections/size-guide.liquid` | Size table, 4 editable columns (apparel, pet, rings, shoes) |

Need something else (UGC video strip, before/after slider, ingredient list, bundle
builder)? Start from Dawn sections first; for a new section copy
`templates/section-template.liquid`, keep settings in `{% schema %}`, add a preset,
run theme check.

## Files

| File | Purpose |
|---|---|
| `scripts/new_theme.py` | Clone Dawn v16.0.0 into `theme/` and run the installer |
| `scripts/install_kit.py` | Copy sections/snippets, patch `main-product.liquid` (render + schema block) |
| `scripts/build_store.py` | brand.json → settings_data + templates + header/footer groups |
| `scripts/zip_theme.py` | Zip for manual upload |
| `templates/brand.example.json` | Complete example (coffee set) to copy |
| `templates/section-template.liquid` | Skeleton for new custom sections |
| `references/brand-json.md` | Every brand.json key explained |
| `references/design-system.md` | Palettes, font pairs, radius, contrast rules per brand mood |
