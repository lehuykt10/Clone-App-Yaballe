# Store blueprint: one-product pet carrier hoodie store

Target: US/UK/CA/AU pet parents (mostly cat owners, 20–45, gift buyers in Q4).
Theme: Dawn + this skill's sections. Language: English.

## Sitemap
| Page | Template | Notes |
|---|---|---|
| Home | `index.json` | Sells the one product; every CTA goes to the PDP |
| Product | `product.json` | The money page. Most effort goes here |
| Collection "Shop all" | `collection.json` | Hoodie + accessories/gift bundle |
| About | `page.about.json` | Real brand story, who's behind it |
| FAQ | `page.faq.json` | `faq-accordion` (same Q&A as PDP plus more) |
| Size guide | `page.size-guide.json` | `size-guide` section |
| Contact | `page.contact.json` | Dawn contact form, email, response time |
| Track order | page + app (e.g. 17TRACK/ParcelPanel) | Cuts "where is my order" emails |
| Policies | Shopify policies | Shipping, refund, privacy, terms |

## Product page (PDP): section order
1. **Announcement bar**: free shipping + guarantee (1 rotating message on mobile)
2. **main-product** blocks, in this order:
   - title → rating (reviews app block) → price
   - short benefit bullets (3 × `icon-with-text` or `text`)
   - `variant_picker` (buttons/swatches: Colour, Size)
   - "Size guide" link (`popup` block → size-guide page)
   - **`quantity_breaks`** (1 / 2 −10% / 3 −15%; remove `quantity_selector`)
   - `buy_buttons` (dynamic checkout on)
   - trust row (`icon-with-text`: free shipping · 30-day returns · secure checkout)
   - `collapsible_tab` × 4: Details & materials · Sizing · Shipping · Returns
3. **Image with text / multicolumn**: "How it works" in 3 steps (step in → zip/adjust → go)
4. **Benefits grid** (from shopify-competitor-clone section template)
5. **Video / UGC**: owner's own clips of real pets
6. **comparison-table**: Us vs "Regular pet carrier"
7. **Reviews widget** (Judge.me full widget)
8. **faq-accordion**: 6–8 questions
9. **Related / complementary products**
10. **sticky-atc** (enabled on mobile + desktop)

## Home: section order
1. Hero (image banner): emotional lifestyle photo, 1 headline, 1 CTA to the PDP
2. Social-proof strip (rating + review count, only when real)
3. Featured product (Dawn `featured-product`): buy from home
4. Benefits grid
5. How it works (3 steps)
6. UGC / testimonials (real only)
7. Comparison table
8. FAQ (4 questions) + link to full FAQ
9. Newsletter (10% off first order)

## Beat-them targets (verify in Phase 7 scorecard)
| # | Improvement | Target |
|---|---|---|
| 1 | Speed | Mobile LCP < 2.5s, CLS < 0.1, ≤ 5 third-party scripts |
| 2 | Correct, keyword-rich title/handle | `cat-carrier-hoodie`; title contains "Cat Carrier Hoodie" |
| 3 | Size certainty | Size guide with human size + pet weight, linked next to variant picker |
| 4 | Bundles | Quantity breaks with a real automatic discount |
| 5 | Mobile conversion | Sticky ATC, swatches, tap targets ≥ 44px |
| 6 | Safety education | "How it works" + "Safe use" FAQ (weight limit, supervision, breaks) |
| 7 | Honest claims | No "vet-approved"/medical claims without written proof |
| 8 | Rich results | Product + FAQPage + Organization JSON-LD, 100% image alt text |
| 9 | Gifting | Gift note, gift bundle, Q4 banner |
| 10 | Post-purchase | Order tracking page + branded notification emails |
| 11 | Distinct brand | Own palette/typography/photo style; screenshots side by side look different |
| 12 | Accessibility | Contrast ≥ 4.5:1, keyboard-usable accordions/drawer |

## Discounts for quantity breaks
The `quantity_breaks` block only **displays** prices. Create matching automatic
discounts (GraphQL, via the Shopify connector: `graphql_schema` → validate → mutate):
```graphql
mutation($d: DiscountAutomaticBasicInput!) {
  discountAutomaticBasicCreate(automaticBasicDiscount: $d) {
    automaticDiscountNode { id } userErrors { field message }
  }
}
# Tier 2: { "title": "Bundle 2 - 10% off", "startsAt": "<ISO now>",
#   "minimumRequirement": { "quantity": { "greaterThanOrEqualToQuantity": "2" } },
#   "customerGets": { "value": { "percentage": 0.10 }, "items": { "products": { "productsToAdd": ["gid://shopify/Product/…"] } } } }
# Tier 3: same with quantity "3", percentage 0.15
```
Shopify applies only the best automatic discount by default, so tier 3 wins at qty ≥ 3.
Confirm the start date and combinations with the owner, then test in the cart.

## Copy angles (write originally, English)
- Closeness: "they nap on your chest, you get on with your day"
- Freedom from carriers: vet visits, errands, walks around the block, stress-free
- Comfort facts: fleece weight (gsm), pouch dimensions, max pet weight, washing instructions
- Dual use: oversized front pocket when the pet is not in it
- Gift: "for the person whose pet is their whole personality"
Never reuse competitor sentences. Avoid health or anxiety-cure claims.

## Compliance
- Real reviews only (FTC rule on fake reviews, 2024). Import reviews only from the owner's own supplier or marketplace listings, with permission
- Safety note: supervise pets, max weight, not for use while driving/cycling
- Product photos: the owner's own shoots, or supplier images with written permission
- Shipping times must match what the supplier can actually deliver
