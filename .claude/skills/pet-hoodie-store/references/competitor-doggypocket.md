# Competitor: doggypocket.com (teardown from screenshots)

> **Status: from the owner's 15 mobile screenshots (Nov 2026).** The cloud
> network blocked the domain, so the theme, apps, fonts and catalogue are
> unverified (❓). Run the capture once `doggypocket.com` is allowed:
> ```bash
> node .claude/skills/shopify-competitor-clone/scripts/capture_site.mjs https://doggypocket.com/ --pages 6
> ```
> The general design lessons are in
> `shopify-competitor-clone/references/brand-story-layout.md`. Describe them in
> our own words and never copy their text, photos or reviews.

## Snapshot
- Shopify (footer says "Powered by Shopify"); theme ❓
- **One-product brand store:** "Doggy Pocket Hoodie", sherpa fleece hoodie with a
  zipped front pouch and a round opening for the pet's head
- Colours seen: Black, Pink. Sizes ❓
- Price $55.00, compare-at $110.00 (−50%), "Halloween 50% off" countdown bar
- Audience: small-dog owners (brand name), but the FAQ talks about cats too

## Page flow (mobile)
1. Countdown announcement bar (espresso) → header with a serif wordmark
2. Gallery (4 images, dots) → rating pill "4.8 · 1,000 reviews" → serif title → price with % off → one-line pitch → colour pills
3. Statement headline (3 beats) on white
4. Three story steps: image + "Unzip …", "Tuck …", "Head out …" + one line each
5. Dark "As seen on TikTok" band with a 2×2 grid of in-cabin airplane photos
6. "What our customers say": rating pill + photo review cards (first name + initial)
7. Brown CTA band with a pet's-point-of-view line + "Get yours" pill button
8. FAQ (safety, max pet size 10 kg / 22 lb, how the zip works, order changes within 12 h)
9. Cream footer with a 3-word tagline

## Product facts they state (paraphrased; verify for our own product)
| Fact | Their claim | Our action |
|---|---|---|
| Material | Sherpa outside, cozy pouch | Check our supplier spec. Cuddle Hoodie is polyester fleece |
| Opening | Curved/horizontal zip above a round, stretchy head opening | Describe our own opening from the product |
| Max pet | 10 kg / 22 lb | **Don't copy.** Ask the supplier for our real limit |
| Changes | Size/colour swap within 12 h if unshipped | Ours is better: 30-day guarantee + size help |

## What makes it work (keep the pattern)
- Calm, editorial brand look: serif headlines, cream/espresso/brown palette, pill UI, rounded photos
- Every photo shows the pet's face in the pouch; white-studio and real-life shots alternate
- Short, rhythmic copy; one idea per screen; consistent voice down to the footer
- Story steps explain the mechanism (open → settle → go) without a feature list

## Weak spots we beat
| Theirs | Risk | Suzeno |
|---|---|---|
| Hard-coded 4.8 / 1,000 reviews; reviewer photos look like the same models as the product shots | Fake reviews (FTC, Meta ads) | Judge.me real reviews only, hidden until we have them |
| "As seen on TikTok: Real … moments" with staged-looking cabin scenes | Misleading UGC claim; airlines restrict pets in the cabin | Lifestyle grid titled honestly; no airplane use claims |
| Permanent 50% off + rolling holiday countdown | Fake urgency and reference pricing | Real Christmas cut-off by country (already built), honest pricing, Buy 2 save $10 |
| "Is it safe? Yes." | Absolute safety claim | Safe-cuddles guidance (support from below, never unattended) |
| Dog brand but "your cat" in the FAQ | Sloppy copy | Consistent pet wording |
| No visible shipping/tax info in the screenshots ❓ | Checkout surprise | Free worldwide shipping, taxes and duties included, delivery ETA by country |
| Size guide not seen ❓ | Returns | Size table in cm/in + EU/US/UK conversion |

## Suzeno mapping (Cuddle Hoodie page)
statement → `story-steps` (open pouch, settle your cat, cuddle up) → designs →
`photo-grid` (Holiday moments, using our lifestyle images) → Judge.me reviews →
CTA band → FAQ. See `brand-story-layout.md` §2.
