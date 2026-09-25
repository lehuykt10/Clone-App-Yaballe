# Competitor: huggiecat.com (partial teardown)

> **Status: PARTIAL.** Built from public search-engine snippets (Sept 2026)
> because the session's network policy blocked huggiecat.com. When the
> domain is allowed, run the full capture and complete this file:
> ```bash
> node .claude/skills/shopify-competitor-clone/scripts/capture_site.mjs \
>   "https://huggiecat.com/products/pet-tote-carier-hoodie" --pages 6
> ```
> Items marked ❓ are unverified. Describe patterns in our own words and never copy their text.

## Snapshot
- Platform: Shopify (product URL pattern `/products/…?variant=…`); theme ❓
- Model: **one-product store**. Hero product is a fleece hoodie with a front
  pouch that carries a cat or small dog
- Secondary competitor in the same niche: thehuggiez.com ("Huggiez" pet hoodie)
- Mass-market alternatives: Amazon, Etsy, Walmart and eBay listings for "cat carrier hoodie"
  (price anchor for shoppers who compare)
- Price, compare-at price, variants (sizes/colours) ❓ capture `/products.json`

## Positioning and messaging angles (paraphrased)
| Angle | How they use it |
|---|---|
| Emotional closeness | Pet rides against your chest and feels your warmth and heartbeat |
| Comfort / safety | Padded pouch spreads weight evenly; open top so the pet can breathe and see you |
| Freedom | Stretchy opening, so the pet can climb in and out on its own |
| Capacity | Fits pets up to ~9 kg / 20 lb (cats, kittens, small dog breeds) |
| Material | Thick, double-sided brushed polar fleece |
| Dual use | Pouch works as a big kangaroo pocket when the pet isn't in it |
| Use case from reviews | Taking a carrier-hating cat to the vet |

## Offer and trust (from snippets)
- Free worldwide shipping
- 30-day satisfaction guarantee
- "Vet-approved comfort" claim ⚠️ (we must NOT make this claim unless the owner has a real vet endorsement in writing)
- "3,500+ 5-star reviews" social-proof counter ❓ (verify what review app is used)
- Review snippets are short and emotional (value for money, vet trips)

## Gaps we can likely beat ❓ (confirm with capture)
- Product title typo ("Carier") → weak SEO and trust. Use correct keywords: *cat carrier hoodie*, *pet pouch hoodie*
- Unverified health/vet claims → we use substantiated claims only (materials, weight limit, washing)
- Probably generic one-product theme → faster, cleaner custom Dawn build
- Sizing uncertainty is the #1 objection for apparel + pets → size guide showing human size **and** pet weight
- Safety education (how to put pet in, max time, when not to use) is rarely shown → a "How it works" + safety section
- Gifting angle (pet-parent gifts, holidays) → gift bundle / 2-pack
- Matching items (human + pet) and colour choice → variant swatches

## To fill after full capture
- Section order for home / PDP / cart (report.md tables)
- Apps (reviews, upsell, pop-up), tracking scripts
- Performance: mobile LCP, CLS, page weight
- Price, bundles, compare-at, discount mechanics, free-shipping threshold
- Screenshots: gallery style, colour palette, typography
