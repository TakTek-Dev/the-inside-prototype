"""Every page but the front page and the identity book.

python -I tools/pages.py   (after build.py)

entry/<id>.html for each story; a page per section; the count, the names, the election desk;
archive by day; method, about, the letter, search (+ assets/data/search.json), credits, 404.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # python -I drops the script dir

import json
import os
from collections import OrderedDict

import shell as sh
from shell import C, E, S, PH, esc, day, gate, link, fig, photo, thumb, icon, SEC, SECTIONS

import build as B

CT = E['count']
ORDER = sorted(S, key=lambda k: (S[k]['date'], S[k].get('weight', 0)), reverse=True)


def ar(t):
    """Arabic source titles read right to left."""
    return ' lang="ar" dir="rtl" class="ar"' if any('؀' <= c <= 'ۿ' for c in t) else ''


def crumbs(*items):
    out = [f'<a href="{C.R}home.html">Front page</a>']
    for label, href in items:
        out.append(f'<span><a href="{href}">{esc(label)}</a></span>' if href else f'<span>{esc(label)}</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(out)}</nav>'


def sheet(ids, head=True):
    rows = ''.join(B.entry(sid, 'minor' if not S[sid].get('photo') else '') for sid in ids)
    h = ('<div class="cols colhead" aria-hidden="true"><div class="lbl">No.</div><div class="lbl vr">Date</div>'
         '<div class="lbl vr mg">Entry</div><div class="lbl vr c4">Source</div></div>') if head else ''
    return h + rows


def entry_no(s):
    """Register number: year · folio of the day · position that day."""
    same = [k for k in ORDER if S[k]['date'] == s['date']]
    return f'2026·{sh.folio(sh.D(s["date"])):03d}·{same.index(s["id"]) + 1:02d}'


# ---------------------------------------------------------------- entry pages
def entry_page(sid):
    s = S[sid]
    k = s['section']
    no = (f'<div class="e-no">{esc(str(s["n"]))}<small>{esc(s.get("nlabel", "count on the day"))}</small></div>' if s.get('n')
          else f'<div class="e-no blank">—<small>{esc(s.get("nlabel", "no count that day"))}</small></div>')
    body = ''.join(f'<p>{esc(p)}</p>' for p in s['body'])
    figs = ''.join(f'<li><b>{esc(f["v"])}</b><span>{esc(f["label"])}</span></li>' for f in s.get('figures', []))
    people = ''.join(f'<li><b>{esc(p["name"])}</b><span>{esc(p["role"])}</span></li>' for p in s.get('people', []))
    srcs = ''.join(f'<li><a href="{esc(a["url"])}" rel="noopener"{ar(a["title"])}>{esc(a["title"])}</a><span class="src">{esc(a["outlet"])}, {day(a["date"], year=True)}</span></li>'
                   for a in s['sources'])
    rel = [x for x in ORDER if x != sid and S[x]['section'] == k][:3]
    if len(rel) < 3:
        rel += [x for x in ORDER if x != sid and x not in rel][:3 - len(rel)]
    rel_html = ''.join(f'<li><a href="{link(x)}">{esc(S[x]["headline"])}</a><span class="src">{esc(SEC[S[x]["section"]][1])} · {day(S[x]["date"])}</span></li>' for x in rel)
    pic = fig(s.get('photo'), sizes='(max-width:720px) 100vw, 680px', eager=True)
    html = f'''<div class="wrap">
{crumbs((SEC[k][2], f"{C.R}{k}.html"), ("Entry " + entry_no(s), None))}
<header class="page-h" style="border-bottom:0;padding-bottom:0">
<p class="lbl"><a href="{C.R}{k}.html">{esc(SEC[k][1])}</a><span>{esc(s["place"])}</span><span>{sh.long_day(s["date"])}</span></p>
<h1>{esc(s["headline"])}</h1>
<p class="dek">{esc(s["dek"])}</p>
</header>
<div class="story">
<aside class="l">{no}<dl><div><dt>Entry</dt><dd class="fig">{entry_no(s)}</dd></div><div><dt>Date</dt><dd>{day(s["date"], year=True)}</dd></div><div><dt>Place</dt><dd>{esc(s["place"])}</dd></div><div><dt>Status</dt><dd style="display:flex;gap:8px;align-items:center">{gate(bool(s.get("verified", True)))}{"Entered" if s.get("verified", True) else "Reported"}</dd></div></dl></aside>
<article class="body">{pic}{body}
{f'<ul class="facts" style="margin-top:30px">{figs}</ul>' if figs else ''}
<p class="corr">{gate()}<span>Entered {day(s["date"], year=True)}. If a figure in this entry changes, the old one stays visible, struck through, with the new one and its date beside it. <a href="{C.R}method.html">How we correct</a>.</span></p>
</article>
<aside class="r">
<div class="box"><h2>Sources</h2><ul>{srcs}</ul></div>
{f'<div class="box people"><h2>Named in this entry</h2><ul>{people}</ul></div>' if people else ''}
<div class="box"><h2>The count</h2><ul><li><a href="{C.R}count.html"><b class="fig" style="font-size:30px;color:var(--red);font-weight:850">{CT["n"]}</b></a><span class="src">Killed in crime and violence in 2026, as of {day(CT["asof"])}.</span></li></ul></div>
</aside>
</div>
<div class="related"><div class="sec-h" style="padding-top:28px"><h2>Entered nearby</h2></div><div class="box" style="border:0;padding:0"><ul>{rel_html}</ul></div></div>
</div>'''
    return sh.page(s['headline'], s['dek'], html, current=k)


# ---------------------------------------------------------------- section pages
def section_page(k):
    _, tab, title, stand = SEC[k]
    ids = [x for x in ORDER if S[x]['section'] == k]
    chips = ''.join(f'<a class="chip" href="{C.R}{s}.html"{" aria-current=\"page\"" if s == k else ""}>{esc(l)} <span class="n">{sum(1 for x in S if S[x]["section"] == s)}</span></a>' for s, l, *_ in SECTIONS)
    extra = ''
    if k == 'elections':
        extra = B.board().replace('<p style="margin-top:26px"><a class="btn" href="' + C.R + 'elections.html">The election desk ' + icon('i-right') + '</a></p>', '')
    lead = ''
    first = next((x for x in ids if S[x].get('photo')), None)
    if first:
        s = S[first]
        lead = (f'<div class="split" style="padding-bottom:10px"><div>{fig(s["photo"], sizes="(max-width:1100px) 100vw, 60vw", eager=True)}</div>'
                f'<div><p class="lbl">Latest · {day(s["date"])} · {esc(s["place"])}</p><h2 style="margin-top:10px;font:700 30px/1.1 var(--serif);letter-spacing:-.012em"><a href="{link(first)}" style="text-decoration:none">{esc(s["headline"])}</a></h2>'
                f'<p style="margin-top:12px;color:var(--ink2)">{esc(s["dek"])}</p><p style="margin-top:16px"><a class="btn" href="{link(first)}">Read the entry {icon("i-right")}</a></p></div></div>')
    body = f'''<div class="wrap">{crumbs((title, None))}
<header class="page-h"><p class="lbl">{gate()}<b>Section</b><span>{len(ids)} entries since {day(S[ids[-1]]["date"]) if ids else ""}</span></p><h1>{esc(title)}</h1><p class="dek">{esc(stand)}</p></header>
<div class="filters" role="navigation" aria-label="Sections">{chips}</div>
{lead}</div>{extra}<div class="wrap" style="margin-top:{'40px' if extra else '10px'}">{sheet(ids)}</div>'''
    return sh.page(title, stand, body, current=k)


# ---------------------------------------------------------------- the count
def count_page():
    ups = ''.join(f'<tr{" class=turn" if i == 0 else ""}><td>{day(u["asof"], year=True)}</td><td class="k">{esc(str(u["n"]))}</td><td>{esc(str(u.get("y25") or "—"))}</td>'
                  f'<td style="text-align:left">{esc(u.get("source", ""))}</td></tr>' for i, u in enumerate(CT['updates']))
    years = ''.join(f'<tr><td>{y["y"]}</td><td class="k">{y["n"]}</td><td style="text-align:left">{esc(y["note"])}</td></tr>' for y in CT['years'])
    body = f'''<div class="wrap">{crumbs(("The Count", None))}</div>
{B.count_block().replace('<h1 class="num"', '<p class="num"').replace('</h1>', '</p>', 1).replace('aria-labelledby="count-h"', 'aria-label="The count"')}
<div class="wrap"><header class="page-h" style="border-bottom:0;padding-bottom:0"><h1>The count, and every time it changed</h1>
<p class="dek">We keep one count: The Abraham Initiatives’ tally of Arab citizens and permanent residents of Israel killed in crime and violence, including by police. Each update it publishes is entered here as published. When a number moves, the earlier one stays on the record.</p></header>
<div class="split"><div><table class="tbl"><caption class="lbl">Published updates, newest first</caption><thead><tr><th scope="col">As of</th><th scope="col">2026</th><th scope="col">2025, same date</th><th scope="col" style="text-align:left">Reported by</th></tr></thead><tbody>{ups}</tbody></table>
<table class="tbl" style="margin-top:40px"><caption class="lbl">The years before</caption><thead><tr><th scope="col">Year</th><th scope="col">Killed</th><th scope="col" style="text-align:left">Note</th></tr></thead><tbody>{years}</tbody></table></div>
<aside><div class="box"><h2>What the count includes</h2><ul><li>Citizens and permanent residents, Arab, killed in crime and violence anywhere in Israel, including East Jerusalem residents and people killed by police gunfire.</li><li>Deaths that happen later in hospital are added on the date of the update that records them.</li><li>Other monitors count differently. Where they disagree we name the source; we never average.</li></ul></div>
<p style="margin-top:22px"><a class="btn" href="{C.R}method.html">Method and corrections {icon("i-right")}</a></p></aside></div></div>
{B.climb()}{B.register()}'''
    return sh.page('The Count', CT['lede'], body, current='index')


# ---------------------------------------------------------------- names
def names_page():
    groups = ''
    for g in E['named']:
        lis = ''.join(f'<li><b>{esc(p["name"])}</b><span>{esc(p["meta"])}</span></li>' for p in g['people'])
        groups += f'<div class="ev" style="padding:0 0 30px"><p class="lbl red">{esc(g["label"])}</p><p class="ctx">{esc(g["ctx"])}</p><ul>{lis}</ul><p class="src">{esc(g["src"])}</p></div>'
    total = sum(len(g['people']) for g in E['named'])
    body = f'''<div class="wrap">{crumbs(("Names", None))}
<header class="page-h"><p class="lbl">{gate()}<b>The register of names</b><span>{total} names published in reports we could verify</span></p><h1>The names behind the count</h1>
<p class="dek">People whose names were published in news reports, with age and town as reported and what was reported about how they died. The list is not complete: most killings are reported without a name, and families sometimes ask that none be printed. No photographs.</p></header>
<div class="split"><div class="evs" style="grid-template-columns:repeat(2,minmax(0,1fr));gap:0 34px">{groups}</div>
<aside><div class="box"><h2>Why names</h2><ul><li>A ledger that keeps only totals forgets who was in it.</li><li>We print a name only when a news report printed it first, and we link that report.</li><li>Ask for a correction or a removal through the method page.</li></ul></div></aside></div></div>'''
    return sh.page('Names', 'The names behind the count, as published in news reports.', body, current='index')


# ---------------------------------------------------------------- archive by day
def archive_page():
    by = OrderedDict()
    for x in ORDER:
        by.setdefault(S[x]['date'], []).append(x)
    days = ''
    for d, ids in by.items():
        days += (f'<section aria-labelledby="d-{d}"><div class="sec-h" style="padding-top:34px"><h2 id="d-{d}" style="font-size:26px">{sh.long_day(d)}</h2>'
                 f'<p class="fig">Folio {sh.folio(sh.D(d))} · {len(ids)} {"entry" if len(ids) == 1 else "entries"}</p></div>{sheet(ids, head=False)}</section>')
    body = f'''<div class="wrap">{crumbs(("Archive", None))}
<header class="page-h"><p class="lbl">{gate()}<b>The journal</b><span>{len(S)} entries</span></p><h1>Every entry, by day</h1><p class="dek">The register in the order it was kept: newest day first, each day with its folio number.</p></header>
{days}</div>'''
    return sh.page('Archive', 'Every entry in the record, by day.', body)


# ---------------------------------------------------------------- utility pages
def method_page():
    body = f'''<div class="wrap">{crumbs(("Method and corrections", None))}
<header class="page-h"><p class="lbl">{gate()}<b>Method</b></p><h1>Whose count, and how we correct it</h1><p class="dek">One count, named sources, and corrections that leave the old figure on the record.</p></header>
<div class="split"><div class="prose">
<h2>One count</h2><p>We keep The Abraham Initiatives’ tally of Arab citizens and permanent residents of Israel killed in crime and violence, including people killed by police. We enter each update on the day it is published, with the outlet that reported it. Other monitors count differently; where they disagree we name the source and never average.</p>
<h2>Since the last count</h2><p>Shootings and deaths reported after the latest update sit in the band marked with the open gate. A death enters the count only when the watchdog counts it.</p>
<h2>The No. column</h2><p>Every entry carries, in its first column, the count on the day it happened. If no count was published that day, or the story is not about a killing, the column stays blank.</p>
<h2>Corrections</h2><p>We never overwrite. A changed figure is struck through once, in red, with the new figure and its date beside it. A correction note sits at the foot of the entry.</p>
<h2>Names</h2><p>We print a name only after a news report has, link that report, and print no photographs of the dead.</p>
<h2>Photographs</h2><p>All photographs come from Wikimedia Commons under free licences, are shown in their own colour and are captioned with place, date, photographer and licence. A photograph appears only with a story it shows.</p>
</div><aside><div class="box"><h2>The three states</h2><ul><li style="display:flex;gap:12px;align-items:center">{gate(False)}Reported, not yet entered</li><li style="display:flex;gap:12px;align-items:center">{gate()}Entered and sourced</li><li style="display:flex;gap:12px;align-items:center"><span class="fig" style="position:relative;color:var(--ink3);font-weight:800">181<span style="position:absolute;left:-3px;right:-3px;top:50%;height:2px;background:var(--red);transform:rotate(-9deg)"></span></span>Corrected</li></ul></div></aside></div></div>'''
    return sh.page('Method and corrections', 'How The Inside – Palestine keeps its count and corrects it.', body)


def about_page():
    body = f'''<div class="wrap">{crumbs(("About", None))}
<header class="page-h"><p class="lbl">{gate()}<b>About</b></p><h1>The Inside</h1><p class="dek">“The Inside”, al-Dakhil, is what Palestinians call the Palestinian citizens of Israel: about a fifth of the country’s population, in the Galilee, the Triangle, the Naqab and the mixed cities.</p></header>
<div class="split"><div class="prose"><p>This is a design prototype for an English-language site that covers them as a record: the count of the killed on the front page, every story entered against it, and the life of the towns alongside.</p>
<p>The prototype was built by TakTek. No newsroom, staff, readership, funders or partners exist or are implied. Every story on these pages was written from published reports, which are linked on each entry; they were checked on {day(sh.TODAY, year=True)}.</p>
<p><a href="{C.R}index.html">Read how the identity was made</a>.</p></div>
<aside><div class="box"><h2>Contact</h2><ul><li>[CONTACT EMAIL]</li><li>[SOCIAL LINKS]</li></ul></div></aside></div></div>'''
    return sh.page('About', 'About The Inside – Palestine, a design prototype.', body)


def letter_page():
    body = f'''<div class="wrap">{crumbs(("The daily ledger", None))}
<header class="page-h"><p class="lbl">{gate()}<b>The letter</b></p><h1>The daily ledger</h1><p class="dek">The count and the day’s entries, each morning at 07:00. One email, no tracking pixels.</p></header>
<div class="split"><form class="letter-f" action="#" method="post" data-proto>
<label for="em-l">Email address</label><input id="em-l" type="email" name="email" autocomplete="email" required placeholder="you@example.com">
<p class="lbl" style="margin-top:8px">Also send me</p>
<label class="opt"><input type="checkbox" name="election" checked> The election count, 27–30 October</label>
<label class="opt"><input type="checkbox" name="weekly"> The week in the towns, Fridays</label>
<button class="btn solid" type="submit" style="justify-self:start;margin-top:8px">Subscribe</button><p class="msg note" role="status"></p></form>
<aside><div class="box"><h2>What a morning looks like</h2><ul><li><b class="fig" style="color:var(--red);font-size:22px">{CT["n"]}</b> The count, and whether it moved.</li><li>Since the last count: what has been reported.</li><li>The day’s entries, each with its source.</li></ul></div></aside></div></div>'''
    return sh.page('The daily ledger', 'Subscribe to the daily ledger.', body)


def search_page():
    body = f'''<div class="wrap">{crumbs(("Search", None))}
<header class="page-h"><p class="lbl">{gate()}<b>Search</b><span>{len(S)} entries</span></p><h1>Search the record</h1>
<form class="search-f" data-search="{C.R}" role="search"><label class="vh" for="q">Search entries</label><input id="q" type="search" name="q" placeholder="A town, a name, a court…" autocomplete="off"><button class="btn solid" type="submit">{icon("i-search")}Search</button></form></header>
<div class="results" aria-live="polite"></div></div>'''
    return sh.page('Search', 'Search the record.', body)


def credits_page():
    used = sorted({S[x]['photo'] for x in S if S[x].get('photo')} | set(E.get('extra_photos', [])))
    rows = ''.join(f'<li>{photo(p, cls="th", sizes="120px")}<div><b>{esc(PH[p]["caption"])}</b><span class="src">{esc(PH[p]["author"])} · {esc(PH[p]["license"])} · <a href="{esc(PH[p]["page_url"])}">Wikimedia Commons</a></span></div></li>' for p in used if p in PH)
    body = f'''<div class="wrap">{crumbs(("Credits", None))}
<header class="page-h"><p class="lbl">{gate()}<b>Credits</b></p><h1>Photographs and type</h1><p class="dek">Every photograph is from Wikimedia Commons under a free licence, shown in its own colour. Type: Andada Pro (Huerta Tipográfica) and Pathway Extreme (Eduardo Tunni), both SIL Open Font License.</p></header>
<ul class="credits-l">{rows}</ul></div>
<style>.credits-l{{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:0 34px;margin-top:20px}}.credits-l li{{display:grid;grid-template-columns:120px minmax(0,1fr);gap:16px;padding:14px 0;border-bottom:1px solid var(--feint)}}.credits-l .th{{width:120px;aspect-ratio:4/3;border-radius:var(--r1);overflow:hidden}}.credits-l .th img{{width:100%;height:100%;object-fit:cover}}.credits-l b{{display:block;font-size:15.5px;line-height:1.4}}</style>'''
    return sh.page('Credits', 'Photograph and type credits.', body)


def notfound_page():
    body = f'''<div class="wrap nf">{gate(False, label="An open gate: nothing entered here")}
<h1>Nothing has been entered here</h1><p>The page you asked for is not in the register. It may have moved, or the address may be mistyped.</p>
<div class="acts"><a class="btn solid" href="{C.R}home.html">The front page</a><a class="btn" href="{C.R}search.html">Search the record</a><a class="btn" href="{C.R}archive.html">Every entry by day</a></div></div>'''
    return sh.page('Not found', 'Page not found.', body)


def search_index():
    out = []
    for x in ORDER:
        s = S[x]
        out.append({'t': s['headline'], 'd': s['dek'], 'p': s['place'], 's': SEC[s['section']][1], 'dt': day(s['date']),
                    'u': f'entry/{x}.html', 'n': s.get('n'), 'i': f'assets/img/photo/{s["photo"]}.webp' if s.get('photo') else ''})
    p = os.path.join(sh.ROOT, 'assets', 'data', 'search.json')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False)


def main():
    C.R = '../'
    for sid in S:
        S[sid]['id'] = sid
    for sid in S:
        sh.write(f'entry/{sid}.html', entry_page(sid))
    C.R = ''
    for k, *_ in SECTIONS:
        sh.write(f'{k}.html', section_page(k))
    sh.write('count.html', count_page())
    sh.write('names.html', names_page())
    sh.write('archive.html', archive_page())
    sh.write('method.html', method_page())
    sh.write('about.html', about_page())
    sh.write('letter.html', letter_page())
    sh.write('search.html', search_page())
    sh.write('credits.html', credits_page())
    C.R = '/the-inside-prototype/'
    sh.write('404.html', notfound_page())
    C.R = ''
    search_index()
    print(len(S), 'entries +', len(SECTIONS), 'sections + 9 pages')


if __name__ == '__main__':
    main()
