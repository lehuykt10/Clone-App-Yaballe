---
name: shopify-competitor-clone
description: Clone-and-beat workflow for Shopify. Takes any competitor website URL and a new brand brief, tears the competitor down (structure, sections, design tokens, apps, pricing, speed, SEO, trust), then rebuilds a complete, better Shopify store for the new brand using a Dawn-based theme, Shopify CLI and the Shopify connector (products, collections, pages, menus, discounts). Use whenever the user says "clone website đối thủ", "copy/clone competitor store", "làm web giống <site>", "phân tích đối thủ Shopify", "build a Shopify store like X but better", or gives a competitor URL for a new brand.
---

# 🛍️ Shopify Competitor Clone → Rebuild Better

You take **one or more competitor URLs** plus a **new brand brief** and ship a
complete Shopify store that keeps what works for the competitor and beats them
where they are weak.

**Rule zero: clone the *structure*, never the *assets*.**
Copy page layouts, section order, conversion patterns, offer mechanics, UX
flows and pricing logic. **Never** copy their text, images, videos, logo,
brand name, product photos, reviews or theme/app source code. Everything the
customer sees must be original to the new brand. Details:
`references/legal-guardrails.md`. If the owner asks to copy assets verbatim,
explain the risk in Vietnamese and offer the original alternative.

**Language:** talk to the owner in **Vietnamese**. Write store content in the
brand's target-market language (usually English for US/UK/CA/AU).

---

## 📥 Inputs (collect before starting)

Copy `templates/brand-brief.md` to `brand/brand-brief.md` in the working repo
and fill it in with the owner. Minimum to start:

1. Competitor URL(s): 1 main + up to 2 secondary
2. New brand name, niche, target market, tone of voice
3. Products (title, price, supplier/image source), or "use the competitor's
   assortment as a pricing reference only"
4. Store domain `xxx.myshopify.com` (the owner logs in to Shopify CLI in the browser)
5. Brand assets available: logo, colours, fonts, product photos (or "need
   placeholders")

Anything missing → list it in Vietnamese as a checklist and continue with the
phases that do not depend on it.

---

## 🔁 Workflow

Work through the phases in order. Each phase writes files, so the work can
resume in a later session. **⛔ = stop and get the owner's OK before going on.**

### Phase 1: Capture the competitor

```bash
node .claude/skills/shopify-competitor-clone/scripts/capture_site.mjs <competitor-url> --pages 6
```

Output in `teardown/<host>/`:
- `report.md`: platform + theme + apps, performance (TTFB/LCP/CLS/weight),
  design tokens (fonts, sizes, colours, radius), SEO, trust signals, nav, and
  a **section-by-section table for every page** (home, collection, product,
  about, FAQ, blog)
- `screens/*.png`: full-page desktop + mobile screenshots. **Look at them**
  with the Read tool; the tables alone miss visual hierarchy.
- `report.json`: raw data, including the catalogue summary (price range,
  product types, options) when the site is Shopify

If the capture fails:
- `Cannot find module 'playwright'` / missing browser → run
  `npm install -g playwright` then `npx playwright install chromium`
- The site blocks bots (403, Cloudflare page, empty screenshots) → retry once with
  `--pages 3`; otherwise ask the owner for full-page screenshots (desktop + mobile) of
  home, product, cart and FAQ and read those images instead
- In a cloud session, `ERR_TUNNEL_CONNECTION_FAILED` means the environment's network
  policy blocks the host: tell the owner to allow the domain in the environment's
  Network access setting
Meanwhile continue with Phase 3 prep.

### Phase 2: Teardown and "beat them" plan ⛔

Fill `references/teardown-template.md` into `teardown/<host>/teardown.md`:
- Page map and section order per template (home / collection / product /
  cart / about / FAQ)
- Offer mechanics: bundles, quantity breaks, free-shipping threshold,
  guarantee, urgency, upsells
- Apps detected (reviews, upsell, subscriptions, pop-ups) and what each does
- **Weaknesses**: score the competitor with `references/beat-them-checklist.md`

Then write `teardown/plan.md`:
1. **Keep**: patterns worth reproducing (why they convert)
2. **Beat**: at least 10 concrete improvements with measurable targets
   (e.g. "mobile LCP 4.8s → < 2.5s", "add FAQ + JSON-LD to PDP", "sticky ATC on mobile")
3. **Differentiate**: the brand angle that makes it *not* look like a copy
   (colours, typography, photography style, voice, a unique section)
4. Sitemap for the new store + section list per template, mapped to Dawn
   sections or new custom sections

Present a short Vietnamese summary of the plan to the owner. ⛔ Wait for approval.

### Phase 3: Brand system

Create `brand/`:
- `brand-brief.md` (filled in)
- `design-tokens.md`: palette (primary, accent, text, background, sale,
  success; check contrast ≥ 4.5:1), heading/body fonts (Shopify font library
  or Google-free alternatives), radius, spacing, button style. **Must differ
  visibly from the competitor.**
- `copy/`: original copy for each page, written from the brand brief and plan
  (headlines, benefits, FAQ, product descriptions, policies). Never paraphrase
  the competitor's text line by line; write from the product facts.

### Phase 4: Theme setup

Use the **shopify-theme-kit** skill:
1. `python .claude/skills/shopify-theme-kit/scripts/new_theme.py` (Dawn v16 + kit sections)
   or `shopify theme pull` if the owner already has a Dawn-based theme, then
   `python .claude/skills/shopify-theme-kit/scripts/install_kit.py theme`
2. `git init` in the project if needed and commit after every meaningful step

### Phase 5: Build the theme

1. Write `brand/brand.json` from the approved plan, brand system and copy
   (keys: `shopify-theme-kit/references/brand-json.md`; palettes and fonts:
   `shopify-theme-kit/references/design-system.md`; niche specifics: the
   **niche-playbooks** skill)
2. `python .claude/skills/shopify-theme-kit/scripts/build_store.py`
3. Anything the plan needs that the kit lacks: reuse Dawn sections first; otherwise a
   new section from `shopify-theme-kit/templates/section-template.liquid`, with a
   `{% schema %}` and preset so the owner can edit it in the theme editor
4. `shopify theme check --path theme`: 0 errors, no new warnings
5. Push to an **unpublished** theme and share the preview link

### Phase 6: Store data (Shopify connector)

Use the Shopify MCP tools (`mcp__Shopify__*`, load them with ToolSearch). If
they are missing, ask the owner to connect Shopify in claude.ai → Settings → Connectors.
- `get-shop-info` first to confirm the right store
- Products: `create-product` (status DRAFT, original titles and descriptions,
  images from **public HTTPS URLs the owner owns**), variants + options
- Collections: `create-collection` (smart rules by tag/type where possible)
- Pages (About, FAQ, Shipping, Contact), menus, SEO fields, metafields: use
  the GraphQL workflow (`graphql_schema` → `validate_graphql_codeblocks` →
  `graphql_mutation`). Mutations: `pageCreate`, `menuCreate`/`menuUpdate`,
  `productUpdate` (seo), `metafieldsSet`
- Discounts: `create-discount` (confirm start date and audience with the owner)
- Legal policies: generate in Admin → Settings → Policies (the owner does
  this), then edit them to fit the brand

### Phase 7: QA and benchmark vs competitor ⛔

```bash
node .claude/skills/shopify-competitor-clone/scripts/capture_site.mjs "https://<store>.myshopify.com/?preview_theme_id=<ID>" --out teardown/_ours --pages 6
```

(Password-protected dev stores: ask the owner for the storefront password,
or run QA after they disable the password page.)

Write `teardown/scorecard.md`: our store vs competitor, same metrics side by
side (LCP, CLS, weight, requests, JSON-LD, alt text, trust signals, sections),
plus a checklist pass from `references/beat-them-checklist.md`. Every "Beat"
target from the plan must be ✅ or explained. Look at our mobile screenshots
for broken layout.

Report to the owner in Vietnamese: preview link, scorecard summary, what is
left for them (photos, policies, payments, domain, apps). ⛔ Publish only
when the owner says so: `shopify theme publish --theme <ID>`.

### Phase 8: Launch checklist

See `references/beat-them-checklist.md` → "Launch". Payments, shipping
zones, taxes, domain, Google/Meta channels, analytics, 301 redirects (if
migrating), test order, remove password page.

---

## 📁 Files in this skill

| File | Use |
|---|---|
| `scripts/capture_site.mjs` | Capture any site (competitor or our preview): screenshots, sections, tokens, apps, perf, SEO, catalogue |
| `references/teardown-template.md` | Structure for the competitor teardown |
| `references/beat-them-checklist.md` | Scoring rubric + targets + launch checklist |
| `references/shopify-build.md` | Theme setup, CLI, section patterns, Shopify connector/GraphQL recipes |
| `references/legal-guardrails.md` | What may and may not be copied |
| `templates/brand-brief.md` | Owner input form |
| (theme kit) `shopify-theme-kit/templates/section-template.liquid` | Starting point for custom sections |

## ✅ Definition of done

- [ ] Every page in the plan's sitemap exists and renders on mobile + desktop
- [ ] No competitor text, images, logo or code in the theme or store
- [ ] `shopify theme check`: 0 errors
- [ ] Scorecard shows our store ≥ competitor on every metric in the plan
- [ ] Products, collections, pages, menus and discounts created as DRAFT/unpublished for owner review
- [ ] Theme committed to git; the owner has the preview link and a Vietnamese to-do list
