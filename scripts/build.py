from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
NAV = (("Services", "services/"), ("States", "states/"), ("Providers", "providers/"),
       ("Resources", "resources/"))
FOOT = (("About", "about/"), ("Contact", "contact/"), ("Privacy", "privacy/"))
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
GROUPS = {"services": "Services", "states": "State Guides", "providers": "Providers", "resources": "Resources"}
LAYOUTS = {
    "services": "overview",
    "states": "states",
    "providers": "providers",
    "how-it-works": "process",
    "resources": "resources",
    "about": "info",
    "contact": "info",
    "privacy": "info",
}
SERVICE_LINKS = (
    ("LLC Formation", "Prepare the filing and compare what a formation package includes.", "services/llc-formation/", "◇"),
    ("Registered Agent", "Find a provider and compare ongoing costs and service terms.", "services/registered-agent/", "◎"),
    ("EIN Assistance", "Get your information ready and find the official IRS instructions.", "services/ein-assistance/", "▤"),
)
STATE_LINKS = (
    ("Wyoming", "Articles of Organization, registered agent and annual reporting.", "states/wyoming/", "WY"),
    ("Delaware", "Certificate of Formation, registered agent and ongoing obligations.", "states/delaware/", "DE"),
    ("Texas", "Certificate of Formation, local permits and franchise tax guidance.", "states/texas/", "TX"),
)


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


def links(entries, prefix, active=""):
    return "".join(
        f'<a href="{prefix}{url}"'
        + (' aria-current="page"' if active == url else "")
        + f'>{escape(label)}</a>' for label, url in entries
    )


def render_block(block, prefix):
    if isinstance(block, list):
        return "<ul>" + "".join(f"<li>{inline(line, prefix)}</li>" for line in block) + "</ul>"
    return f"<p>{inline(block, prefix)}</p>"


def section(item, prefix, index, class_name="article-section"):
    title, *body = item
    words = "".join(render_block(block, prefix) for block in body)
    return f'<section class="{class_name}" id="section-{index}"><h2>{escape(title)}</h2>{words}</section>'


def hub_cards(entries, prefix):
    return '<div class="services hub-cards">' + "".join(
        f'<a class="service" href="{prefix}{url}"><span class="service-icon" aria-hidden="true">{escape(icon)}</span>'
        f'<h2>{escape(title)}</h2><p>{escape(summary)}</p><span class="card-link">View details <span aria-hidden="true">↗</span></span></a>'
        for title, summary, url, icon in entries
    ) + '</div>'


def layout(slug, entry, prefix):
    sections = entry["sections"]
    mode = LAYOUTS.get(slug, "detail")
    if mode == "overview":
        return hub_cards(SERVICE_LINKS, prefix) + section(sections[-1], prefix, 4)
    if mode == "states":
        directory = f'''<section class="directory" data-state-directory data-home="{prefix}"><div class="section-head"><div>
          <h2>Find your state</h2><p>Choose any state to prefill your setup checklist.</p></div>
          <label for="state-search">Search by state<input id="state-search" type="search" placeholder="e.g. Wyoming"></label></div>
          <ul class="directory-grid"></ul><p role="status" class="search-status"></p></section>'''
        return hub_cards(STATE_LINKS, prefix) + directory + section(sections[-1], prefix, 3)
    if mode == "providers":
        cards = []
        for index, (title, description) in enumerate(sections[:-1], 1):
            match = LINK.search(description)
            body = description[match.end():].strip().lstrip(".").strip()
            href = escape(match.group(2), quote=True)
            mark = "".join(part[0] for part in title.split())[:2].upper()
            cards.append(f'''<article class="provider-card"><span class="provider-mark" aria-hidden="true">{escape(mark)}</span>
              <h2>{escape(title)}</h2><p>{escape(body)}</p><a class="card-link" href="{href}">Visit provider <span aria-hidden="true">↗</span></a></article>''')
        return '<div class="provider-grid">' + ''.join(cards) + '</div>' + section(sections[-1], prefix, 6)
    if mode in {"process", "resources", "info"}:
        return f'<div class="content-grid {mode}-grid">' + "".join(
            section(item, prefix, index, "content-card") for index, item in enumerate(sections, 1)
        ) + "</div>"

    index_links = "".join(f'<a href="#section-{index}">{escape(item[0])}</a>' for index, item in enumerate(sections, 1))
    body = "".join(section(item, prefix, index) for index, item in enumerate(sections, 1))
    index = (f'<aside class="article-index"><h2>On this page</h2><nav aria-label="On this page">{index_links}</nav>'
             f'<a class="button" href="{prefix}#setup">Build a Checklist <span aria-hidden="true">↗</span></a></aside>')
    return '<div class="detail-layout"><div class="article-main">' + body + "</div>" + index + "</div>"


def page(slug, entry):
    prefix = "../" * len(slug.split("/"))
    title = escape(entry["title"])
    intro = escape(entry["intro"], quote=True)
    group = slug.split("/")[0]
    parent = f' <span aria-hidden="true">/</span> <a href="{prefix}{group}/">{GROUPS[group]}</a>' if "/" in slug else ""
    nav = links(NAV, prefix, group + "/")
    foot = links(FOOT, prefix, slug + "/")
    body = layout(slug, entry, prefix)
    extra_script = f'<script src="{prefix}directory.js" defer></script>' if slug == "states" else ""
    callout = ""
    if slug != "privacy" and "/" not in slug:
        callout = (f'<section class="inner-callout"><div><h2>Plan your next step.</h2>'
                   f'<p>Build a checklist for the state and service you’re considering.</p></div>'
                   f'<a class="button light-button" href="{prefix}#setup">Build a Checklist <span aria-hidden="true">↗</span></a></section>')
    brand = f'<a class="brand" href="{prefix}" aria-label="Renz home"><img src="{prefix}mark.svg" alt="" width="32" height="30">Renz</a>'
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Renz</title><meta name="description" content="{intro}">
<meta name="theme-color" content="#14243e">
<link rel="stylesheet" href="{prefix}styles.css"><link rel="icon" href="{prefix}mark.svg" type="image/svg+xml">
{extra_script}</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container navigation">{brand}
<nav aria-label="Main navigation">{nav}</nav>
<a class="button header-action" href="{prefix}#setup">Build a Checklist <span aria-hidden="true">↗</span></a></div></header>
<main id="main"><div class="article-hero"><div class="container">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="{prefix}">Home</a>{parent}</nav>
<h1>{title}</h1><p>{intro}</p></div></div>
<div class="container article">{body}{callout}</div></main>
<footer class="footer"><div class="container footer-layout"><div>{brand}<p>U.S. business setup and provider guidance.</p></div>
<nav aria-label="Footer services">{links(NAV,prefix)}</nav><nav aria-label="About Renz">{foot}</nav></div></footer>
</body></html>
"""


for slug, entry in DATA.items():
    path = DOCS / slug / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(slug, entry), encoding="utf-8")
(DOCS / "index.html").write_text((ROOT / "homepage.html").read_text(encoding="utf-8"), encoding="utf-8")
