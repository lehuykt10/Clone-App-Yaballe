"""Builds one product template per product for the Suzeno theme (run from the theme folder)."""
import json, os

SHIP = "<p>Free worldwide shipping with tracking. US orders usually arrive in 9–17 days; Canada, the UK and Australia in 10–20 days; most other countries in 12–25 days. All taxes and import duties are included, so there's nothing extra to pay on delivery. <a href=\"/pages/shipping-policy\">Full shipping policy</a></p>"
GUARANTEE = "<p>If it arrives damaged or faulty, send a photo to support@suzeno.com within 30 days and we'll refund you or send a replacement. Wrong size? Email us and we'll help.</p>"
XMAS = "🎄 Christmas delivery: order by Dec 5 (US), Dec 2 (CA, UK, AU) or Nov 28 (other countries)"
FAQ_SHIP = ("When will my order arrive?", "<p>US orders usually arrive in 9–17 days; Canada, the UK and Australia in 10–20 days; most other countries in 12–25 days. You get a tracking link by email as soon as it ships.</p>")
FAQ_TAX = ("Will I pay customs fees or taxes?", "<p>No. Our prices include all taxes and import duties, so the price at checkout is the final price. If a carrier ever asks you for a fee, contact us before paying and we'll take care of it.</p>")
FAQ_RETURN = ("What if it doesn't fit or arrives damaged?", "<p>Contact support@suzeno.com within 30 days of delivery. If it arrives damaged or faulty, we'll refund you or send a replacement. For a different size, email us and we'll help.</p>")
TRUST = {"trust_1": "Free worldwide shipping", "trust_2": "30-day guarantee", "trust_3": "Taxes & duties included"}
img = lambda f: f"shopify://shop_images/{f}"

def main(perks, accordions, tiers, swatches="", notice="", stock="", size_link=True, featured=None):
    blocks, order = {}, []
    for i, t in enumerate(perks):
        blocks[f"perk-{i+1}"] = {"type": "perk", "settings": {"text": t}}; order.append(f"perk-{i+1}")
    for i, (a, b) in enumerate(accordions):
        blocks[f"acc-{i+1}"] = {"type": "accordion", "settings": {"title": a, "content": b}}; order.append(f"acc-{i+1}")
    st = {"stock_line": stock, "rating_text": "", "notice": notice, "bundle_heading": "Bundle & save" if len(tiers) > 1 else "Choose your style",
          "show_timer": len(tiers) > 1, "default_tier": 1, "gift_text": "", "swatches": swatches, "show_size_link": size_link,
          "show_description": True, "sticky_label": "Add to cart", **TRUST}
    for i in range(3):
        q, off, label, badge = tiers[i] if i < len(tiers) else (0, 0, "", "")
        st.update({f"tier_{i+1}_qty": q, f"tier_{i+1}_discount": off, f"tier_{i+1}_label": label, f"tier_{i+1}_badge": badge})
    if featured: st["product"] = featured
    return {"type": "sz-product", "blocks": blocks, "block_order": order, "settings": st}

def band(before, circled, after="", text=""):
    return {"type": "sz-band", "settings": {"before": before, "circled": circled, "after": after, "text": text}}

def story(image, eyebrow, heading, circled, html, right=False):
    return {"type": "sz-story", "settings": {"image": image, "image_right": right, "eyebrow": eyebrow, "heading": heading, "circled": circled, "text": html}}

def steps(heading, items, numbered=True, bg="paper", eyebrow=""):
    return {"type": "sz-steps", "blocks": {f"s-{i+1}": {"type": "item", "settings": {"title": a, "text": b}} for i, (a, b) in enumerate(items)},
            "block_order": [f"s-{i+1}" for i in range(len(items))], "settings": {"eyebrow": eyebrow, "heading": heading, "numbered": numbered, "background": bg}}

def sizes(sz, rows, intro="", measure="", tip="Between sizes? Pick the bigger one.", first="Size", image="", eyebrow="Find the right fit"):
    return {"type": "sz-size-guide", "blocks": {f"r-{i+1}": {"type": "row", "settings": {"label": a, "values": v, "unit": u}} for i, (a, v, u) in enumerate(rows)},
            "block_order": [f"r-{i+1}" for i in range(len(rows))],
            "settings": {"eyebrow": eyebrow, "heading": "Size guide", "intro": intro, "image": image, "first_col": first, "sizes": sz, "measure": measure, "tip": tip}}

def hotspots(image, eyebrow, heading, pins):
    return {"type": "sz-hotspots", "blocks": {f"h-{i+1}": {"type": "hotspot", "settings": {"title": a, "x": x, "y": y, "text": d}} for i, (a, x, y, d) in enumerate(pins)},
            "block_order": [f"h-{i+1}" for i in range(len(pins))], "settings": {"image": image, "eyebrow": eyebrow, "heading": heading}}

def faq(items, heading="Good to know"):
    return {"type": "sz-faq-contact", "blocks": {f"q-{i+1}": {"type": "question", "settings": {"question": q, "answer": a}} for i, (q, a) in enumerate(items)},
            "block_order": [f"q-{i+1}" for i in range(len(items))], "settings": {"heading": heading, "open_first": True, "show_contact": True, "tracking_url": "https://t.17track.net/en#nums="}}

REVIEWS = {"type": "sz-testimonials", "settings": {"heading": "What our customers say"}}

def template(sections):
    sections = {**sections, "reviews": REVIEWS}
    return {"sections": sections, "order": list(sections.keys())}

T = {}

# ---------- Puddle Suit (raincoat) ----------
def puddle(featured=None):
    return template({
        "main": main(
            ["Clear face-shield hood keeps rain off eyes and ears", "Covers back, belly, all 4 legs and the tail", "Removable snap-on boots with anti-slip soles", "Reflective trim for dark, rainy evenings"],
            [("What's in the box", "<ul><li>1 full-body rain suit per set: hood with clear face shield, tail sleeve, adjustable cuffs and a leash D-ring</li><li>4 removable snap-on boots with anti-slip soles</li></ul>"),
             ("Sizing & fit", "<p>Measure your dog's back length from the base of the collar to the base of the tail, then check the size guide below. Between sizes, fluffy coat or deep chest? Size up.</p>"),
             ("Care", "<p>Rinse under the tap after muddy walks, or hand-wash in cool water with mild soap. Hang to dry. Don't tumble dry or iron.</p>"),
             ("Shipping", SHIP), ("Our guarantee", GUARANTEE)],
            [(1, 0, "1 Puddle Suit", ""), (2, 5, "2 Puddle Suits", "MOST POPULAR"), (3, 7, "3 Puddle Suits", "BEST VALUE")],
            swatches="Sky Blue:#9cc3ea\nCarrot Orange:#f47b20\nDino Green:#7a9a4a", stock="BOOTS INCLUDED · 3 COLORS", featured=featured),
        "band": band("Rainy walks,", "sorted", "", "Dry dog in, dry dog out. No muddy belly, no towel wrestling."),
        "story": story(img("suzeno-raincoat-carrot-wet-walks.jpg"), "Why dog parents switch", "Your dog stays dry. Your floors stay", "clean",
            "<p>Most dog raincoats only cover the back. The rain still soaks the belly, the legs splash through every puddle, and you spend the next 15 minutes drying a wet dog on the doormat.</p><p>The Puddle Suit covers your dog from nose to tail. The hood has a clear face shield, and adjustable cuffs, a tail sleeve and snap-on boots close the gaps where water usually gets in. Reflective bands keep you both visible after dark.</p><p>Snap it on, walk, rinse it off, hang it to dry. That's the whole routine.</p>"),
        "hotspots": hotspots(img("suzeno-raincoat-sky-blue-hotspots.jpg"), "Built for real rain", "Covered from nose to tail", [
            ("Snug hood", 58, 12, "Elastic edge stays in place when your dog shakes."), ("Clear face shield", 73, 36, "Wide-view PVC shield keeps rain off the eyes and ears without blocking vision."),
            ("Tail sleeve", 32, 26, "Covers the tail so it doesn't drip water down the back."), ("Snap-button chest", 57, 65, "Opens at the front, so nothing gets pulled over the head. A D-ring holds the leash."),
            ("Adjustable cuffs", 49, 76, "Toggle cuffs keep wind and splash out. Reflective bands shine in headlights."), ("Removable boots", 69, 93, "Snap-on boots with anti-slip soles keep paws dry and clean.")]),
        "how": steps("On in under a minute", [("Front legs in", "Step the front legs through and pull the hood over the head."), ("Snap the chest", "Close the snap buttons under the chin and chest."), ("Legs, tail & boots", "Slip the back legs and tail into their sleeves, then snap on the boots.")], bg="sun-soft"),
        "size": sizes("XS,S,M,L,XL,XXL", [("Back length", "20,25,30,35,40,45", "length"), ("Chest", "32,37,42,47,52,57", "length"), ("Neck", "27,29,32,35,38,41", "length"), ("Dog weight", "0.5-1.5,1.5-2.5,2.5-4,4-6,6-7.5,7.5-10", "weight")],
            measure="<p><strong>Back length:</strong> base of the collar to the base of the tail. <strong>Chest:</strong> widest part of the ribcage, just behind the front legs. <strong>Neck:</strong> where the collar sits, with room for two fingers.</p>",
            tip="Between sizes? Pick the bigger one. Back length matters most for a full-body suit."),
        "faq": faq([("What size should I get?", "<p>Measure your dog's back length from the base of the collar to the base of the tail, then check the size guide. Between two sizes, choose the bigger one.</p>"),
            ("Does the face shield bother dogs?", "<p>The clear shield sits in front of the face, not on it, so your dog can see normally. Let your dog wear the suit indoors for a few minutes the first time, with a treat.</p>"),
            ("Is it waterproof?", "<p>The high-density outer fabric makes water bead off, and the cuffs, tail sleeve and snap-on boots close the usual gaps.</p>"),
            ("Can my dog wear it without the boots?", "<p>Yes. The boots snap on and off, so you can leave them off for a lighter fit or for dogs still getting used to boots.</p>"),
            ("How do I clean it?", "<p>Rinse it under the tap or hand-wash in cool water with mild soap, then hang it to dry. No tumble dryer.</p>"),
            FAQ_SHIP, FAQ_TAX, FAQ_RETURN]),
    })
T["product.raincoat"] = puddle()
T["index"] = puddle(featured="puddle-suit")

# ---------- Burrow Hoodie ----------
T["product.burrow"] = template({
    "main": main(["Plush sherpa-style fleece that feels like a blanket", "Zip-up front pouch: your pet snuggles in and peeks out", "Fits cats and small dogs up to about 6 kg (13 lb)", "7 colors, sizes S to 3XL"],
        [("Pet size & weight", "<p>Fits cats and small dogs up to about <strong>6 kg (13 lb)</strong> that sit comfortably in the pouch, supported by your arms.</p><p>Bigger or very wriggly pets may prefer a lap cuddle instead.</p>"),
         ("Safe cuddles", "<ul><li>Always support your pet from below with your arms. The pouch is for cuddles, not hands-free carrying.</li><li>Don't use it while driving, cycling, cooking or doing anything where your pet could get hurt.</li><li>Start with a few minutes at home and let your pet climb out whenever they want. Never leave them in the pouch unattended or in the heat.</li></ul>"),
         ("Care", "<p>Turn inside out. Machine wash cold on a gentle cycle. Air-dry flat. Don't tumble dry, bleach or iron.</p>"),
         ("Shipping & Christmas delivery", SHIP), ("Our guarantee", GUARANTEE)],
        [(1, 0, "1 Hoodie", ""), (2, 5, "2 Hoodies", "GIFT PICK")],
        swatches="Olive:#6b7044\nDusty Pink:#d8a7a7\nBurgundy:#7a1f2b\nCream:#efe6d4\nHeather Grey:#a7a9ac\nSky Blue:#9cc3ea\nBlack:#1f1f1f", notice=XMAS, stock="7 COLORS · SIZES S–3XL"),
    "band": band("Designed for", "cozy", "moments together", "Close enough to feel your heartbeat. Snug enough to drift off."),
    "how": steps("How it works", [("Unzip", "Open the curved zip at the top of the front pouch."), ("Pet in", "Let your pet settle into the pouch, supported by your arms."), ("Peek-a-boo", "Their head pops out of the round opening. Zip back and cuddle up.")], bg="sky-mist"),
    "story": story(img("burrow-hoodie-olive.jpg"), "Made for two", "Warm hugs, all winter", "long",
        "<p>Movie nights, slow mornings and holiday photos. Plush fleece outside, a zip-up pouch up front, and your little one snuggled right where they love to be: with you.</p><p>It's a cozy hoodie on its own too, with a kangaroo hand pocket and drawstring hood.</p>"),
    "size": sizes("S,M,L,XL,2XL,3XL", [("Chest (around)", "112,118,124,130,136,142", "length"), ("Length", "74,75,76,77,78,79", "length"), ("Sleeve", "63,64,65,66,67,68", "length")],
        intro="<p>Relaxed, roomy fit to make room for your pet. Garment measurements may vary by 1–3 cm.</p>", eyebrow="Garment measurements",
        tip="Between sizes or carrying a bigger pet? Size up. Tip: lay a hoodie you love flat, measure across the chest and double it."),
    "faq": faq([("How does the pet pouch work?", "<p>Unzip the curved zip at the top of the front pouch and let your pet climb in. Their head pops out through the round, soft-edged opening, then zip it back so they stay snug against you. Always support them from below with your arms.</p>"),
        ("Which pets is it for?", "<p>Cats and small dogs up to about 6 kg (13 lb) that sit comfortably in the pouch. Start with short cuddle sessions at home and let them climb out whenever they want.</p>"),
        ("What size should I choose?", "<p>Pick your usual size: the fit is relaxed to make room for your pet. Between sizes? Size up.</p>"),
        ("Will it arrive before Christmas?", "<p>Order by December 5 for the US, December 2 for Canada, the UK and Australia, and November 28 for other countries.</p>"),
        ("How do I wash it?", "<p>Turn it inside out and machine wash cold on a gentle cycle. Air-dry flat; don't tumble dry or iron.</p>"), FAQ_TAX, FAQ_RETURN]),
})

# ---------- Cuddle Hoodie ----------
T["product.pet-hoodie"] = template({
    "main": main(["Front pouch: your cat peeks out while you cuddle", "Four festive designs for photos, parties and cozy nights", "Soft, roomy fit with zip pockets", "A gift every cat lover will smile at"],
        [("Details", "<ul><li>Front pet pouch with a soft, fluffy opening for your pet's head</li><li>Four festive designs: Holly Wreath, Candy Pink, Santa Red and Christmas Tree</li><li>Two zip side pockets and a zip chest pocket</li><li>Cozy hoodie with drawstring hood</li></ul>"),
         ("Safe cuddles", "<ul><li>Best for kittens, cats and small pets who sit comfortably in the pouch.</li><li>Always support your pet from below with your arms. The pouch is for cuddles, not hands-free carrying.</li><li>Never leave them in the pouch unattended or in the heat.</li></ul>"),
         ("Care", "<p>Turn inside out. Machine wash cold on a gentle cycle, or hand wash. Air-dry flat. Don't tumble dry, bleach or iron the decorations.</p>"),
         ("Shipping & Christmas delivery", SHIP), ("Our guarantee", GUARANTEE)],
        [(1, 0, "1 Hoodie", ""), (2, 5, "2 Hoodies", "GIFT PICK")],
        swatches="Holly Wreath:#2f6b3a\nCandy Pink:#f2a7bf\nSanta Red:#c8202f\nChristmas Tree:#1f5a36", notice=XMAS, stock="4 FESTIVE DESIGNS"),
    "band": band("Cuddles,", "built in", "", "Your cat stays snug against you while you relax."),
    "how": steps("How it works", [("Put it on", "Slip on your hoodie like any other."), ("Pet in", "Let your cat settle into the front pouch, supported by your arms."), ("Peek-a-boo", "Their head pops out of the fluffy opening, right under your chin."), ("Snap & share", "The cutest Christmas photo of the year.")], bg="sky-mist"),
    "story": story(img("10_Holiday_Lifestyle_Concepts.jpg"), "Why you'll love it", "Made for", "photos",
        "<p>Festive designs that look great on camera, a roomy fleece-lined pouch, and two zip pockets for your phone and treats.</p><p>It's a warm holiday hoodie on its own, with or without a cat.</p>"),
    "size": sizes("XXS,XS,S,M,L,XL,XXL", [("Bust", "98,102,106,112,118,124,130", "length"), ("Shoulder", "40,42,44,46,48,50,52", "length"), ("Sleeve", "58,60,62,63,64,66,68", "length"), ("Length", "63,65,67,69,71,73,75", "length"),
        ("US size", "0,2,4,6,8–10,12,14", "text"), ("UK size", "4,6,8,10,12–14,16,18", "text"), ("EU size", "32,34,36,38,40–42,44,46", "text")],
        intro="<p>Relaxed, roomy fit to make space for your pet. Garment measurements, laid flat, may vary by 1–3 cm.</p>", eyebrow="Garment measurements",
        tip="Between sizes or carrying a bigger cat? Size up."),
    "faq": faq([("How does the pet pouch work?", "<p>There's a roomy pouch on the front with a soft, fluffy opening at chest height. Your cat sits in the pouch, supported by your arms, and pokes their head out.</p>"),
        ("What size should I choose?", "<p>Pick your usual size: the hoodie has a relaxed, roomy fit. Between sizes, or carrying a bigger cat? Size up.</p>"),
        ("Which pets is it for?", "<p>Best for kittens, cats and small pets who sit comfortably in the pouch.</p>"),
        ("Will it arrive before Christmas?", "<p>To be safe, order by December 5 for the US, December 2 for Canada, the UK and Australia, and November 28 for other countries.</p>"),
        ("Is it only for pet owners?", "<p>Not at all. It's a cozy, festive hoodie on its own, with two zip side pockets.</p>"),
        ("How do I wash it?", "<p>Turn it inside out and machine wash cold on a gentle cycle, or hand wash. Air-dry flat.</p>"), FAQ_TAX, FAQ_RETURN]),
})

# ---------- Star Cape ----------
T["product.star-cape"] = template({
    "main": main(["Hooded tree cape with a gold star on top", "Ruffled layers and colorful pom-poms", "Easy drawstring tie at the neck", "Two festive colors: Tree Green and Santa Red"],
        [("What's included", "<ul><li>1 hooded Christmas tree cape with a gold star, pom-poms and a drawstring neck tie</li><li>Gift box and props in the photos are not included</li></ul>"),
         ("Safe & comfy", "<ul><li>Dress-up is for supervised fun: photos, parties and short wear.</li><li>Pom-poms and decorations are not toys. Take the costume off if your pet tries to chew it.</li><li>Keep ties loose enough to fit two fingers underneath.</li></ul>"),
         ("Shipping & Christmas delivery", SHIP), ("Our guarantee", GUARANTEE)],
        [(1, 0, "1 Star Cape", ""), (2, 5, "2 Star Capes", "GIFT PICK")],
        swatches="Tree Green:#2f6b3a\nSanta Red:#c8202f", notice=XMAS, stock="FOR SMALL DOGS & CATS"),
    "band": band("Your pet, the little", "Christmas tree", "of the house", "Holiday photos, family gatherings and Christmas parties."),
    "story": story(img("tree-cape3.png"), "Two pups, twice the cheer", "Mix and", "match",
        "<p>Got more than one furry friend? Dress them in Tree Green and Santa Red for the cutest holiday photo of the year. Choose 2 Star Capes and save $10.</p>"),
    "how": steps("How to dress up", [("Weigh", "Pick the size that matches your pet's weight."), ("Hood on", "Slip the hood gently over your pet's head."), ("Tie the bow", "Tie the drawstring loosely at the neck."), ("Say cheese", "Treats ready: it's holiday photo time.")], bg="sky-mist"),
    "size": sizes("S,M,L", [("Pet weight", "1.5-2.5,2.5-5,5-7.5", "weight")], intro="<p>Choose by your pet's weight.</p>", tip="Between two sizes, or a fluffy coat? Choose the larger one."),
    "gift": story(img("tree-cape1.png"), "Easy gifting", "A gift they'll love", "unwrapping",
        "<p>Shopping for a dog lover? The Star Cape is a sweet stocking stuffer for pups and the people who adore them.</p>", right=True),
    "faq": faq([("What's included?", "<p>One hooded Christmas tree cape with a gold star on top and colorful pom-poms.</p>"),
        ("How do I choose the size?", "<p>Choose by your pet's weight: S for 1.5–2.5 kg, M for 2.5–5 kg and L for 5–7.5 kg. Between sizes, go up one.</p>"),
        ("Is it for dogs or cats?", "<p>Both. It's made for small dogs and for cats who are comfortable wearing clothes.</p>"),
        ("Will it arrive before Christmas?", "<p>To be safe, order by December 5 for the US, December 2 for Canada, the UK and Australia, and November 28 for other countries.</p>"),
        FAQ_TAX, FAQ_RETURN]),
})

# ---------- Tree Cape (costume) ----------
T["product.pet-costume"] = template({
    "main": main(["Soft green cape with gold tinsel, pom-poms and a golden bow", "Matching tree hat with a star on top", "Hook-and-loop neck closure, elastic chin strap", "Quick to put on for holiday photos"],
        [("What's included", "<ul><li>1 tree cape with gold tinsel trim, colorful pom-poms and a golden bow</li><li>1 matching tree hat with a star and adjustable elastic chin strap</li></ul>"),
         ("Safe & comfy", "<ul><li>Dress-up is for supervised fun: photos, parties and short wear.</li><li>Pom-poms and tinsel are not toys. Take the costume off if your pet tries to chew it.</li><li>Keep the chin strap loose enough to fit two fingers underneath.</li></ul>"),
         ("Shipping & Christmas delivery", SHIP), ("Our guarantee", GUARANTEE)],
        [(1, 0, "1 Tree Cape set", "")], swatches="Green:#2f6b3a", notice=XMAS),
    "band": band("The cutest", "Christmas tree", "in the house", "Cape and hat set for dogs and cats."),
    "how": steps("How to dress up", [("Cape on", "Wrap the cape and close it at the neck with the hook-and-loop strip."), ("Hat on", "Place the tree hat and adjust the elastic chin strap."), ("Say cheese", "Treats ready: it's holiday photo time.")], bg="sky-mist"),
    "faq": faq([("What's included?", "<p>A green tree cape with gold tinsel, pom-poms and a golden bow, plus a matching tree hat with a star.</p>"),
        ("How does it close?", "<p>The cape closes at the neck with a hook-and-loop strip, and the hat has an adjustable elastic chin strap.</p>"),
        ("Will it arrive before Christmas?", "<p>To be safe, order by December 5 for the US, December 2 for Canada, the UK and Australia, and November 28 for other countries.</p>"),
        FAQ_TAX, FAQ_RETURN]),
})

# ---------- Pounce Toy ----------
T["product.puffer-toy"] = template({
    "main": main(["Random paths: rolls, backs up and turns like real prey", "Swinging tail spins it in place and darts off", "Soft silicone tires stay quiet on wood and tile", "Gentle glowing lights help your cat spot it"],
        [("How it plays", "<p>Switch it on and set it down. Pounce rolls forward, backs up and turns on random paths, and its swinging tail lets it spin and dart off in a new direction.</p>"),
         ("Safe play", "<ul><li>Play together and put the toy away after play.</li><li>Check the toy regularly and stop using it if any part is damaged.</li></ul>"),
         ("Shipping", SHIP), ("Our guarantee", GUARANTEE)],
        [(1, 0, "1 Pounce Toy", "")], swatches="Sky Blue:#9cc3ea\nLemon Yellow:#f5d84a", stock="2 COLORS", size_link=False),
    "band": band("Never moves in a", "straight", "line", "Unpredictable moves that keep cats chasing."),
    "story": story(img("BlueRobotCatToyAdventure.png"), "Meet Pounce", "The little pufferfish that", "darts",
        "<p>Random rolls, quick turns and a swinging tail that spins it in place, just like real prey. Soft tires keep it quiet on hard floors, and gentle lights make it easy for your cat to spot.</p>"),
    "how": steps("Why cats love it", [("Random paths", "Forward, back and sudden turns."), ("Tail-swing turns", "Spins in place and darts off."), ("Quiet tires", "Soft silicone on wood and tile."), ("Glowing lights", "Easy to spot, even in dim rooms.")], numbered=False, bg="sky-mist"),
    "faq": faq([("How do I start it?", "<p>Switch it on and set it on the floor. It starts moving on random paths right away.</p>"),
        ("Is it loud?", "<p>Soft silicone tires keep it quiet on wood and tile floors.</p>"),
        ("Which colors are there?", "<p>Sky Blue and Lemon Yellow.</p>"), FAQ_SHIP, FAQ_TAX, FAQ_RETURN]),
})

# ---------- Buzzy Bee ----------
T["product.cat-toy"] = template({
    "main": main(["Rolls, spins and flips at the tap of a button", "Tail lights glow in seven colors", "Feather tail that begs to be pounced on", "Rests after 5 minutes, a touch from your cat wakes it up"],
        [("How it plays", "<p>One tap and Buzzy rolls, spins and flips while its tail lights glow. After 5 minutes of play it takes a rest, and a touch from your cat wakes it up for another round.</p>"),
         ("Safe play", "<ul><li>Play together and put the toy away after play.</li><li>Replace the feather if it gets worn.</li></ul>"),
         ("Shipping", SHIP), ("Our guarantee", GUARANTEE)],
        [(1, 0, "1 Buzzy Bee", "")], swatches="Honey Yellow:#f5c02a\nBlossom Pink:#f2a7bf", size_link=False),
    "band": band("Turns any floor into a", "hunting", "ground", "Short, exciting bursts of play, just the way cats like it."),
    "how": steps("Why cats love it", [("Rolls & flips", "Unpredictable moves at one tap."), ("7-color lights", "A glowing tail to chase."), ("Feather tail", "Made for pouncing."), ("Smart rest", "Pauses after 5 minutes, wakes on touch.")], numbered=False, bg="sky-mist"),
    "faq": faq([("How long does it play?", "<p>It plays in 5-minute bursts, then rests. A touch from your cat wakes it up for another round.</p>"),
        ("Which colors are there?", "<p>Honey Yellow and Blossom Pink.</p>"), FAQ_SHIP, FAQ_TAX, FAQ_RETURN]),
})

# ---------- Pet Massager ----------
T["product.pet-massager"] = template({
    "main": main(["Soft kneading 'hands' for a relaxing back rub", "Cordless and rechargeable", "Strap on, press a button, relax together", "Use on the rug, the couch or their own bed"],
        [("How to use", "<p>Strap it on, press the button and let the soft kneading do the work during quiet time. Stay close and keep sessions short.</p>"),
         ("Safe use", "<ul><li>Always stay with your pet while the massager is on.</li><li>Keep sessions short and stop if your pet seems uncomfortable.</li></ul>"),
         ("Shipping", SHIP), ("Our guarantee", GUARANTEE)],
        [(1, 0, "1 Massager", "")], swatches="Midnight Black:#1f1f1f\nForest Green:#2f5a3a", size_link=False),
    "band": band("A good back rub,", "anytime", "", "Calm moments together on the sofa."),
    "how": steps("How it works", [("Strap on", "Fit it gently around your pet."), ("Press start", "Soft kneading begins."), ("Relax together", "Stay close and keep sessions short.")], bg="sky-mist"),
    "faq": faq([("Is it cordless?", "<p>Yes. It's rechargeable, so it goes wherever your pet likes to rest.</p>"),
        ("How long should a session be?", "<p>Keep sessions short and always stay close to your pet.</p>"), FAQ_SHIP, FAQ_TAX, FAQ_RETURN]),
})

# ---------- Forever Paw Kit ----------
T["product.paw-kit"] = template({
    "main": main(["Soft air-dry clay picks up every pad and toe", "One clay window and two 4 × 6 in photo windows", "Everything included, no oven required", "11.3 × 9.3 in frame for wall or tabletop"],
        [("What's in the box", "<ul><li>Ready-to-hang wood frame with one clay window and two 4 × 6 in (3R) photo windows</li><li>Air-dry clay, paint and brush, wooden roller stick, double-sided tape and step-by-step instructions</li></ul>"),
         ("Size", "<p>Frame: 11.3 × 9.3 in (28.7 × 23.6 cm). Works on a wall or a tabletop.</p>"),
         ("Shipping", SHIP), ("Our guarantee", GUARANTEE)],
        [(1, 0, "1 Paw Kit", "")], swatches="Natural Oak:#c8a06a\nCloud White:#f2efe8\nWalnut:#6b4a32\nMidnight Black:#1f1f1f", stock="4 FRAME COLORS", size_link=False),
    "band": band("A memory that lasts", "forever", "", "Paw print, nose print and two favorite photos in one frame."),
    "how": steps("How it works", [("Roll the clay", "Flatten the clay with the wooden roller."), ("Press the paw", "Gently press your pet's paw or nose."), ("Let it dry", "Air-dry, then paint if you like."), ("Frame it", "Add two photos and hang or stand it.")], bg="sky-mist"),
    "story": story(img("Suzeno_ForeverPawKit10.png"), "Why pet parents love it", "More than a paw", "print",
        "<p>A gift they'll keep forever: for new pets, birthdays, adoption anniversaries and remembrance. Everything you need is in one box, no oven required.</p>"),
    "faq": faq([("Do I need an oven?", "<p>No. The clay air-dries.</p>"),
        ("Does it work for cats and dogs?", "<p>Yes. The soft clay picks up paw and nose details for dogs and cats.</p>"),
        ("What size photos fit?", "<p>Two 4 × 6 in (3R) photos.</p>"), FAQ_SHIP, FAQ_TAX, FAQ_RETURN]),
})

# ---------- default for any new product ----------
T["product"] = template({
    "main": main([], [("Shipping", SHIP), ("Our guarantee", GUARANTEE)], [(1, 0, "1 item", "")], size_link=False),
    "faq": faq([FAQ_SHIP, FAQ_TAX, FAQ_RETURN]),
})

for name, data in T.items():
    with open(f"templates/{name}.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
print("wrote", len(T), "templates:", ", ".join(sorted(T)))
