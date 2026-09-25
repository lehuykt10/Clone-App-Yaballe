#!/usr/bin/env python3
"""Install this skill's sections/snippets into a Dawn-based theme.

Usage: python3 install_sections.py <theme-dir>

- Copies theme/sections/*.liquid and theme/snippets/*.liquid into the theme.
- Patches sections/main-product.liquid to add a `quantity_breaks` block
  (render case + schema entry). Safe to run more than once.
"""
import json
import re
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SRC = SKILL / "theme"

RENDER_CASE = """                {%- when 'quantity_breaks' -%}
                  {%- render 'quantity-breaks',
                    block: block,
                    product: product,
                    product_form_id: product_form_id,
                    section_id: section.id
                  -%}
"""


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    theme = Path(sys.argv[1]).resolve()
    main_product = theme / "sections" / "main-product.liquid"
    if not main_product.exists():
        print(f"Not a Dawn-based theme (missing {main_product})")
        return 1

    for kind in ("sections", "snippets"):
        for f in sorted((SRC / kind).glob("*.liquid")):
            shutil.copy2(f, theme / kind / f.name)
            print(f"copied {kind}/{f.name}")

    src = main_product.read_text()
    if "'quantity_breaks'" in src:
        print("main-product.liquid already patched")
        return 0

    # 1. Render case, inserted just before the buy buttons case.
    anchor = "                {%- when 'buy_buttons' -%}\n"
    if anchor not in src:
        print("Could not find the buy_buttons block in main-product.liquid; patch it by hand.")
        return 1
    src = src.replace(anchor, RENDER_CASE + anchor, 1)

    # 2. Schema entry appended to the section's blocks.
    m = re.search(r"\{% schema %\}(.*)\{% endschema %\}", src, re.S)
    schema = json.loads(m.group(1))
    schema["blocks"].append(json.loads((SRC / "main-product-block.json").read_text()))
    new_schema = json.dumps(schema, indent=2, ensure_ascii=False)
    src = src[: m.start(1)] + "\n" + new_schema + "\n" + src[m.end(1) :]

    main_product.write_text(src)
    print("patched sections/main-product.liquid (quantity_breaks block)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
