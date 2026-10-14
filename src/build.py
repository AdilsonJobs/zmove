#!/usr/bin/env python3
"""Builds the Z-Move site from src/.

  index.html, pt/index.html   the one-page site in English and Portuguese (src/content.json)
  privacy.html, terms.html    the legal pages (src/legal/*.html, English only)
  blog/, case-studies/, compare/   redirects from the pages the old site had
  sitemap.xml, site.webmanifest

Edit src/content.json (EN and PT side by side, so both languages keep the same content) or the
templates below, then run:  python3 src/build.py
Only the Python standard library is needed. Amplify publishes the repository as it is.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SITE = "https://zmove.click"
UPDATED = "2026-10-14"
FORMSPREE = "https://formspree.io/f/mwvykwlq"
C = json.loads((SRC / "content.json").read_text(encoding="utf-8"))


def e(value):
    return html.escape(str(value), quote=True)


def svg(path_d, size=20, stroke=1.8, cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path_d}{extra}</svg>')


# The Z-Move mark: the Z drawn as a route, from an origin station to a destination terminal.
def mark(size, bold=False):
    sw, ring, ring_w, end = (7.2, 5.6, 3.8, 7) if bold else (6, 5, 3.2, 6)
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true">'
            f'<rect width="64" height="64" rx="14" fill="#0A7A63"/>'
            f'<path d="M17 19H43L21 45H47" fill="none" stroke="#FFFFFF" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="17" cy="19" r="{ring}" fill="#0A7A63" stroke="#FFFFFF" stroke-width="{ring_w}"/>'
            f'<circle cx="47" cy="45" r="{end}" fill="#FFFFFF"/></svg>')


ARROW = svg('<path d="M5 12h14M13 6l6 6-6 6"/>', 18, 2)
MOON = svg('<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>', 20, 1.8, "ic-moon")
SUN = svg('<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4L6 18M18 6l1.4-1.4"/>', 20, 1.8, "ic-sun")
MENU = svg('<path d="M4 7h16M4 12h16M4 17h16"/>', 22, 1.8, "ic-menu")
CLOSE = svg('<path d="M6 6l12 12M18 6L6 18"/>', 22, 1.8, "ic-close")
ROUTE_ARROW = svg('<path d="M4 12h16M14 6l6 6-6 6"/>', 24, 1.8)
BOOT_OK = svg('<path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>', 20, 2, "ic-ok")
BOOT_INFO = svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>', 20, 2, "ic-info")
KNOB = svg('<path d="M9 7l-5 5 5 5M15 7l5 5-5 5"/>', 20, 2)
TICK = svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>', 13, 3)
CHECK = svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>', 16, 2.6)
PLUS = svg('<path d="M12 5v14M5 12h14"/>', 22, 1.8, "qa-ic")
SEC_ICONS = {
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2.5V6M15 2.5V6M9 18v3.5M15 18v3.5M2.5 9H6M2.5 15H6M18 9h3.5M18 15h3.5"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "user": '<circle cx="9" cy="8" r="4"/><path d="M2.5 21c0-3.6 2.9-6.5 6.5-6.5 1.4 0 2.7.4 3.8 1.2"/><path d="M15 18.5l2 2 4.5-4.5"/>',
    "server": '<rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/>',
}
CODES = {"zadara": "ZD", "aws": "AWS", "azure": "AZ"}
NAV = ["how", "routes", "providers", "security", "pricing", "faq"]
NAV_IDS = {"how": "how", "routes": "routes", "providers": "providers", "security": "security", "pricing": "pricing", "faq": "faq"}

# The CSP is also sent as an HTTP header by customHttp.yml (with frame-ancestors, which a meta tag cannot carry).
CSP = ("default-src 'self'; script-src 'self' https://plausible.io; style-src 'self'; font-src 'self'; "
       "img-src 'self' data:; connect-src 'self' https://plausible.io https://formspree.io; "
       "form-action 'self' https://formspree.io; manifest-src 'self'; base-uri 'self'; object-src 'none'; "
       "upgrade-insecure-requests")


def picture(name, lang, alt, sizes, eager=False):
    """A platform screenshot that follows the theme: the dark variant through <source>, which
    assets/site.js re-points when the visitor picks a theme by hand."""
    base = f"/assets/shots/{name}.{lang}"

    def srcset(theme):
        return f"{base}.{theme}.1440.webp 1440w, {base}.{theme}.webp 2880w"

    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source data-theme-dark media="(prefers-color-scheme: dark)" srcset="{srcset("dark")}" sizes="{sizes}">'
            f'<img src="{base}.light.1440.webp" srcset="{srcset("light")}" sizes="{sizes}" alt="{e(alt)}" '
            f'width="2880" height="1800" {load}></picture>')


def head(t, *, title, description, canonical, og_title, og_desc, og_image, og_alt, locale, alt_locale=None,
         alternates=True, jsonld=None):
    alt_links = ""
    if alternates:
        alt_links = (f'<link rel="alternate" hreflang="en" href="{SITE}/">\n'
                     f'<link rel="alternate" hreflang="pt" href="{SITE}/pt/">\n'
                     f'<link rel="alternate" hreflang="x-default" href="{SITE}/">\n')
    alt_locale_tag = f'<meta property="og:locale:alternate" content="{alt_locale}">\n' if alt_locale else ""
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"
                 for x in (jsonld or []))
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="Adilson Camenha">
<meta name="theme-color" content="#0D1921">
<link rel="canonical" href="{canonical}">
{alt_links}<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Z-Move">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{locale}">
{alt_locale_tag}<meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(og_desc)}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(og_title)}">
<meta name="twitter:description" content="{e(og_desc)}">
<meta name="twitter:image" content="{og_image}">
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/theme-init.js"></script>
<script src="/assets/site.js" defer></script>
<script defer data-domain="zmove.click" src="https://plausible.io/js/script.js"></script>
{ld}</head>
"""


def header(t, home):
    """home: "" on the one-page site (anchors stay on the page), "/" or "/pt/" elsewhere."""
    n = t["nav"]
    links = "\n".join(f'      <a href="{home}#{NAV_IDS[k]}">{e(n[k])}</a>' for k in NAV)
    m_links = "\n".join(f'    <a href="{home}#{NAV_IDS[k]}">{e(n[k])}</a>' for k in NAV)
    if t["lang"] == "en":
        lang = '<a href="/pt/" hreflang="pt" lang="pt">PT</a><span aria-current="true">EN</span>'
    else:
        lang = '<span aria-current="true">PT</span><a href="/" hreflang="en" lang="en">EN</a>'
    top = home or ""
    return f"""<body>
<a class="skip" href="#main">{e(t['skip'])}</a>
<header class="hdr" id="top">
  <div class="wrap hdr-in">
    <a class="logo" href="{top or '#'}{'' if top else 'top'}" aria-label="{e(n['home'])}">{mark(30)}<span>Z<span class="hy">-</span>Move</span></a>
    <nav class="nav" aria-label="{e(n['label'])}">
{links}
    </nav>
    <div class="hdr-r">
      <div class="lang" role="group" aria-label="{e(n['lang'])}">{lang}</div>
      <button type="button" class="icon-btn" data-theme-toggle data-to-dark="{e(n['toDark'])}" data-to-light="{e(n['toLight'])}" aria-label="{e(n['toDark'])}" title="{e(n['toDark'])}">{MOON}{SUN}</button>
      <a class="btn btn-primary btn-sm btn-demo" href="{home}#demo">{e(n['demo'])}</a>
      <button type="button" class="icon-btn menu-btn" data-menu-toggle data-open="{e(n['menu'])}" data-close="{e(n['close'])}" aria-expanded="false" aria-controls="m-nav" aria-label="{e(n['menu'])}">{MENU}{CLOSE}</button>
    </div>
  </div>
  <nav class="wrap m-nav" id="m-nav" aria-label="{e(n['label'])}" hidden>
{m_links}
    <a class="btn btn-primary" href="{home}#demo">{e(n['demo'])}</a>
  </nav>
</header>
"""


def footer(t):
    f = t["foot"]
    return f"""<footer class="ftr">
  <div class="wrap ftr-in">
    <div class="ftr-l">{mark(24, bold=True)}<span>{e(f['tag'])}</span></div>
    <div class="ftr-r">
      <a href="/privacy.html" hreflang="en">{e(f['privacy'])}</a>
      <a href="/terms.html" hreflang="en">{e(f['terms'])}</a>
      <span>© 2026 Z-Move</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def mail():
    return '<span data-mail data-u="hello" data-d="zmove.click" class="mail">hello [at] zmove.click</span>'


def jsonld(t):
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": t["lang"],
           "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                          for q in t["faq"]["items"]]}
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "Z-Move", "url": f"{SITE}/",
           "logo": f"{SITE}/assets/brand/icon-512.png", "email": "hello@zmove.click",
           "founder": {"@type": "Person", "name": "Adilson Camenha", "url": "https://www.linkedin.com/in/adilsoncamenha"},
           "sameAs": ["https://www.linkedin.com/in/adilsoncamenha"]}
    app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Z-Move", "url": t["url"],
           "inLanguage": t["lang"], "applicationCategory": "BusinessApplication", "operatingSystem": "Cloud (SaaS)",
           "description": t["meta"]["description"],
           "screenshot": f"{SITE}/assets/shots/session-done.{t['lang']}.light.webp",
           "offers": {"@type": "Offer", "price": "0.05", "priceCurrency": "USD", "description": t["price"]["p1"]["unit"]}}
    return [org, app, faq]


def home(lang):
    t = C[lang]
    h, how, rt, pv, sc, pr, fq, ct = (t[k] for k in ("hero", "how", "routes", "prov", "sec", "price", "faq", "cta"))
    m = t["meta"]
    out = [head(t, title=m["title"], description=m["description"], canonical=t["url"], og_title=m["ogTitle"],
                og_desc=m["ogDescription"], og_image=m["ogImage"], og_alt=m["ogAlt"], locale=m["locale"],
                alt_locale=m["altLocale"], jsonld=jsonld(t)),
           header(t, "")]
    wide = "(min-width: 1280px) 1200px, calc(100vw - 32px)"
    stage = "(min-width: 1280px) 680px, (min-width: 981px) 56vw, calc(100vw - 32px)"

    out.append(f"""<main id="main">
<section class="hero">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="wrap hero-in">
    <p class="eyebrow rise">{e(h['eyebrow'])}</p>
    <h1 class="h1 rise d1"><span class="h1a">{e(h['t1'])}</span> <span class="h1b">{e(h['t2'])}</span></h1>
    <p class="lead-d rise d2">{e(h['lead'])}</p>
    <div class="cta-row rise d3">
      <a class="btn btn-primary btn-lg" href="#demo"><span>{e(h['cta1'])}</span>{ARROW}</a>
      <a class="btn btn-ghost-d btn-lg" href="#how">{e(h['cta2'])}</a>
    </div>
  </div>
</section>

<section class="shot-sec" aria-label="{e(h['alt'])}">
  <div class="wrap">
    <div class="shot-box">
      <div class="shot-band" aria-hidden="true"></div>
      <figure class="shot">
        {picture('session-done', lang, h['alt'], wide, eager=True)}
        <span class="mk mk1" aria-hidden="true">1</span>
        <span class="mk mk2" aria-hidden="true">2</span>
        <span class="mk mk3" aria-hidden="true">3</span>
      </figure>
    </div>
    <ol class="legend">
      <li><span class="lg-n" aria-hidden="true">1</span><span>{e(h['c1'])}</span></li>
      <li><span class="lg-n" aria-hidden="true">2</span><span>{e(h['c2'])}</span></li>
      <li><span class="lg-n" aria-hidden="true">3</span><span>{e(h['c3'])}</span></li>
    </ol>
    <p class="shot-cap">{e(h['cap'])}</p>
  </div>
</section>

<section class="proof" aria-label="{e(t['proofLabel'])}">
  <div class="wrap">
    <div class="proof-grid">
""")
    for p in t["proof"]:
        out.append(f'      <div class="pf"><div class="pf-n">{e(p["n"])}</div><div class="pf-l">{e(p["l"])}</div></div>\n')
    out.append("""    </div>
  </div>
</section>
""")

    # How it works
    steps, shots = [], []
    for i, s in enumerate(how["steps"]):
        on = i == 0
        steps.append(f'        <button type="button" class="step{" is-on" if on else ""}" data-step="{i}" data-cap="{e(s["cap"])}" '
                     f'aria-pressed="{"true" if on else "false"}"><span class="st-n">{i + 1}</span><span class="st-b">'
                     f'<span class="st-t">{e(s["t"])}</span><span class="st-d">{e(s["d"])}</span></span></button>')
        shots.append(f'        <figure class="frame shot-l{" is-on" if on else ""}" data-step-shot="{i}">'
                     f'{picture(s["shot"], lang, s["alt"], stage)}</figure>')
    nl = "\n"
    out.append(f"""
<section id="how" class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow-l">{e(how['eyebrow'])}</p>
      <h2 class="h2">{e(how['title'])}</h2>
      <p class="lead">{e(how['lead'])}</p>
    </div>
    <div class="how">
      <div class="steps">
{nl.join(steps)}
      </div>
      <div class="stage">
{nl.join(shots)}
        <p class="stage-cap" id="step-cap">{e(how['steps'][0]['cap'])}</p>
      </div>
    </div>
  </div>
</section>
""")

    # Routes: rendered for Azure -> Zadara; site.js re-renders from the JSON below
    def seg(side, cur):
        return "".join(f'<button type="button" class="seg-b{" is-on" if c == cur else ""}" data-side="{side}" data-cloud="{c}" '
                       f'aria-pressed="{"true" if c == cur else "false"}"><span class="cc" aria-hidden="true">{CODES[c]}</span>'
                       f'<span>{e(rt["clouds"][c])}</span></button>' for c in ("zadara", "aws", "azure"))
    d = rt["data"]["azure>zadara"]
    readout = "".join(f'<div class="ro"><span class="ro-v">{e(v)}</span><span class="ro-k">{e(k)}</span></div>' for v, k in d["m"])
    data = {k: rt[k] for k in ("clouds", "status", "same", "none", "data")}
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out.append(f"""
<section id="routes" class="sec alt">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow-l">{e(rt['eyebrow'])}</p>
      <h2 class="h2">{e(rt['title'])}</h2>
      <p class="lead">{e(rt['lead'])}</p>
    </div>
    <div class="rp">
      <div class="rp-ctrl">
        <div class="rp-side">
          <span class="rp-lbl" id="rp-from">{e(rt['from'])}</span>
          <div class="seg" role="group" aria-labelledby="rp-from">{seg('from', 'azure')}</div>
        </div>
        <div class="rp-arrow" aria-hidden="true">{ROUTE_ARROW}</div>
        <div class="rp-side">
          <span class="rp-lbl" id="rp-to">{e(rt['to'])}</span>
          <div class="seg" role="group" aria-labelledby="rp-to">{seg('to', 'zadara')}</div>
        </div>
      </div>
      <div class="rp-res">
        <div class="rp-title rp-head" aria-live="polite">
          <h3 class="rp-route" id="rp-title">{e(rt['clouds']['azure'])} → {e(rt['clouds']['zadara'])}</h3>
          <span id="rp-status" class="pill pill-info">{e(rt['status'][d['st']])}</span>
        </div>
        <div class="rp-ok" id="rp-ok">
          <div class="rp-col">
            <div class="kv"><div class="kv-k">{e(rt['k']['how'])}</div><p class="kv-v" id="rp-how">{e(d['how'])}</p></div>
            <div class="kv"><div class="kv-k">{e(rt['k']['result'])}</div><p class="kv-v" id="rp-result">{e(d['result'])}</p></div>
            <div class="kv"><div class="kv-k">{e(rt['k']['os'])}</div><p class="kv-v" id="rp-os">{e(d['os'])}</p></div>
          </div>
          <div class="rp-col">
            <div class="kv-k">{e(rt['k']['measured'])}</div>
            <div class="readout" id="rp-readout">{readout}</div>
            <p class="rp-note" id="rp-note">{e(d['note'])}</p>
            <div class="boot is-ok" id="rp-bootbox">{BOOT_OK}{BOOT_INFO}<div><div class="kv-k">{e(rt['k']['boot'])}</div><div class="boot-v" id="rp-boot">{e(d['boot'])}</div></div></div>
          </div>
        </div>
        <div class="rp-none" id="rp-no" hidden>
          <p class="kv-v" id="rp-msg"></p>
          <a class="btn btn-ghost" href="#demo">{e(rt['ask'])}</a>
        </div>
      </div>
    </div>
    <script type="application/json" id="zm-routes">{data_json}</script>
  </div>
</section>
""")

    # Providers
    feats = "".join(f'<li><span class="tick" aria-hidden="true">{TICK}</span><span>{e(f)}</span></li>' for f in pv["feats"])
    stats = "".join(f'<div><div class="ref-n">{e(s["n"])}</div><div class="ref-k">{e(s["k"])}</div></div>' for s in pv["stats"])
    out.append(f"""
<section id="providers" class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow-l">{e(pv['eyebrow'])}</p>
      <h2 class="h2">{e(pv['title'])}</h2>
      <p class="lead">{e(pv['lead'])}</p>
    </div>
    <div class="cmp">
      {picture('overview', lang, pv['altA'], wide)}
      <div class="cmp-top">{picture('overview-acme', lang, pv['altB'], wide)}</div>
      <div class="cmp-line" aria-hidden="true"></div>
      <span class="cmp-tag l" aria-hidden="true">{e(pv['tagB'])}</span>
      <span class="cmp-tag r" aria-hidden="true">{e(pv['tagA'])}</span>
      <input id="brand-split" class="cmp-range" type="range" min="0" max="100" step="1" value="50" aria-label="{e(pv['drag'])}">
      <span class="cmp-knob" aria-hidden="true">{KNOB}</span>
    </div>
    <p class="cmp-cap">{e(pv['cap'])}</p>
    <ul class="feats">{feats}</ul>
    <div class="ref">
      <p class="ref-q">{e(pv['quote'])}</p>
      <div class="ref-stats">{stats}</div>
    </div>
    <div class="prov-cta"><a class="btn btn-primary btn-lg" href="#demo">{e(pv['cta'])}</a></div>
  </div>
</section>
""")

    # Security
    items = "".join(f'<div class="sec-item"><span class="sec-ic" aria-hidden="true">{svg(SEC_ICONS[i["icon"]], 22)}</span>'
                    f'<div><h3 class="sec-t">{e(i["t"])}</h3><p class="sec-d">{e(i["d"])}</p></div></div>' for i in sc["items"])
    out.append(f"""
<section id="security" class="sec alt">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow-l">{e(sc['eyebrow'])}</p>
      <h2 class="h2">{e(sc['title'])}</h2>
      <p class="lead">{e(sc['lead'])}</p>
    </div>
    <div class="sec-grid">{items}</div>
  </div>
</section>
""")

    # Pricing
    def plan(p, dark):
        lis = "".join(f"<li>{CHECK}<span>{e(i)}</span></li>" for i in p["items"])
        btn = "btn-primary" if dark else "btn-ghost"
        return (f'<div class="plan{" dark" if dark else ""}"><p class="plan-name">{e(p["name"])}</p>'
                f'<div class="price"><span class="price-v">{e(p["price"])}</span><span class="price-u">{e(p["unit"])}</span></div>'
                f'<p class="plan-d">{e(p["desc"])}</p><ul>{lis}</ul><a class="btn {btn}" href="#demo">{e(p["cta"])}</a></div>')
    out.append(f"""
<section id="pricing" class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow-l">{e(pr['eyebrow'])}</p>
      <h2 class="h2">{e(pr['title'])}</h2>
    </div>
    <div class="plans">{plan(pr['p1'], False)}{plan(pr['p2'], True)}</div>
  </div>
</section>
""")

    # FAQ
    qa = "".join(f'<details class="qa"><summary><span>{e(q["q"])}</span>{PLUS}</summary><p>{e(q["a"])}</p></details>' for q in fq["items"])
    out.append(f"""
<section id="faq" class="sec alt">
  <div class="wrap faq">
    <div>
      <p class="eyebrow-l">{e(fq['eyebrow'])}</p>
      <h2 class="h2">{e(fq['title'])}</h2>
      <p class="lead">{e(fq['lead'])} {mail()}</p>
    </div>
    <div>{qa}</div>
  </div>
</section>
""")

    # Demo
    out.append(f"""
<section id="demo" class="cta">
  <div class="wrap cta-grid">
    <div>
      <p class="eyebrow">{e(ct['eyebrow'])}</p>
      <h2 class="h2 h2-d">{e(ct['title'])}</h2>
      <p class="lead-c">{e(ct['lead'])}</p>
      <p class="cta-mail">{e(ct['alt'])} {mail()}</p>
    </div>
    <form class="form" id="demo-form" action="{FORMSPREE}" method="POST" data-msg-ok="{e(ct['ok'])}" data-msg-err="{e(ct['err'])}" data-msg-invalid="{e(ct['invalid'])}" data-msg-sending="{e(ct['sending'])}">
      <div class="row2">
        <div class="field"><label for="f-name">{e(ct['name'])}</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
        <div class="field"><label for="f-email">{e(ct['email'])}</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      </div>
      <div class="field"><label for="f-company">{e(ct['company'])}</label><input id="f-company" name="company" type="text" autocomplete="organization"></div>
      <div class="field"><label for="f-msg">{e(ct['msg'])}</label><textarea id="f-msg" name="message" placeholder="{e(ct['msgPh'])}"></textarea></div>
      <div class="hp" aria-hidden="true"><label for="f-gotcha">Leave empty</label><input id="f-gotcha" type="text" name="_gotcha" tabindex="-1" autocomplete="off"></div>
      <input type="hidden" name="page_lang" value="{lang}">
      <button type="submit" class="btn btn-primary btn-lg">{e(ct['send'])}</button>
      <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
      <p class="form-note">{e(ct['privacy'])}</p>
    </form>
  </div>
</section>
</main>
""")
    out.append(footer(t))
    return "".join(out)


def legal(name, title, description):
    t = C["en"]
    body = (SRC / "legal" / f"{name}.html").read_text(encoding="utf-8")
    return "".join([
        head(t, title=title, description=description, canonical=f"{SITE}/{name}.html", og_title=title, og_desc=description,
             og_image=f"{SITE}/og-image.png", og_alt=t["meta"]["ogAlt"], locale="en_US", alternates=False),
        header(t, "/"),
        f'<main id="main" class="doc">\n  <div class="wrap doc-in">\n    {body}  </div>\n</main>\n',
        footer(t),
    ])


# Pages of the old site: each now points at the part of the page that replaced it.
REDIRECTS = {
    "blog/index.html": "/#how",
    "blog/how-to-migrate-vms-from-aws-to-zadara/index.html": "/#routes",
    "case-studies/index.html": "/#providers",
    "case-studies/telecom-aws-to-zadara/index.html": "/#routes",
    "case-studies/telecom-sql-server/index.html": "/#providers",
    "case-studies/united-investment-sap-hana/index.html": "/#providers",
    "compare/zmove-vs-aws-mgn/index.html": "/",
    "compare/zmove-vs-zadara-migration-tools/index.html": "/",
}


def redirect(target):
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Z-Move</title>\n'
            f'<meta name="robots" content="noindex">\n<link rel="canonical" href="{SITE}{target}">\n'
            f'<meta http-equiv="refresh" content="0; url={target}">\n</head>\n<body>\n'
            f'<p><a href="{target}">Z-Move</a></p>\n</body>\n</html>\n')


def sitemap():
    def url(loc, freq, prio, alts=False):
        alt = ""
        if alts:
            alt = (f'\n    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/"/>'
                   f'\n    <xhtml:link rel="alternate" hreflang="pt" href="{SITE}/pt/"/>'
                   f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>')
        return (f"  <url>\n    <loc>{SITE}{loc}</loc>\n    <lastmod>{UPDATED}</lastmod>\n"
                f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>{alt}\n  </url>\n")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + url("/", "monthly", "1.0", True) + url("/pt/", "monthly", "0.9", True)
            + url("/privacy.html", "yearly", "0.3") + url("/terms.html", "yearly", "0.3") + "</urlset>\n")


MANIFEST = {
    "name": "Z-Move", "short_name": "Z-Move", "start_url": "/", "display": "browser",
    "background_color": "#0D1921", "theme_color": "#0D1921",
    "icons": [{"src": "/assets/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "/assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"}],
}


def main():
    files = {
        "index.html": home("en"),
        "pt/index.html": home("pt"),
        "privacy.html": legal("privacy", "Privacy Policy | Z-Move", "Z-Move Privacy Policy. How we collect, use and protect your data."),
        "terms.html": legal("terms", "Terms of Service | Z-Move", "Z-Move Terms of Service. Your use of the Z-Move cloud migration platform."),
        "sitemap.xml": sitemap(),
        "site.webmanifest": json.dumps(MANIFEST, indent=2) + "\n",
    }
    for path, target in REDIRECTS.items():
        files[path] = redirect(target)
    for path, content in files.items():
        p = ROOT / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
