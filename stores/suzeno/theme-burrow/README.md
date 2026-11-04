# Suzeno one-product theme (Burrow Hoodie)

Files uploaded to the unpublished theme `145501257787` "Suzeno staging (Burrow Hoodie)",
duplicated from the live theme on 2026-11-04. JSON here is pretty-printed; Shopify stores it minified.

- `templates/product.burrow.json`: product page (assigned to Burrow Hoodie via template suffix `burrow`)
- `templates/index.json`: home page, Burrow Hoodie only
- `sections/wave-feature.liquid`: red wavy band, framed image, eyebrow, heading with a circled word
- `sections/video-carousel.liquid`: swipeable vertical videos; hidden until a video is added
- `sections/review-cards.liquid`: "What our customers say"; hidden until real reviews exist
- `snippets/review-summary.liquid`, `snippets/review-quotes.liquid`: stars under the title, quotes under Add to cart
- `snippets/delivery-timeline.liquid`: Ordered → Order ready → Delivered, dates by visitor country
- `config/settings_data.json`: adds scheme-6 (red) and scheme-7 (blush); buttons red
- `sections/header-group.json`: announcement links to the product; cart upsell removed (single product)

Outside rating (AliExpress etc.) is turned off for Suzeno; review source choices are "Verified buyer" and "Received a free product".
Reviews come from the metaobject `suzeno_review` (Content → Metaobjects → Customer review),
linked on the product via the metafield `suzeno.reviews` (list of Customer review).
Only real reviews; no hard-coded rating counts, fake "people shopping" counters or fake compare-at prices.
