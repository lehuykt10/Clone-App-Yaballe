---
name: store-policies
description: Write and publish the legal/customer policies a Shopify store needs to pass Meta (Facebook/Instagram) ads review, Google Merchant Center and payment-provider checks - Refund, Shipping, Terms of Service, Contact information (+ Shopify's Privacy policy) - consistent with the store's real settings, plus a compliance checklist. Use for "chính sách", "policy", "refund/shipping policy", Merchant Center "misrepresentation" or ads rejected for "unacceptable business practices".
---

# Store policies (Meta + Google compliant)

Templates in `templates/` are complete, plain-English policies with `{{PLACEHOLDERS}}`.
Fill every placeholder from the **real** store settings and supplier facts. A policy that
contradicts the store (e.g. says "free shipping" while checkout charges $4.99) is the #1
cause of Merchant Center "Misrepresentation" suspensions.

## Step 1. Collect the facts (ask the owner in Vietnamese, don't guess)
| Placeholder | Question |
|---|---|
| `{{BRAND}}`, `{{DOMAIN}}` | Brand name, domain |
| `{{LEGAL_NAME}}`, `{{COUNTRY}}`, `{{BUSINESS_ADDRESS}}` | Registered business / owner name, country, real address (Google requires a physical address or at least full contact info) |
| `{{SUPPORT_EMAIL}}`, `{{SUPPORT_HOURS}}` | Mailbox the owner reads; hours + timezone |
| `{{CURRENCY}}` | Store currency, e.g. "US dollars (USD)" |
| `{{PROCESSING_DAYS}}` | Days to hand over to carrier, e.g. "1–3" |
| `{{DELIVERY_TABLE_ROWS}}` | One `<tr><td>Region</td><td>X–Y days</td></tr>` per region; = supplier time + 2–3 days; identical to brand.json `delivery` |
| `{{SHIPS_FROM}}` | e.g. "in China", "in the US". If it ships from a local warehouse, delete "so delivery takes longer than a local shop" |
| `{{SHIPPING_COST_TEXT}}` | Free everywhere? threshold? rates? Must match Settings → Shipping and delivery exactly |
| `{{TAXES_SECTION}}` | See below |
| `{{GUARANTEE_DAYS}}` | Usually 30 |
| `{{RETURN_SHIPPING_RULE}}` | Who pays return shipping for change-of-mind returns |
| `{{HYGIENE_OR_CUSTOM_EXCEPTION}}` | e.g. opened cosmetics, personalised items, used consumables: "`<p>…can only be refunded if damaged or defective.</p>`", or empty |
| `{{PRODUCT_SAFETY_PARAGRAPH}}` | 1 paragraph of safe-use warnings for the niche (see niche-playbooks), or empty |
| `{{TAXES_SENTENCE}}` | Terms §4, matches the taxes section |
| `{{LAST_UPDATED}}` | Today's date |

`{{TAXES_SECTION}}` options (pick the TRUE one):
- **Duties & taxes included** (DDP, or supplier/marketplace collects VAT/IOSS, owner confirmed):
  `<p>All our prices <strong>include all taxes and import duties</strong> … nothing extra to pay on delivery.</p><p>If a carrier ever asks you to pay a fee for your order, please don't pay it. Contact us … and we'll take care of it.</p>`
- **Not included:** `<p>Orders may be subject to import duties and taxes (such as VAT/GST) set by your country. Unless shown as included at checkout, these are paid by the customer to the carrier or customs on delivery.</p>`
- **Shopify collects duties at checkout** (Markets duties enabled): say they are calculated and paid at checkout.

## Step 2. Publish
1. Pages: create one page per policy (connector `pageCreate`, or Admin → Online Store →
   Pages), handles `refund-policy`, `shipping-policy`, `terms-of-service`, `contact-information`.
   Also a `track-order` page (the shipping policy links to it).
2. Settings → Policies: the owner pastes each HTML (click `<>` Show HTML first). The
   connector cannot write this (no `write_legal_policies` scope). Privacy policy: keep
   Shopify's auto-generated one, check the store contact email.
3. Footer menu: link all policies + Contact + Track order (`menuUpdate` or Admin → Navigation).

## Step 3. Compliance checklist (Meta ads, Google Merchant Center, payments)
- [ ] Contact info visible: email + address (+ phone optional) on Contact page and footer
- [ ] Refund/return policy: window, condition, who pays shipping, refund timeline, how to start
- [ ] Shipping policy: processing time, delivery times per region, costs, tracking, lost parcels
- [ ] Policies match checkout (shipping price, countries, currency, taxes) and product pages
- [ ] Store not password-protected; checkout works; payment method active
- [ ] Prices: no fake compare-at, no "was $99" never charged; sale end dates real
- [ ] No fake reviews, no fake scarcity/countdown, no invented "as seen on"
- [ ] No prohibited claims for the niche (niche-playbooks Red flags)
- [ ] Product images and descriptions original (not the competitor's)
- [ ] About page tells who runs the store (Google checks transparency)
- [ ] Merchant Center: shipping & returns set in Merchant Center identical to the policies
- [ ] Domain email (support@brand.com) instead of Gmail for trust

Report remaining items to the owner as a Vietnamese checklist.
