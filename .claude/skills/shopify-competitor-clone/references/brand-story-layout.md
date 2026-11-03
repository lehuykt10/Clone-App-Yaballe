# Brand-story layout: making a store look like a real brand

Reference pattern taken from **doggypocket.com** (teardown of the owner's mobile
screenshots, Nov 2026; the site was blocked from the cloud session, so fonts and
colours are estimated). Use it in Phase 2 (plan), 3 (brand system) and 5 (build)
whenever the owner says a competitor "looks like a real brand" or wants a
premium, editorial feel instead of a busy dropshipping page.

Copy the **structure and design principles** below. Never copy their copy,
photos, reviews or brand name (`legal-guardrails.md`).

---

## 1. Why it reads as a brand (the 8 rules)

| # | Rule | What it looks like |
|---|---|---|
| 1 | **One idea per screen** | Each mobile screen holds one headline, one image and at most two lines of text. No stacked badges, icon rows or banners. |
| 2 | **Big editorial serif + quiet sans** | High-contrast display serif for every heading (H1 ≈ 44–56px on mobile), a humanist sans for body text with loose letter-spacing and ~1.7 line height. |
| 3 | **Restrained palette** | White, a warm cream, a deep espresso and one mid brown. No red sale badges, no bright greens or stickers. Stars use the brand brown, not yellow. |
| 4 | **Rhythmic micro-copy** | Three-beat headlines ("One X. One Y. Anywhere."), verb-first step titles, one-sentence body lines. The brand voice repeats in the footer tagline. |
| 5 | **Consistent photography** | The same few models and product colours throughout: white-studio shots alternating with real-life shots. The pet's face is always visible, and the product is always shown in use. |
| 6 | **Soft geometry** | Rounded image corners (~12px), pill-shaped buttons, rating badge and colour swatches. Images run full width inside a 16–20px gutter. |
| 7 | **Generous whitespace** | 64–96px between sections on mobile, and a lot of white above and below headlines. |
| 8 | **Few elements, many repeats** | The same 4–5 components (statement, image + caption, photo grid, review card, CTA band) repeat down the page, so it feels designed rather than assembled. |

## 2. Page blueprint (product page = landing page)

The competitor runs a one-product store where the product page and the home
page are effectively the same long landing page. Section order, top to bottom:

| # | Section | Content pattern | Dawn / our section |
|---|---|---|---|
| 0 | Announcement bar | Dark espresso bar, one offer line | Dawn announcement bar. **Only a real, dated deadline** (see §5) |
| 1 | Header | Hamburger, serif wordmark, search, account and cart icons | Dawn header, logo as text in the heading font, or an SVG wordmark |
| 2 | Gallery | Full-width image with dot pagination, about 4 images | `main-product`, `gallery_layout: thumbnail_slider`, `mobile_thumbnails: hide` (shows dots) |
| 3 | Rating pill | Cream pill: stars + "x.x rating based on N reviews" | Judge.me star badge block, styled as a pill. **Real numbers only** |
| 4 | Title + price | Huge serif title; price, compare-at price, % off | Dawn title + price blocks |
| 5 | One-line pitch | One sentence: material + feature + emotion | Text block |
| 6 | Options | Pill buttons for colour and size | Dawn variant picker `picker_type: button` |
| 7 | Buy | Full-width pill ATC | Bundle picker + buy buttons, delivery ETA, payment icons |
| 8 | Statement | 3-beat serif headline on white, nothing else | Dawn `rich-text`, heading h0, left-aligned |
| 9 | Story steps | 3× (rounded image → H2 step title → one line). Verb-first: open, settle, go | **`templates/brand-story/story-steps.liquid`** |
| 10 | Social photo grid | Dark section, icon + heading + one line, 2×2 portrait grid | **`templates/brand-story/photo-grid.liquid`** |
| 11 | Reviews | Heading, rating pill (white inside brown), cards with photo left and stars + quote + first name and initial | Judge.me "Cards" or "Testimonials" widget (real reviews only) |
| 12 | CTA band | Mid-brown full-width band, centred 3-line serif line, white pill button | Dawn `rich-text` with a brown colour scheme + button block |
| 13 | FAQ | Centred heading, 4–6 short Q&As covering safety, pet size, how it works, order changes | `faq-accordion` (with FAQPage JSON-LD) |
| 14 | Footer | Cream, brand tagline as H2 + one line, minimal links, round back-to-top button | Dawn footer with a brand-info block |

For a multi-product store (e.g. Suzeno), use this blueprint on the **hero
product page** and a shorter version on the home page:
statement → story steps → hero product → photo grid → reviews → CTA band → FAQ.

## 3. Design tokens (estimated from screenshots; build our own variant)

| Token | Competitor (approx.) | Rule for our brand |
|---|---|---|
| Text / dark section | espresso `#2A1D16` | Keep a very dark warm neutral, never pure black |
| Brand mid | brown `#5A3D27` | One brand colour. Choose a different hue for our brand |
| Surface | cream `#F2EAE3` | Warm off-white for cards, pills and the footer |
| Base | `#FFFFFF` | |
| Stars / accents | `#8A5A3B` | Stars in the brand colour, not yellow |
| Heading font | High-contrast display serif (DM Serif Display style) | Shopify font library: Playfair Display, Lora or Fraunces. Pick a **different** one from the competitor |
| Body font | Humanist sans (Karla style), ~0.04em tracking | Shopify font library: Karla, Work Sans, Figtree |
| Radius | ~12px images, 999px buttons and pills | |
| Buttons | Solid dark pill; white pill on dark bands | Dawn: button radius 40, border 0 |

Contrast check: body text on cream must be ≥ 4.5:1. Their grey-brown body text
is borderline, so make ours darker.

Dawn settings (`config/settings_data.json`):
- 4 colour schemes: white base, cream, espresso (text white), brand mid (text white)
- `type_header_font`: the serif; `heading_scale` 130–150
- `type_body_font`: the sans; `body_scale` 100–110
- `buttons_radius` 40
- `media_radius` 12
- `card_corner_radius` 12

## 4. Copy rules (write our own)

- **Headline formula:** 3 short beats that describe the product's job, e.g.
  "One pouch. One purr. All day."
- **Step titles:** verb + object, 2–4 words; body lines under 12 words.
- **Pitch line:** material → feature → emotional payoff, in one sentence.
- **CTA band:** speak from the pet's point of view, plus a 2-word button
  ("Get yours", "Bring them").
- **Footer tagline:** 3 words that sum up the brand promise.
- **Pet wording:** decide "cat", "dog" or "pet" and keep it consistent. The
  competitor sells to dog owners but its FAQ says "your cat climbs in".

## 5. Do NOT copy: their trust problems are our advantage

| Competitor pattern | Why not | Do this instead |
|---|---|---|
| Hard-coded "4.8 stars · 1,000 reviews" pill on a new store | Fake social proof (FTC rule on fake reviews, Meta ad policy) | Judge.me badge showing real counts; hide it until there are reviews |
| Reviewer photos that are the same models as the product shots | Fabricated reviews | Only real customer reviews, imported or collected via Judge.me |
| "As seen on TikTok: Real … moments" with staged, AI-looking cabin scenes | Misleading claim of real UGC/endorsement | Heading like "Made for moments like these" for lifestyle shots; "From our customers" only with real, permitted photos |
| Rolling "Halloween 50% off" countdown + permanent 2× compare-at price | Fake urgency and reference pricing (FTC/EU Omnibus/UK CMA) | Real deadlines only (e.g. the Christmas cut-off by country); compare-at only if it was a genuine selling price |
| "Is it safe? Yes." absolute claim, pets on planes | Liability; airlines have cabin-pet rules | Safety guidance tab: support from below, short sessions, never unattended; no airline claims |
| Change window "within 12 hours" only | Weak policy | 30-day guarantee, size-exchange help |

## 6. Build checklist

- [ ] Colour schemes and fonts set in `settings_data.json` (differ from the competitor)
- [ ] Install `story-steps` and `photo-grid` from `templates/brand-story/` into `theme/sections/`
- [ ] Hero product template follows §2 order; JSON content holds all copy
- [ ] Every image the same aspect family (portrait 4:5 for steps and grid, square for the gallery) and the same photo style
- [ ] Rating pill and reviews only from a real review app
- [ ] Mobile check at 375px: one idea per screen, no horizontal scroll, headings ≤ 3 lines
- [ ] `shopify theme check`: no new offenses
