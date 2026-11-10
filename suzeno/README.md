# Suzeno — dog raincoat store (suzeno.com)

Single-product landing page modelled on the competitor's layout (announcement countdown, gallery, bundle & save, upsells, reviews, FAQ, contact, newsletter, sticky add-to-cart).

- `page.html` — source (edit this). Run `python3 build.py` to regenerate `index.html`.
- `index.html` — standalone page for any static host.
- `assets/` — product photos. Add files here and list them in the `STORE.photos` array at the top of the `<script>` in `page.html`.

All prices, sizes, add-ons, FAQ and reviews live in the `STORE` config object. Reviews and the rating are SAMPLE placeholders: replace them with real customer reviews before launch.

## Shopify (live store setup)
The real store page lives in the suzeno Shopify theme, built from the theme's own sections so it uses the store's colors and fonts:
- `shopify/sections/feature-hotspots.liquid`: new section (numbered feature pins on a photo).
- `shopify/templates/product.raincoat.json`: product template (bundle picker, wave bands, hotspots, steps, comparison, reviews, FAQ, sticky buy bar).
Both are installed in the unpublished theme "Suzeno staging (raincoat page)". The product "Suzeno Full-Body Dog Raincoat" (draft) uses this template.
