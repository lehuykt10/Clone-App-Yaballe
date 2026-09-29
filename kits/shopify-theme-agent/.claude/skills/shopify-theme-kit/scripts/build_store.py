#!/usr/bin/env python3
"""Turn brand/brand.json into a finished Dawn theme (any niche).

Writes into the theme folder:
    config/settings_data.json      colours, fonts, radius, cart drawer
    templates/product.json         product page (bundle picker, delivery ETA, trust, tabs, sections)
    templates/index.json           home page
    templates/page.about.json      /pages/about  (page template suffix "about")
    templates/page.faq.json        /pages/faq    (suffix "faq")
    templates/page.how-it-works.json (suffix "how-it-works", only if how_it_works is set)
    sections/header-group.json     announcement bar + header
    sections/footer-group.json     footer

Run install_kit.py on the theme first. Then:
    python .claude/skills/shopify-theme-kit/scripts/build_store.py [--brand brand/brand.json] [--theme theme]

Every key in brand.json is documented in references/brand-json.md.
Missing optional keys simply skip that part of the page.
"""
import argparse
import json
import sys
from pathlib import Path

B = {}
THEME = Path("theme")

# Africa + South America: slower postal routes from Asian warehouses.
SLOW_COUNTRIES = (
    "DZ,AO,BJ,BW,BF,BI,CM,CV,CF,TD,KM,CG,CD,CI,DJ,EG,GQ,ER,SZ,ET,GA,GM,GH,GN,GW,KE,LS,LR,LY,MG,MW,ML,MR,MU,"
    "YT,MA,MZ,NA,NE,NG,RE,RW,SH,ST,SN,SC,SL,SO,ZA,SS,SD,TZ,TG,TN,UG,EH,ZM,ZW,AC,TA,IO,TF,"
    "AR,BO,BR,CL,CO,EC,FK,GF,GY,PY,PE,SR,UY,VE,GS"
).split(",")

# Icon names accepted by Dawn's icon-with-text and collapsible_tab blocks.
ICONS = set("""apple banana bottle box carrot chat_bubble check_mark clipboard dairy dairy_free dryer eye fire
gluten_free heart iron leaf leather lightning_bolt lipstick lock map_pin nut_free pants paw_print pepper perfume
plane plant price_tag question_mark recycle return ruler serving_dish shirt shoe silhouette snowflake star
stopwatch truck washing""".split())

RADIUS = {
    "rounded": {"buttons_radius": 40, "inputs_radius": 12, "variant_pills_radius": 40, "card_corner_radius": 14,
                "media_radius": 14, "text_boxes_radius": 14, "popup_corner_radius": 14, "badge_corner_radius": 40},
    "soft": {"buttons_radius": 8, "inputs_radius": 8, "variant_pills_radius": 8, "card_corner_radius": 8,
             "media_radius": 8, "text_boxes_radius": 8, "popup_corner_radius": 8, "badge_corner_radius": 8},
    "sharp": {"buttons_radius": 0, "inputs_radius": 0, "variant_pills_radius": 0, "card_corner_radius": 0,
              "media_radius": 0, "text_boxes_radius": 0, "popup_corner_radius": 0, "badge_corner_radius": 0},
}


# ---------------------------------------------------------------- helpers
def get(path, default=None):
    """get("delivery.rules") → B["delivery"]["rules"] or default."""
    node = B
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def para(text):
    text = text.strip()
    return text if text.startswith("<") else f"<p>{text}</p>"


def read_json(rel):
    raw = (THEME / rel).read_text(encoding="utf-8")
    start = raw.index("{")
    return raw[:start], json.loads(raw[start:])


def write(rel, data, comment=""):
    (THEME / rel).write_text(comment + json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("  wrote", rel)


def product_link():
    return f"shopify://products/{B['product']['handle']}"


def image_ref(name):
    """Image from Admin → Content → Files (file name) or already a shopify:// URL."""
    if not name:
        return None
    return name if name.startswith("shopify://") else f"shopify://shop_images/{name}"


def contrast(a, b):
    def lum(h):
        c = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    hi, lo = sorted([lum(a), lum(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def check_contrast():
    c = B["colors"]
    pairs = [("text", "background"), ("text", "surface"), ("primary_text", "primary"), ("dark_text", "dark")]
    for fg, bg in pairs:
        ratio = contrast(c[fg], c[bg])
        if ratio < 4.5:
            print(f"  CANH BAO: do tuong phan {fg}/{bg} = {ratio:.2f} (< 4.5), chu kho doc. Nen chinh mau.")


# ---------------------------------------------------------------- settings
def settings():
    _, data = read_json("config/settings_data.json")
    base = data["presets"].get("Dawn") or next(iter(data["presets"].values()))
    current = dict(base)
    c = B["colors"]

    def scheme(bg, text, button, label, secondary):
        return {"settings": {"background": bg, "background_gradient": "", "text": text, "button": button,
                             "button_label": label, "secondary_button_label": secondary, "shadow": c["text"]}}

    current["color_schemes"] = {
        "scheme-1": scheme(c["background"], c["text"], c["primary"], c["primary_text"], c["dark"]),
        "scheme-2": scheme(c["surface"], c["text"], c["primary"], c["primary_text"], c["dark"]),
        "scheme-3": scheme(c["dark"], c["dark_text"], c["dark_text"], c["dark"], c["dark_text"]),
        "scheme-4": scheme(c.get("accent", c["surface"]), c.get("accent_text", c["text"]), c["dark"], c["dark_text"],
                           c.get("accent_text", c["text"])),
        "scheme-5": scheme(c["primary"], c["primary_text"], c["primary_text"], c["primary"], c["primary_text"]),
    }
    current.update(RADIUS[get("style.radius", "rounded")])
    current.update({
        "type_header_font": get("fonts.heading", "assistant_n4"),
        "type_body_font": get("fonts.body", "assistant_n4"),
        "heading_scale": get("style.heading_scale", 110),
        "body_scale": get("style.body_scale", 100),
        "page_width": get("style.page_width", 1200),
        "spacing_sections": 8,
        "cart_type": "drawer",
        "show_vendor": False,
        "show_cart_note": True,
        "currency_code_enabled": False,
        "predictive_search_enabled": True,
        "brand_headline": get("brand.tagline", ""),
        "brand_description": para(get("brand.description", "")),
        "sale_badge_color_scheme": "scheme-5",
    })
    data["current"] = current
    write("config/settings_data.json", data)


# ---------------------------------------------------------------- shared sections
def grid_section(heading, items, color="scheme-1", columns=4):
    blocks = {f"b-{i}": {"type": "benefit", "settings": {"title": t, "text": para(x)}}
              for i, (t, x) in enumerate(items, 1)}
    return {"type": "benefits-grid", "blocks": blocks, "block_order": list(blocks),
            "settings": {"heading": heading, "heading_size": "h1", "columns_desktop": min(columns, max(2, len(items))),
                         "color_scheme": color, "padding_top": 48, "padding_bottom": 48}}


def how_section(color="scheme-2"):
    how = get("how_it_works")
    if not how:
        return None
    steps = [(f"{i}. {t}", x) for i, (t, x) in enumerate(how["steps"], 1)]
    return grid_section(how.get("heading", "How it works"), steps, color)


def benefits_section(color="scheme-1"):
    ben = get("benefits")
    return grid_section(ben.get("heading", "Why customers love it"), ben["items"], color) if ben else None


def comparison_section():
    comp = get("comparison")
    if not comp:
        return None
    blocks = {f"r-{i}": {"type": "row", "settings": {"feature": f, "us": u, "them": t}}
              for i, (f, u, t) in enumerate(comp["rows"], 1)}
    return {"type": "comparison-table", "blocks": blocks, "block_order": list(blocks),
            "settings": {"heading": comp.get("heading", "Why customers switch"), "heading_size": "h1",
                         "us_label": comp.get("us_label", B["brand"]["name"]),
                         "them_label": comp.get("them_label", "Typical alternatives"),
                         "color_scheme": "scheme-2", "padding_top": 48, "padding_bottom": 48}}


def faq_section(items, heading="Questions? We've got answers", color="scheme-1"):
    if not items:
        return None
    blocks = {f"q-{i}": {"type": "question", "settings": {"question": q, "answer": para(a)}}
              for i, (q, a) in enumerate(items, 1)}
    return {"type": "faq-accordion", "blocks": blocks, "block_order": list(blocks),
            "settings": {"heading": heading, "heading_size": "h1", "open_first": True,
                         "color_scheme": color, "padding_top": 48, "padding_bottom": 48}}


def size_guide_section():
    sg = get("size_guide")
    if not sg:
        return None
    blocks = {f"s-{i}": {"type": "row", "settings": {"size": r[0], "value_2": r[1], "value_3": r[2], "value_4": r[3]}}
              for i, r in enumerate(sg["rows"], 1)}
    cols = sg["columns"]
    return {"type": "size-guide", "blocks": blocks, "block_order": list(blocks),
            "settings": {"heading": sg.get("heading", "Find your size"), "heading_size": "h1",
                         "intro": para(sg.get("intro", "")) if sg.get("intro") else "",
                         "col_1": cols[0], "col_2": cols[1], "col_3": cols[2], "col_4": cols[3],
                         "note": para(sg.get("note", "")) if sg.get("note") else "",
                         "color_scheme": "scheme-1", "padding_top": 36, "padding_bottom": 36}}


def story_section(story, color="scheme-1"):
    """Image + text split. story = {image, heading, text, layout?, button?}."""
    blocks = {"h": {"type": "heading", "settings": {"heading": story["heading"], "heading_size": "h1"}},
              "t": {"type": "text", "settings": {"text": para(story["text"]), "text_style": "body"}}}
    order = ["h", "t"]
    if story.get("button"):
        blocks["b"] = {"type": "button", "settings": {"button_label": story["button"],
                                                     "button_link": story.get("link", product_link()),
                                                     "button_style_secondary": False}}
        order.append("b")
    settings = {"height": "adapt", "desktop_image_width": "medium",
                "layout": story.get("layout", "image_first"), "image_behavior": "none", "content_layout": "no-overlap",
                "desktop_content_position": "middle", "desktop_content_alignment": "left",
                "mobile_content_alignment": "left", "section_color_scheme": color, "color_scheme": color,
                "padding_top": 36, "padding_bottom": 36}
    if image_ref(story.get("image")):
        settings["image"] = image_ref(story["image"])
    return {"type": "image-with-text", "blocks": blocks, "block_order": order, "settings": settings}


def closing_section():
    cl = get("closing")
    if not cl:
        return None
    return {"type": "rich-text",
            "blocks": {"h": {"type": "heading", "settings": {"heading": cl["heading"], "heading_size": "h1"}},
                       "t": {"type": "text", "settings": {"text": para(cl["text"])}}},
            "block_order": ["h", "t"],
            "settings": {"desktop_content_position": "center", "content_alignment": "center",
                         "color_scheme": "scheme-3", "full_width": True, "padding_top": 56, "padding_bottom": 56}}


# ---------------------------------------------------------------- product page blocks
def delivery_liquid():
    d = get("delivery")
    if not d or not d.get("enabled", True):
        return None
    lines = ["{%- liquid", "  assign cc = localization.country.iso_code", "  assign key = ',' | append: cc | append: ','",
             f"  assign d1 = {d['default']['min']}", f"  assign d2 = {d['default']['max']}"]
    for i, rule in enumerate(d.get("rules", [])):
        countries = SLOW_COUNTRIES if rule["countries"] == "AFRICA_SOUTH_AMERICA" else rule["countries"]
        keyword = "if" if i == 0 else "elsif"
        lines.append(f"  {keyword} ',{','.join(countries)},' contains key")
        lines.append(f"    assign d1 = {rule['min']}")
        lines.append(f"    assign d2 = {rule['max']}")
    if d.get("rules"):
        lines.append("  endif")
    lines += ["  assign now_s = 'now' | date: '%s' | plus: 0",
              "  assign from_s = d1 | times: 86400 | plus: now_s",
              "  assign to_s = d2 | times: 86400 | plus: now_s", "-%}"]
    lead = "Free shipping to" if d.get("free_shipping", True) else "Ships to"
    html = (f"<p class=\"kit-eta\">🚚 {lead} {{{{ localization.country.name }}}} · Estimated delivery "
            "<strong>{{ from_s | date: '%b %-d' }} – {{ to_s | date: '%b %-d' }}</strong>")
    if d.get("note"):
        html += f"<br><span>{d['note']}</span>"
    html += "</p>"
    if d.get("payment_icons", True):
        html += ("{%- if shop.enabled_payment_types.size > 0 -%}<ul class=\"kit-pay\" role=\"list\">"
                 "{%- for type in shop.enabled_payment_types -%}<li>{{ type | payment_type_svg_tag }}</li>{%- endfor -%}"
                 "</ul>{%- endif -%}")
    html += ("<style>.kit-eta{font-size:1.4rem;margin:0.4rem 0 0.8rem;text-align:center}"
             ".kit-pay{display:flex;flex-wrap:wrap;gap:0.6rem;justify-content:center;list-style:none;margin:0 0 0.8rem;padding:0}"
             ".kit-pay svg{height:2.4rem;width:3.8rem}</style>")
    return "\n".join(lines) + html


def bundle_block():
    bd = get("bundle")
    if not bd or not bd.get("enabled", True):
        return None
    s = {"heading": bd.get("heading", "Choose your bundle"), "default_tier": bd.get("default_tier", 2),
         "discount_type": bd.get("discount_type", "amount"), "save_label": bd.get("save_label", "Save")}
    tiers = bd["tiers"][:3] + [{"qty": 0}] * (3 - len(bd["tiers"][:3]))
    for i, t in enumerate(tiers, 1):
        s.update({f"tier_{i}_qty": t.get("qty", 0), f"tier_{i}_discount": t.get("discount", 0),
                  f"tier_{i}_label": t.get("label", ""), f"tier_{i}_sublabel": t.get("sublabel", ""),
                  f"tier_{i}_badge": t.get("badge", ""), f"tier_{i}_perks": t.get("perks", "")})
    return {"type": "bundle_picker", "settings": s}


def product_template():
    blocks = {"title": {"type": "title"}, "rating": {"type": "rating"}}
    order = ["title", "rating"]
    bullets = get("product.bullets")
    if bullets:
        items = "".join(f"<li>{b}</li>" for b in bullets)
        blocks["bullets"] = {"type": "custom_liquid", "settings": {"custom_liquid":
            f"<ul class=\"kit-bullets\">{items}</ul>"
            "<style>.kit-bullets{list-style:none;margin:0.4rem 0 0;padding:0;display:grid;gap:0.6rem;font-size:1.5rem}</style>"}}
        order.append("bullets")
    bundle = bundle_block()
    if bundle:
        blocks["bundle"] = bundle
        order.append("bundle")
    else:
        blocks["price"] = {"type": "price"}
        blocks["variant_picker"] = {"type": "variant_picker", "settings": {"picker_type": "button", "swatch_shape": "circle"}}
        blocks["quantity"] = {"type": "quantity_selector"}
        order += ["price", "variant_picker", "quantity"]
    blocks["buy_buttons"] = {"type": "buy_buttons", "settings": {"show_dynamic_checkout": get("product.dynamic_checkout", False),
                                                                 "show_gift_card_recipient": False}}
    order.append("buy_buttons")
    eta = delivery_liquid()
    if eta:
        blocks["delivery"] = {"type": "custom_liquid", "settings": {"custom_liquid": eta}}
        order.append("delivery")
    trust = get("trust")
    if trust:
        s = {"layout": "horizontal"}
        for i, item in enumerate(trust[:3], 1):
            s[f"icon_{i}"] = item["icon"]
            s[f"heading_{i}"] = item["text"]
        blocks["trust"] = {"type": "icon-with-text", "settings": s}
        order.append("trust")
    for i, tab in enumerate(get("product.tabs", []), 1):
        blocks[f"tab-{i}"] = {"type": "collapsible_tab", "settings": {
            "heading": tab["heading"], "icon": tab.get("icon", "check_mark"), "content": para(tab["content"])}}
        order.append(f"tab-{i}")

    main = {"type": "main-product", "blocks": blocks, "block_order": order,
            "settings": {"enable_sticky_info": True, "color_scheme": "scheme-1", "media_position": "left",
                         "gallery_layout": "thumbnail_slider", "media_size": "large", "constrain_to_viewport": True,
                         "media_fit": "cover", "image_zoom": "lightbox", "mobile_thumbnails": "show",
                         "hide_variants": bool(bundle), "enable_video_looping": True,
                         "padding_top": 24, "padding_bottom": 24}}

    stories = get("stories", [])
    sections = {"main": main}
    candidates = [
        ("how", how_section()),
        ("benefits", benefits_section()),
        ("story-1", story_section(stories[0]) if len(stories) > 0 else None),
        ("compare", comparison_section()),
        ("story-2", story_section(stories[1], color="scheme-2") if len(stories) > 1 else None),
        ("size", size_guide_section()),
        ("faq", faq_section(get("faq", []))),
        ("closing", closing_section()),
        ("sticky", {"type": "sticky-atc", "settings": {"button_label": get("product.button_label", "Add to cart"),
                                                        "mobile_only": False, "color_scheme": "scheme-1"}}),
    ]
    for key, sec in candidates:
        if sec:
            sections[key] = sec
    write("templates/product.json", {"sections": sections, "order": list(sections)})


# ---------------------------------------------------------------- home
def welcome_code_liquid(code, text):
    return ("<script>document.addEventListener('DOMContentLoaded',function(){"
            "document.querySelectorAll('.newsletter-form__message--success').forEach(function(el){"
            f"el.insertAdjacentHTML('afterend','<p class=\"kit-welcome\">{text}: <strong>{code}</strong>"
            "<br>Enter it at checkout on your first order.</p>');});});</script>"
            "<style>.kit-welcome{margin:1rem auto 0;padding:1rem 1.6rem;border:2px dashed currentColor;"
            "border-radius:1rem;max-width:36rem;text-align:center;font-size:1.6rem}</style>")


def index_template():
    hero = B["hero"]
    sections = {}
    if image_ref(hero.get("image")):
        sections["hero"] = story_section({**hero, "button": hero.get("button", "Shop now")}, color="scheme-2")
    else:
        sections["hero"] = {"type": "rich-text",
                            "blocks": {"h": {"type": "heading", "settings": {"heading": hero["heading"], "heading_size": "h0"}},
                                       "t": {"type": "text", "settings": {"text": para(hero["text"])}},
                                       "b": {"type": "button", "settings": {"button_label": hero.get("button", "Shop now"),
                                                                            "button_link": product_link(),
                                                                            "button_style_secondary": False}}},
                            "block_order": ["h", "t", "b"],
                            "settings": {"desktop_content_position": "center", "content_alignment": "center",
                                         "color_scheme": "scheme-2", "full_width": True,
                                         "padding_top": 72, "padding_bottom": 72}}
    featured_text = get("home.featured_text", "")
    sections["product"] = {
        "type": "featured-product",
        "blocks": {"title": {"type": "title", "settings": {"heading_size": "h1"}},
                   "price": {"type": "price"},
                   "text": {"type": "text", "settings": {"text": featured_text, "text_style": "body"}},
                   # Send shoppers to the product page, where the bundle picker lives.
                   "cta": {"type": "custom_liquid", "settings": {"custom_liquid":
                       f"<a class=\"button button--full-width\" href=\"{{{{ section.settings.product.url }}}}\">"
                       f"{get('home.featured_button', 'Choose your bundle')}</a>"}}},
        "block_order": ["title", "price", "text", "cta"] if featured_text else ["title", "price", "cta"],
        "settings": {"product": B["product"]["handle"], "color_scheme": "scheme-1", "secondary_background": False,
                     "media_size": "medium", "constrain_to_viewport": True, "media_fit": "cover",
                     "media_position": "left", "image_zoom": "lightbox", "hide_variants": False,
                     "enable_video_looping": False, "padding_top": 48, "padding_bottom": 48}}
    for key, sec in [("benefits", benefits_section(color="scheme-2")), ("how", how_section(color="scheme-1"))]:
        if sec:
            sections[key] = sec
    for i, story in enumerate(get("stories", [])[2:], 3):
        sections[f"story-{i}"] = story_section(story, color="scheme-1" if i % 2 else "scheme-2")
    closing = closing_section()
    if closing:
        sections["closing"] = closing
    faq = get("faq", [])
    picks = [faq[i] for i in get("home.faq_indexes", list(range(min(5, len(faq))))) if i < len(faq)]
    home_faq = faq_section(picks, heading="Good to know", color="scheme-2")
    if home_faq:
        sections["faq"] = home_faq
    nl = get("newsletter")
    if nl:
        sections["newsletter"] = {
            "type": "newsletter",
            "blocks": {"h": {"type": "heading", "settings": {"heading": nl["heading"], "heading_size": "h1"}},
                       "p": {"type": "paragraph", "settings": {"text": para(nl["text"])}},
                       "f": {"type": "email_form"}},
            "block_order": ["h", "p", "f"],
            "settings": {"color_scheme": "scheme-3", "full_width": True, "padding_top": 48, "padding_bottom": 56}}
        if nl.get("welcome_code"):
            # Shows the code under Dawn's "Thanks for subscribing" message after a signup.
            sections["welcome_code"] = {"type": "custom-liquid", "settings": {
                "custom_liquid": welcome_code_liquid(nl["welcome_code"], nl.get("code_label", "Your welcome code")),
                "color_scheme": "scheme-3", "padding_top": 0, "padding_bottom": 0}}
    write("templates/index.json", {"sections": sections, "order": list(sections)})


# ---------------------------------------------------------------- pages
def page_templates():
    about = {"main": {"type": "main-page", "settings": {"padding_top": 36, "padding_bottom": 24}}}
    ben = benefits_section()
    if ben:
        about["benefits"] = ben
    write("templates/page.about.json", {"sections": about, "order": list(about)})

    faq = {"main": {"type": "main-page", "settings": {"padding_top": 36, "padding_bottom": 0}}}
    sec = faq_section(get("faq", []), heading="Frequently asked questions")
    if sec:
        faq["faq"] = sec
    write("templates/page.faq.json", {"sections": faq, "order": list(faq)})

    how = how_section()
    if how:
        page = {"main": {"type": "main-page", "settings": {"padding_top": 36, "padding_bottom": 12}}, "how": how}
        write("templates/page.how-it-works.json", {"sections": page, "order": list(page)})


def header_group():
    comment, data = read_json("sections/header-group.json")
    bar = data["sections"]["announcement-bar"]
    bar["settings"].update({"color_scheme": "scheme-3", "auto_rotate": True, "change_slides_speed": 5})
    bar["blocks"] = {f"a{i}": {"type": "announcement", "settings": {"text": t, "link": ""}}
                     for i, t in enumerate(get("announcements", []), 1)}
    bar["block_order"] = list(bar["blocks"])
    header = data["sections"].get("header", {}).setdefault("settings", {})
    header.update({"enable_country_selector": get("header.country_selector", True),
                   "menu": "main-menu", "sticky_header_type": "on-scroll-up"})
    write("sections/header-group.json", data, comment)


def footer_group():
    comment, data = read_json("sections/footer-group.json")
    footer = data["sections"]["footer"]
    email = B["brand"]["support_email"]
    reply = get("brand.reply_time", "within 1 business day")
    footer["blocks"] = {
        "brand": {"type": "brand_information", "settings": {"show_social": True}},
        "links": {"type": "link_list", "settings": {"heading": "Help", "menu": "footer"}},
        "contact": {"type": "text", "settings": {"heading": "Contact us", "subtext":
            f"<p>Questions about your order? Email <a href=\"mailto:{email}\">{email}</a>. We reply {reply}.</p>"}},
    }
    footer["block_order"] = ["brand", "links", "contact"]
    # The home page has its own newsletter section; avoid a second signup box.
    footer["settings"].update({"newsletter_enable": not bool(get("newsletter")), "color_scheme": "scheme-2",
                               "enable_follow_on_shop": False})
    write("sections/footer-group.json", data, comment)


REQUIRED = ["brand.name", "brand.support_email", "colors.background", "colors.surface", "colors.text",
            "colors.primary", "colors.primary_text", "colors.dark", "colors.dark_text",
            "product.handle", "hero.heading", "hero.text"]


def main():
    global B, THEME
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", default="brand/brand.json")
    ap.add_argument("--theme", default="theme")
    args = ap.parse_args()
    B = json.loads(Path(args.brand).read_text(encoding="utf-8"))
    THEME = Path(args.theme)
    missing = [k for k in REQUIRED if get(k) in (None, "")]
    if missing:
        print("LOI: brand.json thieu cac truong bat buoc:", ", ".join(missing))
        sys.exit(1)
    bad_icons = [i["icon"] for i in get("trust", []) + get("product.tabs", []) if i.get("icon", "check_mark") not in ICONS]
    if bad_icons:
        print("LOI: icon khong hop le:", ", ".join(bad_icons), "\nIcon hop le:", " ".join(sorted(ICONS)))
        sys.exit(1)
    if get("style.radius", "rounded") not in RADIUS:
        print("LOI: style.radius phai la rounded, soft hoac sharp")
        sys.exit(1)
    if not (THEME / "snippets/bundle-picker.liquid").exists():
        print("LOI: chua cai kit. Chay install_kit.py (hoac new_theme.py) truoc.")
        sys.exit(1)
    print(f"Building {B['brand']['name']} into {THEME}/")
    check_contrast()
    settings()
    product_template()
    index_template()
    page_templates()
    header_group()
    footer_group()
    print("Xong. Tiep theo: shopify theme check --path", THEME)


if __name__ == "__main__":
    main()
