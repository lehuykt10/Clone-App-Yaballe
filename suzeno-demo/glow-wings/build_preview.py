"""Static preview of the Suzeno product page for product.glow-wings.json.

Mirrors the markup of the Suzeno theme sections (sz-product, sz-band, sz-story,
sz-hotspots, sz-steps, sz-faq-contact) so the page can be reviewed before upload.
Uses the theme's own suzeno.css and sz-product.js.
"""
import html
import json
import re
import shutil
from pathlib import Path

from build_template import TEMPLATE

ROOT = Path(__file__).parent
OUT = ROOT / "preview"
e = html.escape

PRODUCT = {
    "id": 1, "title": "Glow Wings Night Walk Light",
    "description": "<p>A small light that wraps around your dog's collar and projects glowing wings onto the path around "
                   "them, with a side light that helps others spot your dog after dark.</p>",
    "styles": [("Rainbow Butterfly", "rainbow-butterfly"), ("Golden Fairy", "golden-fairy"), ("Pink Dragon", "pink-dragon"),
               ("Purple Dragon", "purple-dragon"), ("Pink Heart Angel", "pink-heart-angel"), ("White Angel", "white-angel")],
    "price": 2695,
}
CIRCLE = ('<svg viewBox="0 0 200 80" preserveAspectRatio="none" aria-hidden="true"><path d="M18 46 C14 18 70 6 112 8 '
          'C160 10 192 24 188 44 C184 66 130 76 90 74 C46 72 12 62 16 40 C19 26 40 16 70 12"/></svg>')
TRUST_SVGS = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
]
CONFIRM_RE = re.compile(r"⟨XÁC NHẬN VỚI NCC⟩")


def mark(htmlstr):
    return CONFIRM_RE.sub('<mark class="todo">⟨xác nhận với NCC⟩</mark>', htmlstr)


def img(name):
    return f"images/suzeno-glow-wings-{name}.jpg"


def shop_image(ref):
    return "images/" + ref.split("shopify://shop_images/")[1]


def section_main(s):
    st = s["settings"]
    media = [(100 + i, img(slug), f"{PRODUCT['title']}, {name}") for i, (name, slug) in enumerate(PRODUCT["styles"])]
    media.append((200, img("light-device"), "The Glow Wings light with its adjustable strap"))
    slides = "".join(f'<div class="slide" data-media-id="{mid}"><img src="{src}" alt="{e(alt)}" loading="eager"></div>'
                     for mid, src, alt in media)
    thumbs = "".join(f'<button class="thumb" type="button" data-i="{i}" aria-label="Photo {i + 1}"><img src="{src}" alt=""></button>'
                     for i, (_, src, _) in enumerate(media))
    perks = "".join(f"<li>{e(b['settings']['text'])}</li>" for k in s["block_order"]
                    for b in [s["blocks"][k]] if b["type"] == "perk")
    acc = f'<details><summary>Description</summary><div class="ans rte">{PRODUCT["description"]}</div></details>'
    acc += "".join(f'<details><summary>{e(b["settings"]["title"])}</summary><div class="ans rte">{mark(b["settings"]["content"])}</div></details>'
                   for k in s["block_order"] for b in [s["blocks"][k]] if b["type"] == "accordion")
    trust = "".join(f"<div>{svg}{e(st[f'trust_{i + 1}'])}</div>" for i, svg in enumerate(TRUST_SVGS))
    product_json = {"id": 1, "title": PRODUCT["title"], "options": ["Style"], "variants": [
        {"id": i + 1, "title": name, "options": [name], "price": PRODUCT["price"], "compare_at_price": 0,
         "available": True, "featured_media": {"id": 100 + i}} for i, (name, _) in enumerate(PRODUCT["styles"])]}
    config = {"tiers": [{"qty": st[f"tier_{i}_qty"], "off": round(st[f"tier_{i}_discount"] * 100),
                         "label": st[f"tier_{i}_label"], "badge": st[f"tier_{i}_badge"]} for i in (1, 2, 3)],
              "defaultTier": st["default_tier"] - 1, "gift": st["gift_text"], "swatches": st["swatches"], "addons": []}
    timer = ('<div class="timer-pill">Hurry! Offer expires in: <b data-cd-all>00:00:00</b> ⏰</div>' if st["show_timer"] else "")
    return f'''<div class="shopify-section">
<div class="wrap product" data-sz-product>
  <div class="gallery">
    <div class="stage"><div class="slides" data-slides>{slides}</div>
      <button class="arrow prev" type="button" data-prev aria-label="Previous photo">‹</button>
      <button class="arrow next" type="button" data-next aria-label="Next photo">›</button></div>
    <div class="thumbs" role="tablist" aria-label="Product photos" data-thumbs>{thumbs}</div>
  </div>
  <div class="info">
    <div class="stock">{e(st["stock_line"])}</div>
    <h1 class="title">{e(PRODUCT["title"])}</h1>
    <ul class="perks">{perks}</ul>
    <div class="divider">{e(st["bundle_heading"].upper())}</div>{timer}
    <div class="bundles" data-bundles role="radiogroup" aria-label="Choose a bundle"></div>
    <button class="cta" type="button" data-add>Add to cart<small data-add-sub></small></button>
    <p class="err-msg" data-err hidden></p>
    <div class="trust">{trust}</div>
    <div class="acc">{acc}</div>
  </div>
</div>
<div class="sticky" data-sticky><div class="row"><span class="cur">USD</span><button class="cta" type="button" data-sticky-add>{e(st["sticky_label"])}</button></div></div>
<script type="application/json" data-product-json>{json.dumps(product_json)}</script>
<script type="application/json" data-config-json>{json.dumps(config)}</script>
</div>'''


def section_band(s):
    st = s["settings"]
    return f'''<div class="band" style="margin-top:44px">
  <svg class="wave-edge" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true" style="position:absolute;top:-43px;left:0"><path class="soft" d="M0 60 C240 20 480 20 720 45 C960 70 1200 70 1440 30 L1440 90 L0 90 Z"/><path d="M0 75 C260 40 520 40 760 60 C1000 80 1220 78 1440 50 L1440 90 L0 90 Z"/></svg>
  <div class="wrap"><h2>{e(st["before"])} <span class="circle">{e(st["circled"])}{CIRCLE}</span></h2><p>{e(st["text"])}</p></div>
</div>'''


def section_story(s):
    st = s["settings"]
    return f'''<section class="block"><div class="wrap story">
  <div class="media"><img src="{shop_image(st["image"])}" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="txt"><span class="eyebrow">{e(st["eyebrow"])}</span>
    <h2>{e(st["heading"])} <span class="circle" style="color:var(--sky-deep)">{e(st["circled"])}{CIRCLE}</span></h2>
    <div class="rte" style="font-size:16px">{st["text"]}</div></div>
</div></section>'''


def section_hotspots(s):
    st = s["settings"]
    bl = [s["blocks"][k]["settings"] for k in s["block_order"]]
    pins = "".join(f'<span class="pin" style="left:{b["x"]}%;top:{b["y"]}%">{i + 1}</span>' for i, b in enumerate(bl))
    legend = "".join(f'<li><span>{i + 1}</span><div><b>{e(b["title"])}</b><p>{e(b["text"])}</p></div></li>' for i, b in enumerate(bl))
    return f'''<section class="block anatomy"><div class="wrap">
  <div style="text-align:center;display:grid;gap:8px"><span class="eyebrow">{e(st["eyebrow"])}</span><h2>{e(st["heading"])}</h2></div>
  <div class="diagram" style="aspect-ratio:auto"><img src="{shop_image(st["image"])}" alt="" loading="lazy" style="height:auto">{pins}</div>
  <ol class="legend">{legend}</ol>
</div></section>'''


def section_steps(s):
    st = s["settings"]
    items = "".join(f'<li>{"<span class=step-n>%d</span>" % (i + 1) if st["numbered"] else ""}<b>{e(b["title"])}</b><p>{e(b["text"])}</p></li>'
                    for i, b in enumerate(s["blocks"][k]["settings"] for k in s["block_order"]))
    return f'''<section class="block" style="background:var(--{st["background"]})"><div class="wrap" style="display:grid;gap:24px">
  <div style="text-align:center;display:grid;gap:8px"><h2 style="font-size:clamp(28px,6.5vw,40px)">{e(st["heading"])}</h2></div>
  <ol class="steps" role="list" style="--cols:{min(len(s["block_order"]), 4)}">{items}</ol>
</div></section>'''


def section_faq(s):
    st = s["settings"]
    qs = "".join(f'<details{" open" if i == 0 and st["open_first"] else ""}><summary>{e(b["question"])}</summary><div class="ans rte">{mark(b["answer"])}</div></details>'
                 for i, b in enumerate(s["blocks"][k]["settings"] for k in s["block_order"]))
    return f'''<section class="block faq" id="faq"><div class="wrap grid-2">
  <div><h2>{e(st["heading"])}</h2><div class="acc">{qs}</div></div>
  <div style="display:grid;gap:18px;align-content:start">
    <form class="card" onsubmit="event.preventDefault()"><h3>Contact us</h3>
      <p>Questions about your order? Send us a message and we'll reply within 1 business day.</p>
      <label class="sr" for="SzName">Name</label><input class="field" id="SzName" placeholder="Name">
      <label class="sr" for="SzEmail">Email</label><input class="field" id="SzEmail" type="email" placeholder="Email">
      <label class="sr" for="SzMsg">Message</label><textarea class="field" id="SzMsg" placeholder="Your message"></textarea>
      <button class="btn sun" type="submit">Send message</button>
      <p class="note">Or email us at <b class="mail">support@suzeno.com</b></p></form>
    <form class="card" onsubmit="event.preventDefault()"><h3>Track your order</h3>
      <label class="sr" for="SzTrack">Tracking number</label><input class="field" id="SzTrack" placeholder="Tracking number">
      <button class="btn dark" type="submit">Track package</button></form>
  </div>
</div></section>'''


RENDER = {"sz-product": section_main, "sz-band": section_band, "sz-story": section_story,
          "sz-hotspots": section_hotspots, "sz-steps": section_steps, "sz-faq-contact": section_faq}

HEAD = '''<title>Glow Wings Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700;6..12,800&display=swap">
<style>
:root{--sky:#F3C2C8;--sky-deep:#D7263D;--sky-mist:#FDECEC;--sun:#F5B301;--sun-soft:#EDE6DA;--cta:#D7263D;--cta-ink:#ffffff;
--ink:#2B2B28;--ink-soft:#64645D;--line:#e7dfd2;--paper:#FAF7F2;--night:#3F5A4A;--ok:#2f9e6a;--sale:#d64545;
--font-display:"Quicksand","Nunito Sans",system-ui,sans-serif;--font-body:"Nunito Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
--r-sm:12px;--r-md:14px;--r-lg:14px;--pill:40px;--gutter-l:max(16px, env(safe-area-inset-left, 0px));--gutter-r:max(16px, env(safe-area-inset-right, 0px));color-scheme:light}
.preview-note{background:#1f2a24;color:#fff;font:600 12.5px/1.4 var(--font-body);text-align:center;padding:8px var(--gutter-r) 8px var(--gutter-l)}
mark.todo{background:#fff3b0;color:#5a4500;border-radius:4px;padding:0 4px;font-weight:700}
</style>
<link rel="stylesheet" href="suzeno.css">'''

HEADER = '''<div class="preview-note">BẢN XEM TRƯỚC: trang sản phẩm Glow Wings trên theme Suzeno. Nút "Add to cart" chỉ là demo.</div>
<div class="promo"><div class="wrap"><b>HOLIDAY DEALS END IN</b>
  <div class="clock" aria-hidden="true"><span><i data-cd-h>00</i>HRS</span><em>:</em><span><i data-cd-m>00</i>MINS</span><em>:</em><span><i data-cd-s>00</i>SECS</span></div>
</div></div>
<div class="marquee" aria-hidden="true"><div>{marquee}</div></div>
<header class="head"><div class="wrap">
  <span class="icon-btn" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></span>
  <a class="logo" href="#" aria-label="Suzeno home"><b style="font-family:var(--font-display);font-size:28px;color:var(--ink)">suzeno</b></a>
  <span class="icon-btn" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg></span>
</div></header>'''

FOOTER = '''<section class="news"><div class="wrap"><h2>Join the Suzeno family</h2><p>Pet tips, new arrivals and members-only offers. No spam.</p></div></section>
<footer><div class="wrap"><b style="font-family:var(--font-display);font-size:26px">suzeno</b><p class="note" style="max-width:46ch">Made for the pets who make us smile.</p>
<span class="mail">support@suzeno.com</span><span class="copy">© 2026 Suzeno</span></div></footer>
<div class="toast" id="toast" role="status"></div>'''

SHIM = '''<script>
/* Preview stand-in for suzeno.js: money format, toast, countdown. Add to cart only shows a message. */
(function(){
  var SZ = window.SZ = window.SZ || {};
  SZ.money = function(c){ return "$" + ((Number(c)||0)/100).toFixed(2); };
  SZ.esc = function(s){ return String(s == null ? "" : s).replace(/[&<>"]/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); };
  var t; SZ.toast = function(m){ var el = document.getElementById("toast"); el.textContent = m; el.classList.add("show"); clearTimeout(t); t = setTimeout(function(){ el.classList.remove("show"); }, 2400); };
  SZ.addItems = function(items){ var n = items.reduce(function(s,i){ return s + i.quantity; }, 0); SZ.toast("Demo: " + n + " sản phẩm sẽ được thêm vào giỏ trên website thật"); return Promise.resolve(); };
  function tick(){ var now = new Date(), end = new Date(now); end.setHours(24,0,0,0); var s = Math.max(0, Math.floor((end-now)/1000));
    var p = function(x){ return String(x).padStart(2,"0"); }, h = p(Math.floor(s/3600)), m = p(Math.floor(s%3600/60)), sec = p(s%60);
    document.querySelectorAll("[data-cd-h]").forEach(function(e){ e.textContent = h; });
    document.querySelectorAll("[data-cd-m]").forEach(function(e){ e.textContent = m; });
    document.querySelectorAll("[data-cd-s]").forEach(function(e){ e.textContent = sec; }); }
  tick(); setInterval(tick, 1000);
})();
</script>'''


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "images").mkdir(exist_ok=True)
    for f in (ROOT / "images").glob("*.jpg"):
        shutil.copy(f, OUT / "images" / f.name)
    shutil.copy(ROOT / "theme/assets/suzeno.css", OUT / "suzeno.css")
    shutil.copy(ROOT / "theme/assets/sz-product.js", OUT / "sz-product.js")
    marquee_items = "FREE WORLDWIDE SHIPPING | TAXES & DUTIES INCLUDED | 30-DAY GUARANTEE | ORDER BY DEC 5 FOR US CHRISTMAS DELIVERY".split("|")
    marquee = "".join(f"<span>{e(t.strip())}</span>" for _ in range(2) for t in marquee_items)
    body = "".join(RENDER[TEMPLATE["sections"][k]["type"]](TEMPLATE["sections"][k])
                   for k in TEMPLATE["order"] if TEMPLATE["sections"][k]["type"] in RENDER)
    page = (HEAD + "\n" + HEADER.format(marquee=marquee) + '\n<main id="MainContent">' + body + "</main>\n"
            + FOOTER + "\n" + SHIM + '\n<script src="sz-product.js"></script>\n')
    (OUT / "index.html").write_text(page, encoding="utf-8")
    print("wrote", OUT / "index.html")


if __name__ == "__main__":
    main()
