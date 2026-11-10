"""Wraps page.html (artifact-preview format) into a standalone index.html for any static host."""
from pathlib import Path
src = Path(__file__).with_name("page.html").read_text()
head, body = src.split("</style>", 1)
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + "</style>\n</head>\n<body>\n" + body.strip() + "\n</body>\n</html>\n")
Path(__file__).with_name("index.html").write_text(out)
print("index.html written")
