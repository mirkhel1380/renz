from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
NAV = (
    ("Services", "services", (
        ("All Services", "services/"), ("LLC Formation", "services/llc-formation/"),
        ("Registered Agent", "services/registered-agent/"), ("EIN Assistance", "services/ein-assistance/"),
    )),
    ("States", "states", (
        ("All 50 States", "states/"), ("Wyoming", "states/wyoming/"),
        ("Delaware", "states/delaware/"), ("Texas", "states/texas/"),
    )),
    ("Providers", "providers", (
        ("Provider Directory", "providers/"), ("How to Compare", "providers/#section-1"),
        ("Questions to Ask", "providers/#section-2"),
    )),
    ("Resources", "resources", (
        ("Resource Library", "resources/"), ("How It Works", "how-it-works/"), ("Contact", "contact/"),
    )),
)
FOOT = (("About", "about/"), ("Contact", "contact/"), ("Privacy", "privacy/"))
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
GROUPS = {"services": "Services", "states": "State Guides", "providers": "Providers", "resources": "Resources", "blog": "Blog"}
LAYOUTS = {
    "services": "overview",
    "states": "states",
    "providers": "providers",
    "how-it-works": "process",
    "resources": "resources",
    "blog": "blog",
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


def brand(prefix):
    return (
        f'<a class="brand" href="{prefix}" aria-label="Renz home">'
        f'<img src="{prefix}mark.svg" alt="" width="36" height="36"><span>Renz</span></a>'
    )


def site_header(prefix, slug=""):
    current = slug + "/" if slug else ""
    menus = []
    for label, group, entries in NAV:
        is_current = slug.split("/")[0] == group or any(path == current for _, path in entries)
        active = ' class="nav-current"' if is_current else ""
        options = links(entries, prefix, current)
        menus.append(
            f'<details name="renz-primary"{active}><summary>{label}</summary>'
            f'<div class="nav-panel">{options}</div></details>'
        )
    blog_active = ' aria-current="page"' if slug == "blog" else ""
    blog_class = " nav-current-link" if slug.startswith("blog/") else ""
    menus.append(f'<a class="nav-link{blog_class}" href="{prefix}blog/"{blog_active}>Blog</a>')
    return f"""<header class="site-header" data-site-header><div class="container navigation">
  {brand(prefix)}
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="renz-navigation">
    <span class="menu-icon" aria-hidden="true"></span><span>Menu</span>
  </button>
  <nav id="renz-navigation" class="main-nav" aria-label="Main navigation">{"".join(menus)}</nav>
  <a class="button header-action" href="{prefix}#setup">Build a Checklist <span aria-hidden="true">→</span></a>
</div></header>"""


def site_footer(prefix, slug=""):
    return f"""<footer class="footer"><div class="container footer-layout">
  <div class="footer-intro">{brand(prefix)}
    <p>Renz helps founders plan U.S. company formation, compare registered agents, and prepare for EIN applications.</p>
  </div>
  <div class="footer-company"><h2>About &amp; Support</h2>
    <nav aria-label="About Renz">{links((*FOOT, ("Blog", "blog/")), prefix, slug + "/")}</nav>
  </div>
  <div class="footer-start"><h2>Ready to get started?</h2>
    <p>Choose a state and service to see your next steps.</p>
    <a href="{prefix}#setup">Build a Checklist <span aria-hidden="true">→</span></a>
  </div>
</div></footer>"""


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
        f'<h2>{escape(title)}</h2><p>{escape(summary)}</p><span class="card-link">View details <span aria-hidden="true">→</span></span></a>'
        for title, summary, url, icon in entries
    ) + '</div>'


def blog_card(slug, article, prefix, featured=False):
    variant = " blog-featured" if featured else ""
    heading = "h2" if featured else "h3"
    return f'''<article class="blog-card{variant}">
      <p class="section-label">{escape(article["category"])}</p>
      <{heading}><a href="{prefix}{slug}/">{escape(article["title"])}</a></{heading}>
      <p>{escape(article["intro"])}</p>
      <a class="card-link" href="{prefix}{slug}/" aria-label="Read {escape(article["title"], quote=True)}">Read article <span aria-hidden="true">→</span></a>
    </article>'''


def blog_index(prefix):
    posts = [(slug, entry) for slug, entry in DATA.items() if slug.startswith("blog/")]
    featured_slug, featured = posts[0]
    cards = "".join(blog_card(slug, article, prefix) for slug, article in posts[1:])
    return (
        blog_card(featured_slug, featured, prefix, featured=True)
        + '<section class="blog-latest"><h2>More from the blog</h2>'
        + f'<div class="blog-grid">{cards}</div></section>'
    )



def layout(slug, entry, prefix):
    sections = entry["sections"]
    mode = LAYOUTS.get(slug, "detail")
    if mode == "blog":
        return blog_index(prefix)
    if mode == "overview":
        return hub_cards(SERVICE_LINKS, prefix) + "".join(section(item, prefix, index) for index, item in enumerate(sections[3:], 4))
    if mode == "states":
        directory = f'''<section class="directory" data-state-directory data-home="{prefix}"><div class="section-head"><div>
          <h2>Find your state</h2><p>Choose any state to prefill your setup checklist.</p></div>
          <label for="state-search">Search by state<input id="state-search" type="search" placeholder="e.g. Wyoming"></label></div>
          <ul class="directory-grid"></ul><p role="status" class="search-status"></p></section>'''
        return hub_cards(STATE_LINKS, prefix) + directory + "".join(section(item, prefix, index) for index, item in enumerate(sections[2:], 3))
    if mode == "providers":
        cards = []
        for provider in entry["companies"]:
            title = escape(provider["name"])
            note = escape(provider["note"])
            href = escape(provider["url"], quote=True)
            logo = escape(provider["logo"], quote=True)
            cards.append(f'''<article class="provider-card">
              <div class="provider-heading">
                <span class="provider-logo"><img src="{prefix}assets/providers/{logo}" alt="" width="140" height="44" decoding="async"></span>
                <h2>{title}</h2>
              </div>
              <p>{note}</p>
              <a class="card-link" href="{href}">Visit provider <span aria-hidden="true">→</span></a>
            </article>''')
        guidance = "".join(section(item, prefix, index) for index, item in enumerate(sections, 1))
        return '<div class="provider-grid">' + "".join(cards) + "</div>" + guidance
    if mode in {"process", "resources", "info"}:
        return f'<div class="content-grid {mode}-grid">' + "".join(
            section(item, prefix, index, "content-card") for index, item in enumerate(sections, 1)
        ) + "</div>"

    index_links = "".join(f'<a href="#section-{index}">{escape(item[0])}</a>' for index, item in enumerate(sections, 1))
    body = "".join(section(item, prefix, index) for index, item in enumerate(sections, 1))
    index = (f'<aside class="article-index"><h2>On this page</h2><nav aria-label="On this page">{index_links}</nav>'
             f'<a class="button" href="{prefix}#setup">Build a Checklist <span aria-hidden="true">→</span></a></aside>')
    return '<div class="detail-layout"><div class="article-main">' + body + "</div>" + index + "</div>"


def page(slug, entry):
    prefix = "../" * len(slug.split("/"))
    title = escape(entry["title"])
    intro = escape(entry["intro"], quote=True)
    group = slug.split("/")[0]
    parent = f' <span aria-hidden="true">/</span> <a href="{prefix}{group}/">{GROUPS[group]}</a>' if "/" in slug else ""
    body = layout(slug, entry, prefix)
    category = entry.get("category")
    article_label = f'<p class="article-category">{escape(category)}</p>' if category else ""
    extra_script = f'<script src="{prefix}directory.js" defer></script>' if slug == "states" else ""
    callout = ""
    if slug.startswith("blog/"):
        callout = f'<p class="back-to-blog"><a class="text-link" href="{prefix}blog/">← All blog articles</a></p>'
    if slug not in {"privacy", "blog"} and "/" not in slug:
        callout = (f'<section class="inner-callout"><div><h2>Plan your next step.</h2>'
                   f'<p>Build a checklist for the state and service you’re considering.</p></div>'
                   f'<a class="button light-button" href="{prefix}#setup">Build a Checklist <span aria-hidden="true">→</span></a></section>')
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Renz</title><meta name="description" content="{intro}">
<meta name="theme-color" content="#14243e">
<link rel="stylesheet" href="{prefix}styles.css"><link rel="icon" href="{prefix}mark.svg" type="image/svg+xml">
<script src="{prefix}navigation.js" defer></script>{extra_script}</head><body>
<a class="skip" href="#main">Skip to content</a>
{site_header(prefix, slug)}
<main id="main"><div class="article-hero"><div class="container">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="{prefix}">Home</a>{parent}</nav>
{article_label}<h1>{title}</h1><p>{intro}</p></div></div>
<div class="container article">{body}{callout}</div></main>
{site_footer(prefix, slug)}
</body></html>
"""


for slug, entry in DATA.items():
    path = DOCS / slug / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(slug, entry), encoding="utf-8")
home = (ROOT / "homepage.html").read_text(encoding="utf-8")
home = home.replace("{{site-header}}", site_header("./")).replace("{{site-footer}}", site_footer("./"))
(DOCS / "index.html").write_text(home, encoding="utf-8")
