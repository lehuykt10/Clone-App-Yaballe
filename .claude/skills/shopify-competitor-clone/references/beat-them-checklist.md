# 🏆 Beat-them checklist

Score the competitor 0–5 per area in Phase 2, then verify our store in
Phase 7. Our store must match or beat them in every area and hit every target
marked 🎯.

## 1. Speed (biggest, easiest win: most dropship stores are slow)
- 🎯 Mobile LCP < 2.5s, CLS < 0.1 (capture script; confirm with PageSpeed Insights once live)
- 🎯 Home transfer < 1.5 MB, ≤ 5 third-party scripts
- Hero image: `image_url: width:` with `srcset`/`sizes`, `fetchpriority="high"`, **no** lazy-load on the LCP image
- All other images `loading="lazy"`, explicit width/height (prevents CLS)
- No autoplay video above the fold on mobile (poster image instead)
- Uninstall/avoid apps that inject heavy JS; prefer theme-native sections (bundles, sticky ATC, FAQ, badges)
- Fonts: max 2 families, `font_display: 'swap'`, preload the heading font

## 2. Mobile UX
- Sticky add-to-cart bar on PDP
- Thumb-reachable CTAs, tap targets ≥ 44px
- Variant picker as buttons/swatches, not dropdowns
- Drawer cart with free-shipping progress bar
- No horizontal scroll at 390px; test screenshots from the capture script

## 3. Trust
- Real reviews app (Judge.me/Loox) with photo reviews once collected, never fake
- Clear shipping times and returns on PDP (collapsible rows), not only in policies
- Guarantee badge the owner actually honours
- About page with a real brand story, contact email, business address/country
- Payment icons, secure checkout note, working contact page

## 4. Offer / CRO
- One clear hero offer above the fold
- Quantity breaks or bundles (theme section, not a heavy app)
- Benefit-led PDP: problem → solution → how it works → proof → FAQ → CTA
- Comparison section ("Us vs typical alternatives", no competitor names)
- Email/SMS capture with a real incentive, delayed ≥ 15s or on exit intent
- Upsell in cart drawer (1 complementary product)

## 5. SEO
- Unique title (≤ 60 chars) + meta description (≤ 155) per product/collection/page
- One H1 per page; logical H2/H3
- JSON-LD: Product (with offers, aggregateRating when real), Organization, BreadcrumbList, FAQPage
- Descriptive alt text on 100% of images
- Clean handles, collection descriptions, internal links
- Blog: 3 starter articles targeting buyer-intent keywords (optional)

## 6. Accessibility
- Text contrast ≥ 4.5:1 (buttons included)
- Visible focus states, keyboard-usable menus and drawer
- Form labels, `aria-label` on icon buttons, `lang` attribute

## 7. Brand distinctiveness (anti-copy check)
- Palette, fonts, logo and photo style clearly different from competitor
- Side-by-side screenshots: a shopper would not confuse the two brands
- No competitor phrases, names or images anywhere (search the theme: `grep -ri "<competitor name>"`)

---

## 🚀 Launch checklist (owner + Claude)
- [ ] Payments active (Shopify Payments / PayPal), test order placed and refunded
- [ ] Shipping zones and rates match the promises on PDP
- [ ] Taxes configured for target markets
- [ ] Policies: refund, privacy, terms, shipping, contact info (Settings → Policies)
- [ ] Custom domain connected, primary domain set, SSL active
- [ ] Google & YouTube channel, Meta channel, Google Search Console + sitemap
- [ ] Analytics / pixels (only the ones actually used)
- [ ] Email notifications branded (logo, colours)
- [ ] Favicon, social share image (og:image)
- [ ] 404 page, search results page styled
- [ ] Products moved DRAFT → ACTIVE (`bulk-update-product-status`) after owner review
- [ ] Theme published, password page removed
- [ ] Final capture of live site → `teardown/scorecard.md` updated
