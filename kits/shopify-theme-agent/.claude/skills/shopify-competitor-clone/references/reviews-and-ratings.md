# Reviews and ratings on a Shopify theme (no app needed)

Competitor stores often show a rating pill ("4.8 · 1,000 reviews"), quotes under the
Add to cart button and a "What our customers say" grid. Rebuild the **layout**, but feed
it only with numbers that are true. This kit ships a ready, app-free system for that.

## Rules (explain them to the owner in Vietnamese)

| Allowed | Not allowed |
|---|---|
| Typing real reviews by hand (from your own customers, from the supplier listing of the same item, from people who got a free product) | Writing reviews yourself or with AI, or inventing names |
| Showing the real rating of the same product on another platform **with its name** ("4.8 from 1,240 ratings on AliExpress") | Typing a rating or count with no source ("4.8 · 853 reviews") |
| Customer photos used with permission | Model, studio or AI photos presented as customer photos |
| Showing 3–4 star reviews too | Hiding every review below 5 stars and claiming an average |
| Live counters from real data | "20+ orders in 24h", "2 people shopping now" |

Why: the US FTC rule on fake reviews (in force since Oct 2024) fines fake reviews,
invented ratings and fake social-proof counters per violation, **whatever the traffic
source** (ads, Instagram, TikTok, organic). The EU/UK have similar rules. Instagram and
TikTok also remove posts that send people to deceptive pages. If an owner insists on an
unsourced number, do not build it; offer the sourced rating below instead.

## What the kit gives you

The four files ship inside `shopify-theme-kit/theme/` and are copied into the theme by
`install_kit.py` (they are also in `templates/reviews/` here for reference).

| File | Installed as | What it does |
|---|---|---|
| `review-summary.liquid` | `snippets/` | Stars + "4.7 · 12 reviews" under the product title, computed from real reviews; then the sourced outside rating |
| `external-rating.liquid` | `snippets/` | "★ 4.8 from 1,240 ratings on AliExpress · See ratings"; hidden unless rating, count **and source** are filled |
| `review-quotes.liquid` | `snippets/` | Swipeable quotes (photo, text, name, stars) under Add to cart |
| `review-cards.liquid` | `sections/` | "What our customers say": rating pill computed from the reviews, outside rating line, photo cards; hidden until there is data |

In `templates/product.<suffix>.json` (main-product blocks, all `custom_liquid`):
- after `title`: `{% render 'review-summary', product: product %}`
- after `buy_buttons`: `{% render 'review-quotes', product: product, id: 'pdp' %}`
- add the section `{"type":"review-cards","settings":{}}` before the FAQ.
On the home page, set the section's `product` setting to the product handle.

## One-time store setup (Admin GraphQL, via the Shopify connector)

1. Metaobject definition `customer_review`, storefront `PUBLIC_READ`, publishable:
   fields `author` (single line, required), `location`, `rating` (integer 1–5, required),
   `body` (multi-line, required), `photo` (file, image), `color`, `size`,
   `source` (single line, required, choices: "Verified buyer",
   "Verified buyer · AliExpress", "Received a free product").
2. Product metafield `custom.reviews`: `list.metaobject_reference` → that definition.
3. Optional, outside rating: product metafields `custom.ext_rating` (number_decimal 1–5),
   `custom.ext_rating_count` (number_integer ≥ 1), `custom.ext_rating_source`
   (single line), `custom.ext_rating_url` (url, optional). All storefront `PUBLIC_READ`.
   Skip this step if the owner only wants their own customers' reviews.

```graphql
mutation { metaobjectDefinitionCreate(definition: { type: "customer_review", name: "Customer review",
  displayNameKey: "author", access: { storefront: PUBLIC_READ }, capabilities: { publishable: { enabled: true } },
  fieldDefinitions: [
    { key: "author", name: "Name (first name + initial)", type: "single_line_text_field", required: true },
    { key: "location", name: "Country", type: "single_line_text_field" },
    { key: "rating", name: "Stars (1-5)", type: "number_integer", required: true,
      validations: [{ name: "min", value: "1" }, { name: "max", value: "5" }] },
    { key: "body", name: "Review text (as written)", type: "multi_line_text_field", required: true },
    { key: "photo", name: "Customer photo", type: "file_reference",
      validations: [{ name: "file_type_options", value: "[\"Image\"]" }] },
    { key: "color", name: "Color bought", type: "single_line_text_field" },
    { key: "size", name: "Size bought", type: "single_line_text_field" },
    { key: "source", name: "Source", type: "single_line_text_field", required: true,
      validations: [{ name: "choices", value: "[\"Verified buyer\",\"Verified buyer · AliExpress\",\"Received a free product\"]" }] } ] })
  { metaobjectDefinition { id } userErrors { field message } } }
```
Then `metafieldDefinitionCreate` for each product metafield (ownerType `PRODUCT`; for
`reviews` add the validation `metaobject_definition_id` = the id returned above).

## Owner steps (Vietnamese, give these to the owner)

**Nhập review gõ tay (review thật):**
1. Shopify admin → **Content → Metaobjects → Customer review → Add entry**.
2. Điền: tên (tên + chữ cái đầu họ), quốc gia, số sao, nội dung (giữ nguyên ý khách, chỉ dịch), ảnh khách (nếu có), màu, size, nguồn.
3. Đặt trạng thái **Active** → Save.
4. Vào **Products → sản phẩm → Metafields → Customer reviews** → chọn các review vừa tạo → Save.
5. Sao dưới tên sản phẩm, ô điểm và khung review tự cập nhật. Không cần sửa theme.

**Hiện đánh giá từ nền tảng khác (ví dụ AliExpress):**
1. Mở listing của **đúng mẫu đó** trên AliExpress, ghi lại số sao và số lượt đánh giá thật.
2. **Products → sản phẩm → Metafields**: điền *Outside rating: stars* (vd 4.8), *number of ratings* (vd 1240), *source* (vd AliExpress), *link* (tuỳ chọn).
3. Trang sẽ hiện: "★ 4.8 from 1,240 ratings on AliExpress". Muốn tắt: xoá ô *source*.
4. Cập nhật lại số này khi listing thay đổi; khi review thật trên store đủ nhiều thì tắt.

## Test before handing over
- No reviews and no outside rating → stars, quotes and the section are all hidden on the storefront
  (the theme editor shows a hint instead).
- One review of 4★ and one of 5★ → "4.5 · 2 reviews"; pill says "Based on 2 reviews on <brand>".
- Outside rating with an empty source → nothing shown.
