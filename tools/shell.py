"""The page shell every built page shares: head, binding strip, masthead, tabs, footer, loader.

Imported by build.py (home) and pages.py (everything else). R is the path back to the site
root; pages in folders set it to '../', the 404 page to the absolute site path.
"""
import datetime as dt
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = '4'                                       # bump on any asset change (Chrome caches hard)
SITE = 'The Inside – Palestine'
BASE_URL = 'https://taktek-dev.github.io/the-inside-prototype/'
E = json.load(open(os.path.join(ROOT, 'tools', 'edition.json'), encoding='utf-8'))
MARKS = json.load(open(os.path.join(ROOT, 'tools', 'out', 'marks.json'), encoding='utf-8'))
PH = json.load(open(os.path.join(ROOT, 'tools', 'photos.json'), encoding='utf-8'))
DIM_P = os.path.join(ROOT, 'tools', 'out', 'photos.json')
DIM = json.load(open(DIM_P, encoding='utf-8')) if os.path.exists(DIM_P) else {}
esc = html.escape
D = dt.date.fromisoformat
TODAY = D(E['date'])
S = E['stories']


class Ctx:
    R = ''


C = Ctx()

SECTIONS = [  # slug, tab label, page title, standfirst
    ('police', 'Police', 'Police and crime', 'Killings, raids and arrests, and how the police and the Shin Bet answer for them.'),
    ('government', 'Government', 'Government', 'Budgets, plans and ministers’ decisions that reach Arab towns, followed to where the money goes.'),
    ('courts', 'Courts', 'Courts', 'Sentences, rulings and petitions, from magistrates’ courts to the Supreme Court.'),
    ('elections', 'Election', 'The 2026 election', 'The Knesset election of 27 October: the Arab lists, the polls, the turnout and the rulings that shaped the ballot.'),
    ('rights', 'Rights', 'Rights, land and housing', 'Demolitions, the unrecognised villages of the Naqab, laws, arrests over speech and the fight over land.'),
    ('protest', 'Protest', 'Protest', 'Strikes, marches and vigils, and what they asked for.'),
    ('roads', 'Roads', 'Roads', 'The second count: deaths on the roads in Arab towns and on the roads that lead to them.'),
    ('life', 'Life', 'Life in the towns', 'Schools, hospitals, work, culture and sport: the record is not only of the dead.'),
]
SEC = {s[0]: s for s in SECTIONS}


def day(d, year=False, wd=False):
    d = D(d) if isinstance(d, str) else d
    s = f"{d.day} {d.strftime('%b')}" + (f" {d.year}" if year else '')
    return (d.strftime('%a') + ' ' + s) if wd else s


def long_day(d):
    d = D(d) if isinstance(d, str) else d
    return f"{d.strftime('%A')} {d.day} {d.strftime('%B')} {d.year}"


def folio(d=None):
    d = d or TODAY
    return d.timetuple().tm_yday


# ---------------------------------------------------------------- icons and marks
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-right" viewBox="0 0 16 16"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-search" viewBox="0 0 16 16"><path d="M7 2.5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9zM10.4 10.4 14 14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></symbol>
<symbol id="i-out" viewBox="0 0 16 16"><path d="M6 3.5H3.5v9h9V10M9 3h4v4M13 3 7.5 8.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</defs></svg>'''


def icon(name, cls='ic'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'


def gate(closed=True, label=None, cls='gate'):
    """The gate as a small inline icon in the current text colour (open = reported, closed = entered)."""
    g = MARKS['gate']
    s = ''.join(f'<path class="s" d="M{x} {g["top"]}V{g["foot"]}" stroke-width="{g["w"]}"/>' for x in g['strokes'])
    r = ''
    if closed:
        x0, y0, x1, y1 = g['rule']
        d = f'M{x0} {y0}L{x1} {y1}'
        r = (f'<path class="h" d="{d}" stroke-width="{g["w"] + g["halo"]}"/>'
             f'<path class="r" d="{d}" stroke-width="{g["w"]}"/>')
    a = f'role="img" aria-label="{esc(label)}"' if label else 'aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="0 0 64 64" {a}>{s}{r}</svg>'


def tally_svg(n):
    """One tally group of n strokes (1–5) for the field; 5 is a closed gate."""
    xs = [4, 10, 16, 22]
    s = ''.join(f'<path class="s" d="M{x} 3V23"/>' for x in xs[:min(n, 4)])
    if n >= 5:
        s += '<path class="h" d="M1 19.5L27 7"/><path class="r" d="M1 19.5L27 7"/>'
    return f'<svg viewBox="0 0 28 26" aria-hidden="true">{s}</svg>'


def wordmark(ink='currentColor', red=None, label=SITE):
    w, g = MARKS['wordmark'], MARKS['gate']
    red = red or 'var(--red)'
    k, gx, gy = w['gk'], w['gx'], w['gy']
    t = lambda v, o: f'{o + v * k:.2f}'
    strokes = ''.join(f'<path d="M{t(x, gx)} {t(g["top"], gy)}V{t(g["foot"], gy)}"/>' for x in g['strokes'])
    x0, y0, x1, y1 = g['rule']
    rd = f'M{t(x0, gx)} {t(y0, gy)}L{t(x1, gx)} {t(y1, gy)}'
    r = w['rule']
    return (f'<svg viewBox="0 0 {w["w"]} {w["h"]}" role="img" aria-label="{esc(label)}">'
            f'<g class="gate-g"><g fill="none" stroke="{ink}" stroke-width="{g["w"] * k:.2f}" stroke-linecap="round">{strokes}</g>'
            f'<path d="{rd}" fill="none" stroke="var(--halo,var(--paper))" stroke-width="{(g["w"] + g["halo"]) * k:.2f}" stroke-linecap="round"/>'
            f'<path d="{rd}" fill="none" stroke="{red}" stroke-width="{g["w"] * k:.2f}" stroke-linecap="round"/></g>'
            f'<path d="{w["the"]}" fill="{ink}"/><path d="{w["pal"]}" fill="{ink}"/>'
            f'<path d="M{r[0]} {r[1]}H{r[2]}" stroke="{red}" stroke-width="{w["rw"]}" stroke-linecap="round"/></svg>')


# ---------------------------------------------------------------- photographs
def photo(slug, sizes='100vw', cls='ph', eager=False):
    if not slug or slug not in PH:
        return ''
    p = PH[slug]
    dm = DIM.get(slug, {'w': 1000, 'h': 667})
    pos = f' style="object-position:{p["focus"]}"' if p.get('focus') else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<div class="{cls}"><img src="{C.R}assets/img/photo/{slug}.webp?v={V}" width="{dm["w"]}" height="{dm["h"]}" '
            f'alt="{esc(p["alt"])}" sizes="{sizes}" {load}{pos}></div>')


def caption(slug):
    p = PH[slug]
    return f'<figcaption>{esc(p["caption"])} Photo: {esc(p["author"])}, {esc(p["license"])}, Wikimedia Commons.</figcaption>'


def fig(slug, cls='ph r169', **kw):
    img = photo(slug, cls=cls, **kw)
    return f'<figure>{img}{caption(slug)}</figure>' if img else ''


def thumb(slug, cls='th'):
    return photo(slug, sizes='170px', cls=cls) if slug else ''


def link(sid):
    return f'{C.R}entry/{sid}.html'


# ---------------------------------------------------------------- the shell
def head(title, desc, path='', og=None):
    t = esc(title if title == SITE else f'{title} · {SITE}')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0E2424">
<link rel="icon" href="{C.R}favicon.svg?v={V}" type="image/svg+xml">
<link rel="preload" href="{C.R}assets/fonts/andada.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{C.R}assets/fonts/pathway.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{C.R}assets/css/ti.css?v={V}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE_URL}{og or 'assets/og.png'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="noindex">
</head>
<body>
<a class="skip" href="#main">Skip to the record</a>
{SPRITE}'''


def strip():
    el = E['election']
    days = (D(el['date']) - TODAY).days
    when = 'today' if days == 0 else ('tomorrow' if days == 1 else f'in {days} days')
    return (f'<div class="strip"><div class="wrap"><span><b>{long_day(TODAY)}</b></span>'
            f'<a class="elx" href="{C.R}elections.html"><i aria-hidden="true"></i>Knesset election {when} · {day(el["date"], wd=True)}</a>'
            f'<span class="sp"></span><span class="fol">Folio {folio()} of the 2026 register</span></div></div>')


def mast(current=''):
    tabs = [('index', 'The Count', f'{C.R}count.html')] + [(s, l, f'{C.R}{s}.html') for s, l, *_ in SECTIONS]
    lis = ''.join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if k == current else ""}{" class=\"el\"" if k == "elections" else ""}>'
        f'{gate() if k == "index" else ""}{esc(l)}</a></li>' for k, l, u in tabs)
    return f'''<header class="mast">
<div class="wrap">
<div class="top">
<div><a class="brand" href="{C.R}home.html" aria-label="{SITE}, front page">{wordmark()}</a>
<p class="motto">News of Palestinian citizens of Israel, kept as a record. Corrected, never <s>erased</s>.</p></div>
<div class="tools"><a class="btn icon" href="{C.R}search.html" aria-label="Search the record">{icon("i-search")}</a><a class="btn" href="{C.R}letter.html">The daily ledger</a></div>
</div>
<nav class="tabs" aria-label="Sections"><ul>{lis}</ul></nav>
</div>
</header>'''


def loader():
    g = MARKS['gate']
    s = ''.join(f'<path class="s" d="M{x} {g["top"]}V{g["foot"]}"/>' for x in g['strokes'])
    x0, y0, x1, y1 = g['rule']
    d = f'M{x0} {y0}L{x1} {y1}'
    return (f'<div class="ldr" aria-hidden="true"><div class="in"><svg viewBox="0 0 64 64">{s}'
            f'<path class="h" d="{d}"/><path class="r" d="{d}"/></svg>'
            f'<p>Entered · <b>{day(TODAY, year=True)}</b></p></div></div>')


def foot():
    secs = ''.join(f'<li><a href="{C.R}{s}.html">{esc(t)}</a></li>' for s, _, t, _ in SECTIONS[:5])
    secs2 = ''.join(f'<li><a href="{C.R}{s}.html">{esc(t)}</a></li>' for s, _, t, _ in SECTIONS[5:])
    return f'''<footer class="foot">
<div class="wrap">
<div><a class="brand" href="{C.R}home.html" aria-label="{SITE}, front page" style="--halo:var(--cloth)">{wordmark(ink="var(--onc)", red="var(--red-on)")}</a>
<p style="margin-top:16px;max-width:44ch">News of Palestinian citizens of Israel, the people the Arab press calls the Inside, kept as a record: every story entered against the count, every figure sourced, every correction left legible.</p></div>
<div><p class="lbl">The daily ledger</p><p style="margin-top:6px">The count and the day’s entries, each morning at 07:00.</p>
<form class="sub" action="#" method="post" data-proto><label for="em-f">Email address</label><input id="em-f" name="email" type="email" placeholder="you@example.com" autocomplete="email" required><button type="submit">Subscribe</button><p class="msg" role="status"></p></form></div>
<div><p class="lbl">Sections</p><ul><li><a href="{C.R}count.html">The Count</a></li>{secs}</ul></div>
<div><p class="lbl">The register</p><ul>{secs2}<li><a href="{C.R}names.html">Names</a></li><li><a href="{C.R}archive.html">Archive by day</a></li><li><a href="{C.R}method.html">Method and corrections</a></li><li><a href="{C.R}about.html">About</a></li><li><a href="{C.R}index.html">Identity</a></li></ul></div>
</div>
<div class="credits"><div class="wrap"><span>Design prototype by TakTek. Not a live site: no newsroom, readership or partners are implied.</span><span>Type: Andada Pro and Pathway Extreme (OFL). Photographs: Wikimedia Commons, <a href="{C.R}credits.html">credited here</a>.</span></div></div>
</footer>'''


def page(title, desc, body, current='', with_loader=False, og=None):
    return (head(title, desc, og=og) + (loader() if with_loader else '') + strip() + mast(current) +
            f'<main id="main">{body}</main>' + foot() +
            f'<script src="{C.R}assets/js/ti.js?v={V}" defer></script>\n</body>\n</html>\n')


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
