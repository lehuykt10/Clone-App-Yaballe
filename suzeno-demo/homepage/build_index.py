"""Writes theme/templates/index.json: multi-product homepage for Suzeno."""
import json
from pathlib import Path

HDR = """/*
 * ------------------------------------------------------------
 * IMPORTANT: The contents of this file are auto-generated.
 *
 * This file may be updated by the Shopify admin theme editor
 * or related systems. Please exercise caution as any changes
 * made to this file may be overwritten.
 * ------------------------------------------------------------
 */
"""


def blocks(items):
    b, order = {}, []
    for key, typ, settings in items:
        b[key] = {"type": typ, "settings": settings}
        order.append(key)
    return b, order


hero = {"type": "sz-hero", "settings": {
    "image": "shopify://shop_images/suzeno-glow-wings-golden-fairy.jpg", "shade": 45,
    "eyebrow": "Holiday gift shop · Order by Dec 5 for US Christmas",
    "heading": "Gifts for the pets who make us smile",
    "text": "Cozy hoodies, rainy-day suits and glowing night walks. Free worldwide shipping, taxes included.",
    "button_label": "Shop gifts", "button_link": "/#shop",
    "button2_label": "Meet Glow Wings", "button2_link": "/products/glow-wings"}}

g_b, g_o = blocks([
    ("p-1", "product", {"product": "glow-wings", "badge": "New"}),
    ("p-2", "product", {"product": "cuddle-hoodie", "badge": "Christmas"}),
    ("p-3", "product", {"product": "burrow-hoodie", "badge": ""}),
    ("p-4", "product", {"product": "puddle-suit", "badge": ""}),
])
grid = {"type": "sz-product-grid", "blocks": g_b, "block_order": g_o, "settings": {
    "anchor": "shop", "eyebrow": "Shop", "heading": "Gifts for every kind of pet parent",
    "text": "Pick a style, choose a size, and we'll ship it free to your door.",
    "limit": 8, "button_label": "Shop all products", "button_link": "/collections/shop-all"}}

glow = {"type": "sz-story", "settings": {
    "image": "shopify://shop_images/suzeno-glow-wings-pink-dragon.jpg", "image_right": False,
    "eyebrow": "New for winter", "heading": "Dark evenings, but your dog still", "circled": "shines",
    "text": "<p>Glow Wings wraps around your dog's collar and projects glowing butterfly, dragon or angel wings "
            "onto the path around them. A side light helps cars and cyclists notice you both.</p>"
            "<p>6 styles. Rechargeable. Every night walk becomes the best photo of the day.</p>",
    "button_label": "Shop Glow Wings", "button_link": "/products/glow-wings"}}

hoodie = {"type": "sz-story", "settings": {
    "image": "shopify://shop_images/burrow-hoodie-olive.jpg", "image_right": True,
    "eyebrow": "Keep them close", "heading": "A hoodie with room for your", "circled": "best friend",
    "text": "<p>Our hoodies have a built-in pet pouch at the front, so your cat or small dog can snuggle in "
            "while you hang out, work or watch a movie.</p><p>Choose the Burrow Hoodie in 7 colors, or the "
            "Cuddle Hoodie in festive Christmas prints.</p>",
    "button_label": "Shop hoodies", "button_link": "/products/burrow-hoodie"}}

why_b, why_o = blocks([
    ("w-1", "item", {"title": "🚚 Free worldwide shipping", "text": "Tracked delivery to the US, Canada, the UK, Australia and more."}),
    ("w-2", "item", {"title": "🧾 Taxes & duties included", "text": "The price at checkout is the final price. Nothing extra to pay on delivery."}),
    ("w-3", "item", {"title": "💛 30-day guarantee", "text": "Arrived damaged or faulty? We'll refund you or send a replacement."}),
    ("w-4", "item", {"title": "💬 Real people", "text": "Email support@suzeno.com and we reply within 1 business day."}),
])
why = {"type": "sz-steps", "blocks": why_b, "block_order": why_o, "settings": {
    "eyebrow": "", "heading": "Why pet parents shop Suzeno", "numbered": False, "background": "sky-mist"}}

fq_b, fq_o = blocks([
    ("q-1", "question", {"question": "Will my order arrive before Christmas?", "answer":
        "<p>Order by December 5 for estimated US Christmas delivery. Later orders may still arrive in time, but we can't guarantee it.</p>"}),
    ("q-2", "question", {"question": "When will my order arrive?", "answer":
        "<p>US orders usually arrive in 9–17 days; Canada, the UK and Australia in 10–20 days; most other countries in 12–25 days. "
        "You get a tracking link by email as soon as it ships.</p>"}),
    ("q-3", "question", {"question": "Will I pay customs fees or taxes?", "answer":
        "<p>No. Our prices include all taxes and import duties, so the price at checkout is the final price. If a carrier ever asks "
        "you for a fee, contact us before paying and we'll take care of it.</p>"}),
    ("q-4", "question", {"question": "What if something arrives damaged or doesn't fit?", "answer":
        "<p>Contact support@suzeno.com within 30 days of delivery. If it arrives damaged or faulty, we'll refund you or send a "
        "replacement. For a different size, email us and we'll help.</p>"}),
    ("q-5", "question", {"question": "Do bundles save money?", "answer":
        "<p>Yes. Most products have a bundle discount when you buy 2 or more. You'll see the bundle price on each product page, "
        "and the discount is applied automatically in your cart.</p>"}),
])
faq = {"type": "sz-faq-contact", "blocks": fq_b, "block_order": fq_o, "settings": {
    "heading": "Good to know", "open_first": True, "show_contact": True, "tracking_url": "https://t.17track.net/en#nums="}}

TEMPLATE = {"sections": {"hero": hero, "grid": grid, "glow": glow, "hoodie": hoodie, "why": why, "faq": faq},
            "order": ["hero", "grid", "glow", "hoodie", "why", "faq"]}

if __name__ == "__main__":
    out = Path(__file__).parent / "theme/templates/index.json"
    out.write_text(HDR + json.dumps(TEMPLATE, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", out)
