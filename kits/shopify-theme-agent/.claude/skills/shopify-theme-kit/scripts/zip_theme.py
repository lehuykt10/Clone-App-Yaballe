#!/usr/bin/env python3
"""Zip the theme folder for Shopify Admin → Online Store → Themes → Add theme → Upload zip file.

Use this when `shopify theme push` fails (network/SSL errors on some PCs).

Usage:
    python .claude/skills/shopify-theme-kit/scripts/zip_theme.py [--theme theme] [--out dist/theme.zip]
"""
import argparse
import zipfile
from pathlib import Path

FOLDERS = ("assets", "blocks", "config", "layout", "locales", "sections", "snippets", "templates")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", default="theme")
    ap.add_argument("--out", default="dist/theme.zip")
    args = ap.parse_args()
    theme, out = Path(args.theme), Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for folder in FOLDERS:
            for f in sorted((theme / folder).rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(theme).as_posix())
                    count += 1
    print(f"Da tao {out} ({count} file). Upload trong Shopify Admin > Online Store > Themes > Add theme > Upload zip file.")


if __name__ == "__main__":
    main()
