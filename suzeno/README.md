# Suzeno — dog raincoat store (suzeno.com)

Single-product landing page modelled on the competitor's layout (announcement countdown, gallery, bundle & save, upsells, reviews, FAQ, contact, newsletter, sticky add-to-cart).

- `page.html` — source (edit this). Run `python3 build.py` to regenerate `index.html`.
- `index.html` — standalone page for any static host.
- `assets/` — product photos. Add files here and list them in the `STORE.photos` array at the top of the `<script>` in `page.html`.

All prices, sizes, add-ons, FAQ and reviews live in the `STORE` config object. Reviews and the rating are SAMPLE placeholders: replace them with real customer reviews before launch.
