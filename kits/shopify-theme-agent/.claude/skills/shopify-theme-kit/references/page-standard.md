# Standard one-product layout (home + product page)

The layout proven on a live one-product store (pet pouch hoodie, Nov 2026), modelled on
the best competitor pages but with **honest** social proof. Use it for any single hero
product. All sections below are installed by `install_kit.py` and can be added or
re-ordered in the theme editor (Customize → Add section).

## 1. Product page, top to bottom

| # | Block / section | File | Notes |
|---|---|---|---|
| 1 | Gallery | Dawn `main-product` | `gallery_layout: thumbnail_slider`, `hide_variants: false`, `image_zoom: none`. One photo per colour, linked to that colour's variants |
| 2 | Title | Dawn | Short brand-like name, 2 words |
| 3 | Stars + "4.7 · 12 reviews" | `snippets/review-summary.liquid` (custom_liquid block) | Computed from real reviews; hidden when there are none |
| 4 | Price | Dawn | Compare-at price only if it was really sold at that price |
| 5 | One-line pitch | Dawn text block | Material → feature → feeling, one sentence |
| 6 | Holiday cut-off line | custom_liquid | Real dates by country, hidden after the cut-off |
| 7 | Bundle picker 1 / 2 (/ 3) | `snippets/bundle-picker.liquid` | Per-unit colour + size; create the matching automatic discount |
| 8 | Add to cart | Dawn buy buttons | |
| 9 | Delivery timeline: Ordered → Order ready → Delivered | `snippets/delivery-timeline.liquid` | Edit the day ranges to match the shipping policy |
| 10 | Review quotes (photo, quote, name, stars) | `snippets/review-quotes.liquid` | First 3 real reviews; hidden when none |
| 11 | 3 trust icons | Dawn icon-with-text | 30-day guarantee · Secure checkout · Free shipping (only what is true) |
| 12 | Payment icons | custom_liquid | `shop.enabled_payment_types` |
| 13 | Description | Dawn | |
| 14 | Tabs | Dawn collapsible tabs + custom_liquid size table | Pet/size & weight (real max), Size guide (supplier cm + inches), Safety, Care, Shipping, Guarantee |
| 15 | Wave band "Made for two" | `sections/wave-feature.liquid` | Colour band with wavy top, framed photo, eyebrow, heading with one circled word |
| 16 | Video carousel | `sections/video-carousel.liquid` | Vertical 9:16 clips; hidden until a video is added. Never title it "as seen on TikTok/Instagram" unless true |
| 17 | How it works (3 steps) | `sections/benefits-grid.liquid` | Verb-first steps |
| 18 | Colour grid | Dawn multicolumn | One tile per colour → `/products/<handle>?variant=<id>`; `image_ratio` = ratio of the photos (portrait for 4:5) |
| 19 | Second wave band | `sections/wave-feature.liquid` | `image_right: true` for rhythm |
| 20 | "What our customers say" | `sections/review-cards.liquid` | Rating pill + photo cards from real reviews; hidden when none |
| 21 | FAQ | `sections/faq-accordion.liquid` | 6–8 questions incl. how it works, pet/size, delivery, taxes, returns |
| 22 | Sticky "Buy now" bar | `sections/sticky-atc.liquid` | |

## 2. Home page (one-product store)
Hero image-with-text ("Your pet, closer." + button to the product) → benefits grid →
Dawn `featured-product` (title, review-summary, price, pitch, variant picker, buy
buttons, delivery timeline, link "See all details & bundle deal") → wave band →
video carousel → colour grid → review-cards (`product` setting = the handle) → FAQ →
newsletter (+ welcome code). **No other products, no cart upsell** on a one-product store.

Optional calmer variant: `sections/story-steps.liquid` (3 big images with step titles)
and `sections/photo-grid.liquid` (dark band, 2×2 lifestyle photos), see the
competitor-clone `brand-story-layout.md`.

## 3. Colours and images
- Add two schemes in `settings_data.json` when the brand needs them: a strong brand
  colour band (white text) for wave bands and the announcement bar, and a light tint for
  How it works / FAQ. Keep buttons in the brand colour.
- **Photos:** all product photos in **one ratio** (best 4:5, at least 1000 px wide,
  e.g. 1122×1402). Mixed ratios make the gallery jump. Replace a photo with
  `fileUpdate` (`originalSource`) to keep its file name, so theme references keep working.
- **Lifestyle photos** (wave bands, photo grid, hero): no text, stars or names baked in.
- Logo: horizontal PNG with transparent background, logo width 140–160 px; favicon
  512×512 square.

## 4. Social proof rules (non-negotiable)
- Reviews only from real buyers or people who got a free product (labelled). Typed by
  the owner in Content → Metaobjects → Customer review (see `shopify-competitor-clone/references/reviews-and-ratings.md`).
- Never: AI-made "customer" photos, names and quotes baked into images, hard-coded
  "4.8 · 1,000 reviews", "20+ orders in 24h", "2 people shopping now", fake countdowns,
  fake compare-at prices. US FTC fines these whatever the traffic source (ads or organic).
- If the owner sends review images with names/stars printed on them, do not upload them:
  explain why and offer to use the photos as lifestyle images once exported without text.

## 5. Working on a live store
- Never write to the published theme. Duplicate it (`themeDuplicate`), edit the copy,
  the owner publishes.
- Before overwriting a template on the copy, read the live one: the owner may have
  changed it in the theme editor (logo, settings, videos). Merge, then upload.
- Theme upload via the Admin API has a 16 KB document limit: one large template per call.
- After every upload compare the file checksum with your local file.

## 6. Owner checklist (Vietnamese, hand to the student)
1. Gửi: ảnh 7 màu cùng tỉ lệ 4:5, bảng size của nhà cung cấp, tải trọng thú cưng tối đa, giá vốn.
2. Agent tạo sản phẩm (DRAFT), biến thể màu × size, ảnh theo màu, mã giảm combo.
3. Agent nhân bản theme, dựng trang chủ + trang sản phẩm theo chuẩn trên, gửi link xem trước.
4. Bạn tự thêm: video (Customize → Video carousel), review thật (Content → Metaobjects → Customer review), logo + favicon (Theme settings → Logo).
5. Kiểm tra trên điện thoại → chuyển sản phẩm sang Active → Publish theme.
