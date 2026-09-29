#!/usr/bin/env python3
"""Install the Shopify Theme Kit into a Dawn theme folder.

Copies the kit's sections/snippets and patches sections/main-product.liquid so
the product page gets a "Bundle picker" block. Safe to run more than once.

Usage:
    python install_kit.py <theme-folder>
    python install_kit.py theme
"""
import json
import re
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent / "theme"
RENDER = """                {%- when 'bundle_picker' -%}
                  {%- render 'bundle-picker',
                    block: block,
                    product: product,
                    product_form_id: product_form_id,
                    section_id: section.id
                  -%}
"""


def fail(msg):
    print(f"LOI: {msg}")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail("cach dung: python install_kit.py <thu-muc-theme>")
    theme = Path(sys.argv[1]).resolve()
    main_product = theme / "sections/main-product.liquid"
    if not main_product.exists():
        fail(f"khong thay {main_product}. Thu muc theme phai la theme Dawn (co sections/main-product.liquid).")

    for sub in ("sections", "snippets"):
        for src in sorted((KIT / sub).glob("*.liquid")):
            shutil.copy2(src, theme / sub / src.name)
            print(f"  copied {sub}/{src.name}")

    text = main_product.read_text(encoding="utf-8")
    if "'bundle_picker'" not in text:
        anchor = "                {%- when 'buy_buttons' -%}"
        if anchor not in text:
            fail("khong tim thay block 'buy_buttons' trong main-product.liquid (phien ban Dawn khac?).")
        text = text.replace(anchor, RENDER + anchor, 1)
        print("  patched main-product.liquid: render bundle_picker")

    m = re.search(r"{%\s*schema\s*%}(.*?){%\s*endschema\s*%}", text, re.S)
    if not m:
        fail("khong doc duoc {% schema %} cua main-product.liquid")
    schema = json.loads(m.group(1))
    if not any(b.get("type") == "bundle_picker" for b in schema.get("blocks", [])):
        block = json.loads((KIT / "main-product-bundle-block.json").read_text(encoding="utf-8"))
        schema["blocks"].append(block)
        new_schema = "{% schema %}\n" + json.dumps(schema, indent=2, ensure_ascii=False) + "\n{% endschema %}"
        text = text[: m.start()] + new_schema + text[m.end():]
        print("  patched main-product.liquid: schema block 'Bundle picker'")

    main_product.write_text(text, encoding="utf-8")
    print("Xong: da cai Shopify Theme Kit vao", theme)


if __name__ == "__main__":
    main()
