# brand/brand.json reference

Start from `templates/brand.example.json`. Keys marked **required** must be filled;
everything else is optional and its section disappears when the key is missing or `null`.
Text that customers see is written in the store's market language (usually English).
Strings may contain simple HTML (`<p>`, `<ul><li>`, `<a href>`, `<strong>`).

## brand (required)
| Key | Example | Notes |
|---|---|---|
| `name` **required** | `"Brewly"` | Shown in comparison table and footer |
| `tagline` | `"Café-quality coffee…"` | Theme "brand headline" (footer) |
| `description` | `"Simple pour-over sets…"` | Footer brand text |
| `support_email` **required** | `"support@brewly.com"` | Must be a mailbox the owner reads |
| `reply_time` | `"within 1 business day"` | Only promise what the owner can keep |

## colors (required)
Hex codes. Five colour schemes are generated from them:

| Scheme | Background | Used for |
|---|---|---|
| scheme-1 | `background` | Main sections, product page |
| scheme-2 | `surface` | Alternate sections (so the page has rhythm) |
| scheme-3 | `dark` + `dark_text` | Announcement bar, closing banner, newsletter |
| scheme-4 | `accent` + `accent_text` | Spare, for highlights |
| scheme-5 | `primary` + `primary_text` | Sale badges |

Buttons use `primary` / `primary_text`. Contrast: `text` on `background` and on `surface`
≥ 4.5:1, `primary_text` on `primary` ≥ 4.5:1, `dark_text` on `dark` ≥ 4.5:1.
See `design-system.md` for palettes per niche mood.

## fonts
Shopify font library handles: `<family>_<style><weight>`, e.g. `lora_n7`, `nunito_sans_n4`,
`quicksand_n7`, `montserrat_n6`, `playfair_display_n7`, `dm_sans_n4`, `assistant_n4`,
`work_sans_n4`, `josefin_sans_n6`, `cormorant_n6`, `poppins_n6`, `karla_n4`.
Unknown handles fall back to the default font; check in the theme editor
(Theme settings → Typography) after the first push and pick visually if needed.

## style
| Key | Values |
|---|---|
| `radius` | `rounded` (friendly: pets, kids, food) · `soft` (default for most) · `sharp` (luxury, fashion, tech) |
| `heading_scale` / `body_scale` | 100–150 / 100–130 |
| `page_width` | 1000–1600 |

## announcements
List of 1–3 short lines for the rotating top bar. Only true offers.

## hero (required: heading, text)
`image` (file name from Admin → Content → Files, empty = text-only hero), `heading`, `text`, `button`,
`link` (default: the product page; multi-product stores use `/collections/all`).
Best hero image: wide 16:9 or 3:2 lifestyle photo, product in use, no text baked in.

## product (required: handle)
| Key | Notes |
|---|---|
| `handle` **required** | Product URL handle, e.g. `brewly-pour-over-set` (→ /products/brewly-pour-over-set). Never use ™ or accents |
| `button_label` | Sticky bar button |
| `bullets` | 3–5 benefit lines under the title (an emoji at the start is fine) |
| `tabs` | `[{heading, icon, content}]` collapsible tabs: what's in the box, size/specs, shipping, guarantee, care |
| `description` | `true` adds each product's own description (from Shopify Admin) under the title. Use for multi-product stores, where `bullets` would be the same on every product |
| `dynamic_checkout` | `true` shows Shop Pay/PayPal buttons (off by default: they skip the bundle picker) |

## bundle
| Key | Notes |
|---|---|
| `enabled` | `false` → normal price + variant buttons + quantity |
| `heading`, `save_label` | Texts |
| `default_tier` | 1–3, usually 2 (the anchor) |
| `discount_type` | `amount` = `$discount` off **each unit**; `percent` = `discount`% off the tier total |
| `tiers` | Up to 3 × `{qty, discount, label, sublabel, badge, perks}`; `qty` 0 hides a tier |

Pricing rule of thumb: tier 2 saves 10–15 %, tier 3 saves 20–25 %, never below landed cost + ad
cost per order. Create the matching automatic discounts (one per tier with discount > 0).

## delivery
| Key | Notes |
|---|---|
| `enabled` | Show the estimate under Add to cart |
| `free_shipping` | `true` → "Free shipping to {country}", `false` → "Ships to {country}" |
| `default` | `{min, max}` days for every country without a rule |
| `rules` | `[{countries: ["US"], min, max}]`, first match wins. `"AFRICA_SOUTH_AMERICA"` is a built-in list of slow countries |
| `note` | Second line, e.g. `"All taxes & import duties included"`. Only if true |
| `payment_icons` | Show the store's payment icons |

Days = supplier's delivery window + 2–3 days buffer. Keep identical to the Shipping policy page.

## trust
Exactly 3 × `{icon, text}`. Valid icons: apple banana bottle box carrot chat_bubble check_mark
clipboard dairy dairy_free dryer eye fire gluten_free heart iron leaf leather lightning_bolt
lipstick lock map_pin nut_free pants paw_print pepper perfume plane plant price_tag
question_mark recycle return ruler serving_dish shirt shoe silhouette snowflake star
stopwatch truck washing. (Same list for `product.tabs[].icon`.)

## Content sections (all optional)
| Key | Shape | Where |
|---|---|---|
| `how_it_works` | `{heading, steps: [[title, text], …]}` 3–4 steps | Product, home, /pages/how-it-works |
| `benefits` | `{heading, items: [[title, text], …]}` 3–4 items | Product, home, about |
| `comparison` | `{heading, us_label, them_label, rows: [[feature, us_bool, them_bool]]}` | Product. Compare to a *category* ("pod machines"), never a named brand |
| `stories` | `[{image, heading, text, layout: image_first/text_first, button?}]` | #1–2 product page, #3+ home |
| `size_guide` | `{heading, intro, columns: [4 headers], rows: [[4 values]], note}` | Product |
| `faq` | `[[question, answer], …]` 6–12 | Product, /pages/faq, home subset |
| `closing` | `{heading, text}` | Dark banner near the bottom |
| `home` | `{featured_text, featured_button, faq_indexes: [0,1,3], featured_product: true, collection: {handle, heading, count}}` | Home page. `collection` adds a product grid (handle `all` = every product); `featured_product: false` hides the single-product block |
| `newsletter` | `{heading, text, welcome_code?, code_label?}` | Home. Create the code in Shopify first |
| `header` | `{country_selector: true}` | Needed for the per-country delivery estimate |

## Pages the owner/agent must create in Shopify
The templates exist, but the pages must be created (connector `pageCreate` or Admin → Pages)
with the matching template: About (`page.about`), FAQ (`page.faq`), How it works
(`page.how-it-works`), plus Contact (`page.contact`) and policy pages.
