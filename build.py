"""Assemble the case study.

- index.html  : full document for GitHub Pages
- preview.html: body-only version for the hosted preview (wrapped by the host)
Also adds width/height and lazy loading to every <img> so layout doesn't shift.
"""
import re
from pathlib import Path
from PIL import Image

root = Path(__file__).parent
src = root / "src"
head = (src / "head.html").read_text()
body = (src / "body.html").read_text()
script = (src / "script.html").read_text()

hero_srcs = set()
hero_srcs = set(re.findall(r'<img src="([^"]+)"', body)[:5])  # hero mockups + slider load eagerly


def add_dims(m):
    tag = m.group(0)
    path = re.search(r'src="([^"]+)"', tag).group(1)
    w, h = Image.open(root / path).size
    extra = f' width="{w}" height="{h}" decoding="async"'
    if path not in hero_srcs:
        extra += ' loading="lazy"'
    return tag[:-1] + extra + ">"


body = re.sub(r'<img src="assets/[^"]+"[^>]*>', add_dims, body)
inner = head + "\n" + body + "\n" + script

(root / "preview.html").write_text(inner)
(root / "index.html").write_text(
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + head + "\n</head>\n<body>\n" + body + "\n" + script + "</body>\n</html>\n"
)
print("built", len(inner), "chars")
