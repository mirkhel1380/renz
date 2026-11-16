from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))

NAV = (("Services", "services/"), ("States", "states/"), ("How It Works", "how-it-works/"),
       ("Resources", "resources/"), ("Providers", "providers/"))
FOOT = (("About", "about/"), ("Contact", "contact/"), ("Privacy", "privacy/"))
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

def inline(text, prefix):
    pieces = []
    start = 0
    for match in LINK.finditer(text):
        pieces.append(escape(text[start:match.start()]))
        label, href = match.groups()
        if not href.startswith("https://"):
            href = prefix + href
        pieces.append(f'<a href="{escape(href, quote=True)}">{escape(label)}</a>')
        start = match.end()
    pieces.append(escape(text[start:]))
    return "".join(pieces)

def links(entries, prefix):
    return "".join(f'<a href="{prefix}{url}">{escape(label)}</a>' for label, url in entries)

def section(item, prefix):
    title, *body = item
    output = [f'<section class="article-section"><h2>{escape(title)}</h2>']
    for block in body:
        if isinstance(block, list):
            output.append("<ul>" + "".join(f"<li>{inline(line, prefix)}</li>" for line in block) + "</ul>")
        else:
            output.append(f"<p>{inline(block, prefix)}</p>")
    return "\n".join(output) + "\n</section>"

def page(slug, entry):
    prefix = "../" * len(slug.split("/"))
    title = escape(entry["title"])
    intro = escape(entry["intro"])
    nav = links(NAV, prefix)
    foot = links(FOOT, prefix)
    sections = "\n".join(section(item, prefix) for item in entry["sections"])
    signup = "" if slug in {"privacy", "contact"} else f'<aside class="article-cta"><a class="button" href="{prefix}#setup">Build a setup checklist <span aria-hidden="true">→</span></a></aside>'
    brand = f'<a class="brand" href="{prefix}" aria-label="Renz home"><img src="{prefix}mark.svg" alt="" width="32" height="30">Renz</a>'
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Renz</title><meta name="description" content="{intro}">
<meta name="theme-color" content="#14243e">
<link rel="stylesheet" href="{prefix}styles.css"><link rel="icon" href="{prefix}mark.svg" type="image/svg+xml">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container navigation">{brand}
<nav aria-label="Main navigation">{nav}</nav>
<a class="button header-action" href="{prefix}#setup">Setup Checklist</a></div></header>
<main id="main"><div class="article-hero"><div class="container">
<a class="breadcrumb" href="{prefix}">Home</a>
<h1>{title}</h1><p>{intro}</p></div></div>
<div class="container article">{sections}{signup}</div></main>
<footer class="footer"><div class="container footer-inner">{brand}<nav aria-label="Footer navigation">{foot}</nav></div></footer>
</body></html>
"""

for slug, entry in DATA.items():
    path = DOCS / slug / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(slug, entry), encoding="utf-8")
(DOCS / "index.html").write_text((ROOT / "homepage.html").read_text(encoding="utf-8"), encoding="utf-8")
