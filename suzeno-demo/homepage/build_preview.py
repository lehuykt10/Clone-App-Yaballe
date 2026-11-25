"""Static preview of the new Suzeno homepage (templates/index.json), using the theme's CSS."""
import html
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "glow-wings"))
import build_preview as gw  # noqa: E402  (reuses the Suzeno header/footer/section markup)
from build_index import TEMPLATE  # noqa: E402

e = html.escape
OUT = ROOT / "preview"

# Store data as of 2026-11-25 (Shopify Admin), images downloaded to preview/images
PRODUCTS = {
    "glow-wings": ("Glow Wings", "$36.95", "", "suzeno-glow-wings-rainbow-butterfly.jpg", "suzeno-glow-wings-golden-fairy.jpg"),
    "cuddle-hoodie": ("Cuddle Hoodie", "$44.95", "", "03_MAIN_Wreath_Green.jpg", "06_Built_In_Pet_Pouch.jpg"),
    "burrow-hoodie": ("Burrow Hoodie", "$49.95", "", "burrow-hoodie-olive.jpg", "burrow-hoodie-dusty-pink.jpg"),
    "puddle-suit": ("Puddle Suit", "$39.95", "$42.99", "suzeno-raincoat-sky-blue-wet-walks.jpg", "suzeno-raincoat-styles.jpg"),
}


def img_of(ref):
    return "images/" + ref.split("shopify://shop_images/")[1]


def hero(s):
    st = s["settings"]
    b2 = f'<a class="hero-btn ghost" href="#">{e(st["button2_label"])}</a>' if st.get("button2_label") else ""
    return f'''<section class="hero"><div class="hero-media"><img src="{img_of(st["image"])}" alt="" style="object-position:50% 45%"></div>
<div class="hero-shade" style="--shade:{st["shade"] / 100}"></div>
<div class="wrap hero-copy"><span class="hero-eyebrow">{e(st["eyebrow"])}</span><h1>{e(st["heading"])}</h1><p>{e(st["text"])}</p>
<div class="hero-actions"><a class="hero-btn" href="#shop">{e(st["button_label"])}</a>{b2}</div></div></section>'''


def grid(s):
    st = s["settings"]
    cards = ""
    for k in s["block_order"]:
        b = s["blocks"][k]["settings"]
        title, price, compare, im1, im2 = PRODUCTS[b["product"]]
        badge = f'<span class="pbadge">{e(b["badge"])}</span>' if b["badge"] else ""
        comp = f"<s>{compare}</s>" if compare else ""
        cards += (f'<a class="pcard" href="#"><div class="pimg"><img src="images/{im1}" alt="{e(title)}" loading="lazy">'
                  f'<img class="pimg-alt" src="images/{im2}" alt="" loading="lazy">{badge}</div>'
                  f'<b>{e(title)}</b><span class="pp">{price}{comp}</span></a>')
    return f'''<section class="block" id="{st["anchor"]}"><div class="wrap pgrid-wrap">
<div class="pgrid-head"><span class="eyebrow">{e(st["eyebrow"])}</span><h2>{e(st["heading"])}</h2><p>{e(st["text"])}</p></div>
<div class="grid-cards">{cards}</div><a class="pgrid-more" href="#">{e(st["button_label"])}</a></div></section>'''


def story(s):
    st = s["settings"]
    right = " story--right" if st["image_right"] else ""
    return f'''<section class="block"><div class="wrap story{right}">
<div class="media"><img src="{img_of(st["image"])}" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover"></div>
<div class="txt"><span class="eyebrow">{e(st["eyebrow"])}</span>
<h2>{e(st["heading"])} <span class="circle" style="color:var(--sky-deep)">{e(st["circled"])}{gw.CIRCLE}</span></h2>
<div class="rte" style="font-size:16px">{st["text"]}</div><a class="story-btn" href="#">{e(st["button_label"])}</a></div></div></section>'''


RENDER = {"sz-hero": hero, "sz-product-grid": grid, "sz-story": story,
          "sz-steps": gw.section_steps, "sz-faq-contact": gw.section_faq}


def main():
    OUT.mkdir(exist_ok=True)
    shutil.copy(ROOT / "theme/assets/suzeno.css", OUT / "suzeno.css")
    head = gw.HEAD.replace("<title>Glow Wings Preview</title>", "<title>Suzeno Homepage Preview</title>")
    header = gw.HEADER.replace("trang sản phẩm Glow Wings trên theme Suzeno. Nút \"Add to cart\" chỉ là demo.",
                               "trang chủ mới của Suzeno. Các nút chỉ là demo; giá và ảnh lấy từ store ngày 25/11/2026.")
    marquee_items = "FREE WORLDWIDE SHIPPING | TAXES & DUTIES INCLUDED | 30-DAY GUARANTEE | ORDER BY DEC 5 FOR US CHRISTMAS DELIVERY".split("|")
    marquee = "".join(f"<span>{e(t.strip())}</span>" for _ in range(2) for t in marquee_items)
    body = "".join(RENDER[TEMPLATE["sections"][k]["type"]](TEMPLATE["sections"][k]) for k in TEMPLATE["order"])
    page = head + "\n" + header.format(marquee=marquee) + '\n<main id="MainContent">' + body + "</main>\n" + gw.FOOTER + "\n" + gw.SHIM + "\n"
    (OUT / "index.html").write_text(page, encoding="utf-8")
    print("wrote", OUT / "index.html")


if __name__ == "__main__":
    main()
