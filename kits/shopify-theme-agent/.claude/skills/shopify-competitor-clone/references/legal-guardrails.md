# ⚖️ Legal guardrails: what can be "cloned"

Copying a competitor's **ideas, layout and business model** is normal
competition. Copying their **creative work or brand identity** is copyright or
trademark infringement. It can get the store taken down (DMCA notices to
Shopify), ad accounts banned, and payment processors frozen.

## ✅ OK to reproduce

| What | Example |
|---|---|
| Page structure and section order | Hero → benefits → social proof → PDP-style featured product → FAQ |
| UX patterns | Sticky add-to-cart, quantity-break bundles, drawer cart, mega menu |
| Offer mechanics | "Buy 2 get 1", free-shipping threshold, 30-day guarantee |
| Pricing strategy | Price points, compare-at logic, bundle discounts (use your own numbers) |
| Information architecture | Which collections exist, which policies/pages exist, nav depth |
| Functionality | Same *kind* of app (reviews, upsell), installed and configured yourself |
| Generic facts | Product specs, materials, dimensions (facts are not copyrightable) |

## ❌ Never copy

| What | Do instead |
|---|---|
| Text: headlines, descriptions, FAQ answers, About story, policies | Write original copy from the product facts and brand voice |
| Images, videos, GIFs, icons, illustrations | Owner's own photos, supplier images the owner has rights to, licensed stock, AI-generated originals |
| Logo, brand name, slogans, look-alike names/domains | New brand identity; check trademarks (USPTO/EUIPO/WIPO) before committing |
| Customer reviews and testimonials | Collect real reviews only (Judge.me, etc.). **Never** import or invent reviews (FTC rule 2024 bans fake reviews) |
| Theme or app source code (Liquid/CSS/JS) from their site | Build on Dawn (MIT-licensed) or a theme the owner bought |
| Trade dress that makes buyers think it's the same brand | Visibly different palette, typography and photo style |
| Claims you can't back up ("#1 in USA", "clinically proven", "as seen on") | Only claims the owner can substantiate |

## Scraping etiquette

- `capture_site.mjs` loads each page once per viewport. Don't loop it or crawl the whole site.
- Captured data (screens, report.json) is for internal analysis. Don't publish it.
- `/products.json` is used for price and assortment analysis only. Never bulk-import competitor products.

## If the owner insists on copying assets

Explain in Vietnamese, briefly: "Sao chép chữ/ảnh/logo của đối thủ có thể bị
DMCA gỡ store, khóa tài khoản quảng cáo và cổng thanh toán. Mình sẽ giữ bố
cục và chiến lược bán hàng, còn nội dung và hình ảnh làm mới cho thương hiệu
của anh/chị." Then continue with original assets.
