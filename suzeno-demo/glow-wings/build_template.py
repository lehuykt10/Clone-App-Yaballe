"""Writes theme/templates/product.glow-wings.json (Suzeno theme, same section set as product.raincoat.json)."""
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
CONFIRM = "⟨XÁC NHẬN VỚI NCC⟩"


def blocks(items):
    b, order = {}, []
    for key, typ, settings in items:
        b[key] = {"type": typ, "settings": settings}
        order.append(key)
    return b, order


main_b, main_o = blocks([
    ("perk-1", "perk", {"text": "Projects glowing wings onto the ground around your dog"}),
    ("perk-2", "perk", {"text": "Side light helps cars and cyclists spot your dog after dark"}),
    ("perk-3", "perk", {"text": "Adjustable strap fits most collars and harnesses"}),
    ("perk-4", "perk", {"text": "6 wing styles: butterflies, dragons and angels"}),
    ("acc-1", "accordion", {"title": "How it looks in real life", "content":
        "<p>The light projects the wing pattern onto the ground beside and behind your dog. It looks brightest on dark, "
        "smooth surfaces like paths, pavement and snow, and softer on grass or under bright street lights.</p>"
        "<p>Product photos are illustrations of the effect. The wings appear on the ground, not attached to your dog.</p>"}),
    ("acc-2", "accordion", {"title": "What's in the box", "content":
        "<ul><li>1 Glow Wings light with adjustable strap, in the wing style you choose</li>"
        f"<li>Charging cable {CONFIRM}</li></ul>"}),
    ("acc-3", "accordion", {"title": "Battery & charging", "content":
        f"<p>Rechargeable battery {CONFIRM}. Charging time {CONFIRM}. Light time per charge {CONFIRM}.</p>"}),
    ("acc-4", "accordion", {"title": "Fit, care & safety", "content":
        "<ul><li>Wrap the strap around your dog's collar or harness and pull it snug so the light faces backwards.</li>"
        "<li>Not a toy. Don't let your dog chew the light.</li>"
        "<li>Wipe clean with a dry cloth. Don't put it in water.</li>"
        "<li>Always walk on a leash and stay visible yourself. The light is an extra, not a replacement for reflective gear.</li></ul>"}),
    ("acc-5", "accordion", {"title": "Shipping", "content":
        "<p>Free worldwide shipping with tracking. US orders usually arrive in 9–17 days; Canada, the UK and Australia in "
        "10–20 days; most other countries in 12–25 days. All taxes and import duties are included, so there's nothing extra "
        "to pay on delivery. <a href=\"/pages/shipping-policy\">Full shipping policy</a></p>"}),
    ("acc-6", "accordion", {"title": "Our guarantee", "content":
        "<p>If it arrives damaged or faulty, send a photo to support@suzeno.com within 30 days and we'll refund you or send "
        "a replacement.</p>"}),
])
main = {"type": "sz-product", "blocks": main_b, "block_order": main_o, "settings": {
    "stock_line": "6 WING STYLES · FITS MOST COLLARS", "rating_text": "", "notice": "",
    "bundle_heading": "Bundle & save", "show_timer": False, "default_tier": 2, "gift_text": "",
    "swatches": "Rainbow Butterfly:#b48cf0\nGolden Fairy:#f2b94b\nPink Dragon:#ff3fa4\nPurple Dragon:#9b4dff\n"
                "Pink Heart Angel:#ff8fc2\nWhite Angel:#e3e8f0",
    "show_size_link": False, "show_description": True, "sticky_label": "Add to cart",
    "trust_1": "Free worldwide shipping", "trust_2": "30-day guarantee", "trust_3": "Taxes & duties included",
    "tier_1_qty": 1, "tier_1_discount": 0, "tier_1_label": "1 Glow Wings light", "tier_1_badge": "",
    "tier_2_qty": 2, "tier_2_discount": 4.5, "tier_2_label": "2 lights · mix any styles", "tier_2_badge": "FOR 2 DOGS",
    "tier_3_qty": 3, "tier_3_discount": 7, "tier_3_label": "3 lights · mix any styles", "tier_3_badge": "BEST VALUE"}}

band = {"type": "sz-band", "settings": {"before": "Night walks, made", "circled": "magical", "after": "",
        "text": "Glowing wings on the path. A side light that helps drivers see you."}}
story = {"type": "sz-story", "settings": {
    "image": "shopify://shop_images/suzeno-glow-wings-golden-fairy.jpg", "image_right": False,
    "eyebrow": "Why dog parents love it", "heading": "Dark evenings, but your dog still", "circled": "shines",
    "text": "<p>From November, most walks happen after dark. Your dog disappears into the shadows, and every car seems "
            "too close.</p><p>The Glow Wings light wraps around the collar and projects a pair of glowing wings onto "
            "the path around your dog, while a light on each side helps others notice you both. Pick butterflies, "
            "dragons or angels.</p><p>Wrap it on, switch it on, walk. Your evening walk just became the best photo of the day.</p>"}}
hs_b, hs_o = blocks([
    ("h-1", "hotspot", {"title": "Projection lens", "x": 26, "y": 62, "text": "Shines the wing pattern down and back onto the ground."}),
    ("h-2", "hotspot", {"title": "Side light strip", "x": 45, "y": 83, "text": "Glows on both sides so your dog is easier to spot."}),
    ("h-3", "hotspot", {"title": "Adjustable strap", "x": 64, "y": 58, "text": "Wraps around most collars and harness straps."}),
    ("h-4", "hotspot", {"title": "Metal buckle", "x": 31, "y": 22, "text": "Holds the strap snug so the light keeps facing backwards."}),
])
hotspots = {"type": "sz-hotspots", "blocks": hs_b, "block_order": hs_o, "settings": {
    "image": "shopify://shop_images/suzeno-glow-wings-light-device.jpg",
    "eyebrow": "Small light, big effect", "heading": "How the Glow Wings light works"}}
st_b, st_o = blocks([
    ("s-1", "item", {"title": "Wrap it on", "text": "Wrap the strap around the collar with the lens facing backwards."}),
    ("s-2", "item", {"title": "Switch it on", "text": "Press the button. The wings appear on the ground behind your dog."}),
    ("s-3", "item", {"title": "Walk and shine", "text": "Best on dark paths, pavement and snow. Switch off when you're home."}),
])
how = {"type": "sz-steps", "blocks": st_b, "block_order": st_o, "settings": {
    "eyebrow": "", "heading": "Ready in 10 seconds", "numbered": True, "background": "sun-soft"}}
fq_b, fq_o = blocks([
    ("q-1", "question", {"question": "Will it look like the photos?", "answer":
        "<p>The photos show the effect. In real life the wings are projected onto the ground around your dog. They look "
        "brightest on dark, smooth surfaces and softer on grass or under street lights.</p>"}),
    ("q-2", "question", {"question": "Will it fit my dog's collar?", "answer":
        "<p>The adjustable strap wraps around most collars and harness straps. It works for small dogs to large dogs.</p>"}),
    ("q-3", "question", {"question": "Does it keep my dog safe at night?", "answer":
        "<p>The side lights help drivers and cyclists notice your dog, but no light can guarantee safety. Always use a "
        "leash and stay visible yourself.</p>"}),
    ("q-4", "question", {"question": "How do I charge it?", "answer": f"<p>{CONFIRM}</p>"}),
    ("q-5", "question", {"question": "Can I choose different styles in one order?", "answer":
        "<p>Yes. In the 2 and 3 light bundles you pick a style for each light.</p>"}),
    ("q-6", "question", {"question": "When will my order arrive?", "answer":
        "<p>US orders usually arrive in 9–17 days; Canada, the UK and Australia in 10–20 days; most other countries in "
        "12–25 days. You get a tracking link by email as soon as it ships.</p>"}),
    ("q-7", "question", {"question": "Will I pay customs fees or taxes?", "answer":
        "<p>No. Our prices include all taxes and import duties, so the price at checkout is the final price.</p>"}),
    ("q-8", "question", {"question": "What if it arrives damaged or doesn't work?", "answer":
        "<p>Contact support@suzeno.com within 30 days of delivery and we'll refund you or send a replacement.</p>"}),
])
faq = {"type": "sz-faq-contact", "blocks": fq_b, "block_order": fq_o, "settings": {
    "heading": "Good to know", "open_first": True, "show_contact": True, "tracking_url": "https://t.17track.net/en#nums="}}
reviews = {"type": "sz-testimonials", "settings": {"heading": "What our customers say"}}

TEMPLATE = {"sections": {"main": main, "band": band, "story": story, "hotspots": hotspots, "how": how,
                         "faq": faq, "reviews": reviews},
            "order": ["main", "band", "story", "hotspots", "how", "faq", "reviews"]}

if __name__ == "__main__":
    out = Path(__file__).parent / "theme/templates/product.glow-wings.json"
    out.write_text(HDR + json.dumps(TEMPLATE, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", out)
