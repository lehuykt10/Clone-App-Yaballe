#!/usr/bin/env python3
"""Build the student kit: render the Vietnamese guide to HTML and zip the kit.

    pip install markdown
    python kits/build_kit.py            → kits/shopify-theme-agent/HUONG-DAN.html + dist/shopify-theme-agent.zip
"""
import zipfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
KIT = ROOT / "shopify-theme-agent"
DIST = ROOT.parent / "dist"
TOP_SKIP = {"theme", "dist"}  # generated per project, only at the kit root
SKIP_DIRS = {"node_modules", "__pycache__", ".git"}

CSS = """
:root{--bg:#fbf9f6;--panel:#ffffff;--text:#1f2328;--muted:#5b6470;--line:#e4e0da;--accent:#2f6f5e;--accent-bg:#e7f2ee;--code:#f3f0eb;--warn:#fff6e0}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#15171a;--panel:#1c1f23;--text:#e8e6e3;--muted:#a3a9b1;--line:#30343a;--accent:#7cc7b0;--accent-bg:#1f332d;--code:#23272c;--warn:#3a3220}}
:root[data-theme=dark]{--bg:#15171a;--panel:#1c1f23;--text:#e8e6e3;--muted:#a3a9b1;--line:#30343a;--accent:#7cc7b0;--accent-bg:#1f332d;--code:#23272c;--warn:#3a3220}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{display:grid;grid-template-columns:280px minmax(0,1fr);gap:40px;max-width:1240px;margin:0 auto;padding:32px 24px}
nav{position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);overflow:auto;font-size:14px}
nav .toc ul{list-style:none;padding-left:0;margin:0}
nav .toc ul ul{padding-left:14px}
nav a{color:var(--muted);text-decoration:none;display:block;padding:3px 0}
nav a:hover{color:var(--accent)}
nav .brand{font-weight:700;color:var(--text);margin-bottom:12px;font-size:15px}
main{min-width:0;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:40px 48px}
h1{font-size:30px;line-height:1.25;margin-top:0}
h2{font-size:23px;margin-top:48px;padding-top:12px;border-top:1px solid var(--line)}
h3{font-size:18px;margin-top:32px}
a{color:var(--accent)}
hr{display:none}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:15px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--accent-bg)}
code{background:var(--code);padding:2px 6px;border-radius:5px;font-size:.92em;font-family:ui-monospace,Consolas,Menlo,monospace}
pre{background:var(--code);padding:14px 16px;border-radius:10px;overflow-x:auto;position:relative}
pre code{background:none;padding:0}
blockquote{margin:16px 0;padding:10px 16px;background:var(--warn);border-left:4px solid #d9a23a;border-radius:6px}
blockquote p{margin:6px 0}
details{background:var(--code);border-radius:10px;padding:10px 16px;margin:16px 0}
summary{cursor:pointer;font-weight:600}
.copy{position:absolute;top:8px;right:8px;font-size:12px;border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:6px;padding:3px 8px;cursor:pointer}
.theme-toggle{margin-top:16px;font-size:13px;border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:6px;padding:4px 10px;cursor:pointer}
@media (max-width:900px){.wrap{grid-template-columns:1fr;padding:16px}nav{position:static;max-height:none;border:1px solid var(--line);border-radius:12px;padding:12px 16px;background:var(--panel)}main{padding:24px 18px}}
"""

JS = """
document.querySelectorAll('pre').forEach(function(pre){var b=document.createElement('button');b.className='copy';b.textContent='Copy';
b.onclick=function(){navigator.clipboard.writeText(pre.innerText.replace(/^Copy\\n?/,'')).then(function(){b.textContent='Da copy';setTimeout(function(){b.textContent='Copy'},1500)})};pre.appendChild(b)});
var t=document.querySelector('.theme-toggle');t.onclick=function(){var r=document.documentElement;var dark=r.dataset.theme==='dark'||(!r.dataset.theme&&matchMedia('(prefers-color-scheme: dark)').matches);r.dataset.theme=dark?'light':'dark';try{localStorage.setItem('theme',r.dataset.theme)}catch(e){}};
try{var s=localStorage.getItem('theme');if(s)document.documentElement.dataset.theme=s}catch(e){}
"""


def build_html():
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "md_in_html", "sane_lists"],
                           extension_configs={"toc": {"toc_depth": "2-3"}})
    body = md.convert((KIT / "docs/HUONG-DAN.md").read_text(encoding="utf-8"))
    html = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hướng dẫn AI Agent Shopify</title><style>{CSS}</style></head>
<body><div class="wrap"><nav><div class="brand">AI Agent Thiết Kế Theme Shopify</div>{md.toc}
<button class="theme-toggle" type="button">Sáng / Tối</button></nav>
<main>{body}</main></div><script>{JS}</script></body></html>
"""
    (KIT / "HUONG-DAN.html").write_text(html, encoding="utf-8")
    print("wrote", KIT / "HUONG-DAN.html")


def build_zip():
    DIST.mkdir(exist_ok=True)
    out = DIST / "shopify-theme-agent.zip"
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(KIT.rglob("*")):
            rel = f.relative_to(KIT)
            if f.is_dir() or SKIP_DIRS & set(rel.parts[:-1]) or (len(rel.parts) > 1 and rel.parts[0] in TOP_SKIP):
                continue
            if f.name in {"PROGRESS.md", ".DS_Store"} or f.suffix == ".pyc":
                continue
            info = zipfile.ZipInfo.from_file(f, ("shopify-theme-agent" / rel).as_posix())
            if f.suffix in {".sh"}:
                info.external_attr = 0o755 << 16
            with open(f, "rb") as fh:
                z.writestr(info, fh.read(), zipfile.ZIP_DEFLATED)
            count += 1
    print(f"wrote {out} ({count} files)")


if __name__ == "__main__":
    build_html()
    build_zip()
