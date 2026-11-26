"""Static preview of product.glow-wings-es.json using the same markup helpers as the English preview."""
import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "glow-wings"))
import build_preview as gw  # noqa: E402
from build_template_es import T  # noqa: E402

e = html.escape
OUT = ROOT / "preview"


def section_main_es(s):
    st = s["settings"]
    out = gw.section_main(s)
    out = out.replace("Add to cart<small data-add-sub>", e(st["label_add"]) + "<small data-add-sub>")
    labels = {"add": st["label_add"], "item": st["label_item"], "yourPick": st["label_your_pick"], "youSave": st["label_you_save"],
              "save": st["label_save"], "free": st["label_free"], "itemOne": st["label_item_one"],
              "itemOther": st["label_item_other"], "soldOutError": st["label_sold_out_error"]}
    out = out.replace('"addons": []}', '"addons": [], "labels": ' + json.dumps(labels, ensure_ascii=False) + "}")
    if not st["show_description"]:
        start = out.index("<details><summary>Description</summary>")
        out = out[:start] + out[out.index("</details>", start) + len("</details>"):]
    return out


def section_faq_es(s):
    st = s["settings"]
    out = gw.section_faq(s)
    for en, key in [("Contact us", "label_contact"),
                    ("Questions about your order? Send us a message and we'll reply within 1 business day.", "label_contact_text"),
                    ('placeholder="Name"', None), ('placeholder="Email"', None), ('placeholder="Your message"', None),
                    ("Send message", "label_send"), ("Or email us at", "label_email_us"), ("Track your order", "label_track"),
                    ('placeholder="Tracking number"', None), ("Track package", "label_track_button")]:
        if key:
            out = out.replace(e(en, quote=False) if "'" in en else en, e(st[key]))
    out = (out.replace('placeholder="Name"', f'placeholder="{e(st["label_name"])}"')
              .replace('placeholder="Email"', f'placeholder="{e(st["label_email"])}"')
              .replace('placeholder="Your message"', f'placeholder="{e(st["label_message"])}"')
              .replace('placeholder="Tracking number"', f'placeholder="{e(st["label_tracking_number"])}"'))
    return out


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "images").mkdir(exist_ok=True)
    for f in (ROOT.parent / "glow-wings/images").glob("*.jpg"):
        shutil.copy(f, OUT / "images" / f.name)
    theme = ROOT.parent / "theme/assets"
    shutil.copy(theme / "suzeno.css", OUT / "suzeno.css")
    shutil.copy(theme / "sz-product.js", OUT / "sz-product.js")
    render = dict(gw.RENDER, **{"sz-product": section_main_es, "sz-faq-contact": section_faq_es})
    marquee_items = "ENVÍO GRATIS A TODO EL MUNDO | IMPUESTOS Y ARANCELES INCLUIDOS | GARANTÍA DE 30 DÍAS | PIDE ANTES DEL 5 DE DIC. PARA RECIBIR EN NAVIDAD (EE. UU.)".split("|")
    marquee = "".join(f"<span>{e(t.strip())}</span>" for _ in range(2) for t in marquee_items)
    head = gw.HEAD.replace("<title>Glow Wings Preview</title>", "<title>Glow Wings ES Preview</title>")
    header = (gw.HEADER.replace('trang sản phẩm Glow Wings trên theme Suzeno. Nút "Add to cart" chỉ là demo.',
                                'trang Glow Wings tiếng Tây Ban Nha (link: /products/glow-wings?view=glow-wings-es). Nút mua chỉ là demo.')
              .replace("HOLIDAY DEALS END IN", "OFERTAS NAVIDEÑAS TERMINAN EN")
              .replace("MINS</span>", "MIN</span>").replace("SECS</span>", "SEG</span>"))
    footer = (gw.FOOTER.replace("Join the Suzeno family", "Únete a la familia Suzeno")
              .replace("Pet tips, new arrivals and members-only offers. No spam.", "Consejos para mascotas, novedades y ofertas exclusivas. Sin spam.")
              .replace("Made for the pets who make us smile.", "Hecho para las mascotas que nos hacen sonreír."))
    shim = gw.SHIM.replace('" sản phẩm sẽ được thêm vào giỏ trên website thật"', '" producto(s) se agregarían al carrito en la tienda real"')
    body = "".join(render[T["sections"][k]["type"]](T["sections"][k]) for k in T["order"] if T["sections"][k]["type"] in render)
    page = (head.replace('<style>', '<style>html{}', 1) + "\n" + header.format(marquee=marquee) + '\n<main id="MainContent" lang="es">'
            + body + "</main>\n" + footer + "\n" + shim + '\n<script src="sz-product.js"></script>\n')
    (OUT / "index.html").write_text(page, encoding="utf-8")
    print("wrote", OUT / "index.html")


if __name__ == "__main__":
    main()
