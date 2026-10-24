"""Compose tools/edition.json from research/news.json (+ tools/photo_map.json).

python -I tools/edition.py

research/news.json is the sourced research (every item checked against an opened page).
This script decides what the front page shows and in what order; it writes no facts of its own
beyond the framing sentences below, each of which restates a sourced figure.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = json.load(open(os.path.join(ROOT, 'research', 'news.json'), encoding='utf-8'))
PM_P = os.path.join(ROOT, 'tools', 'photo_map.json')
PMAP = json.load(open(PM_P, encoding='utf-8')) if os.path.exists(PM_P) else {}

DROP = {'haifa-man-dies-after-police-taser'}         # not confirmed that the man was Arab
COUNTED = ('police', 'government', 'protest', 'courts')

counts = sorted(N['counts'], key=lambda c: (c['as_of'], c['count']))
latest = counts[-1]


def count_on(d):
    """The latest published count on or before a date."""
    best = None
    for c in counts:
        if c['as_of'] <= d:
            best = c['count']
    return best


stories = {}
for it in N['items']:
    if it['id'] in DROP:
        continue
    s = {k: it[k] for k in ('date', 'section', 'place', 'headline', 'dek', 'body', 'people', 'sources')}
    s['figures'] = [{'v': f['value'], 'label': f['label']} for f in it.get('figures', [])]
    s['verified'] = it.get('confidence') == 'verified'
    if it['section'] in COUNTED and count_on(it['date']):
        s['n'] = count_on(it['date'])
    elif it['section'] == 'roads' and it['id'] == 'or-yarok-134-arab-road-deaths':
        s['n'], s['nlabel'] = 134, 'second ledger · roads'
    if it['id'] == 'aya-abu-hajjaj-killers-sentenced':
        s.pop('n', None)
        s['nlabel'] = 'case from 2023'
    if PMAP.get(it['id']):
        s['photo'] = PMAP[it['id']]
    stories[it['id']] = s

# the count -------------------------------------------------------------
b = latest['breakdown']
trail = [('100+', '2026-05-01'), ('152', '2026-07-05'), ('157', '2026-07-20'), ('181', '2026-09-25'),
         ('182', '2026-09-25'), ('183', '2026-10-10'), ('184', '2026-10-13'), (str(latest['count']), latest['as_of'])]
# spans between published counts: each row of the tally is one span, so every stroke is accounted for
spans = [('5 Feb', 37), ('26 Feb', 21), ('29 Mar', 19), ('1 May', 23), ('30 May', 18), ('29 Jun', 25),
         ('20 Jul', 14), ('4 Sep', 15), ('25 Sep', 10), ('23 Oct', 4)]
assert sum(n for _, n in spans) == latest['count'], 'spans must add up to the count'
pairs = [(c['as_of'], c['count'], c['same_date_2025']) for c in counts if isinstance(c.get('same_date_2025'), int)]

count = {
    'n': latest['count'],
    'asof': latest['as_of'],
    'lede': 'Arab citizens and residents of Israel killed in crime and violence since 1 January 2026.',
    'source': f'Count: The Abraham Initiatives, as reported by Bokra on {23} October. '
              f'{b["citizens"]} citizens and {b["residents"]} residents. Incidents reported since are listed below.',
    'breakdown': [{'n': b['shot'], 'label': 'shot'}, {'n': b['stabbed'], 'label': 'stabbed'}, {'n': b['arson'], 'label': 'killed in arson'},
                  {'n': b['women_girls'], 'label': 'women and girls'}, {'n': b['by_police'], 'label': 'killed by police gunfire', 'red': True}],
    'trail': [{'v': v, 'date': d} for v, d in trail],
    'cmp_caption': 'Same date, last year · Abraham Initiatives updates',
    'compare': [
        {'date': '2026-06-29', 'y26': 143, 'y25': 128, 'chg': '+12%'},
        {'date': '2026-07-20', 'y26': 157, 'y25': 139, 'chg': '+13%'},
        {'date': '2026-09-25', 'y26': 181, 'y25': 187, 'chg': '−3%', 'turn': True},
        {'date': '2026-10-13', 'y26': 184, 'y25': 200, 'chg': '−8%'},
        {'date': latest['as_of'], 'y26': latest['count'], 'y25': latest['same_date_2025'], 'chg': '−10.5%'},
    ],
    'note': 'Since late September the count has sat below the same date in 2025, a year that ended at 252, the worst on record. '
            'The gap widened because last autumn was worse, not because this one has been calm: four people were killed in the first three weeks of October.',
    'monthly': [{'m': m, 'n': n} for m, n in spans],
    'field_label': f'{latest["count"]} tally marks in rows, one row for each span between published counts.',
    'field_cap': 'Each mark stands for one person in the watchdog’s register. Each row is the span between two published counts, '
                 'dated by the update that closed it, so the marks add up to the count exactly.',
    'monthly_note': 'Rows from Abraham Initiatives updates reported by the Times of Israel and Bokra. The watchdog does not publish monthly totals; the dates are those of its updates.',
    'pairs': [{'d': d, 'a': a, 'p': p} for d, a, p in pairs],
    'climb_h': 'Ahead all summer, behind since September',
    'climb_p': 'Year-to-date killings at each published update: 2026 against the same date in 2025.',
    'hundred': [{'y': 2021, 'w': '18 Oct', 'pct': 79.7}, {'y': 2022, 'w': '24 Nov', 'pct': 89.9}, {'y': 2023, 'w': '9 Jun', 'pct': 43.8},
                {'y': 2024, 'w': '23 Jun', 'pct': 47.8}, {'y': 2025, 'w': '30 May', 'pct': 41.1}, {'y': 2026, 'w': 'day 121', 'pct': 33.2, 'now': True}],
    'hundred_p': 'In 2026 the count passed one hundred on 1 May, day 121: the fastest in five years.',
    'updates': [{'asof': c['as_of'], 'n': c['count'], 'y25': c.get('same_date_2025') if isinstance(c.get('same_date_2025'), int) else None,
                 'source': c['source']['outlet'] if isinstance(c.get('source'), dict) else ''} for c in reversed(counts)],
    'years': [{'y': 2025, 'n': 252, 'note': 'The deadliest year on record.'}, {'y': 2024, 'n': 230, 'note': ''},
              {'y': 2023, 'n': 244, 'note': 'More than double the year before.'}],
}

# reported, not entered -------------------------------------------------
open_items = [
    {'date': '2026-10-15', 'place': 'Golani junction', 'text': 'The body of Rabia Obeidi, 38, from Zububa near Jenin, was found in the Lavi forest; three suspects were arrested. As a West Bank resident he is probably outside the count.'},
    {'date': '2026-10-14', 'place': 'Abu Tor, Jerusalem', 'text': 'Mohammed Ashraf Shweiki, 24, was shot dead and two others were wounded. Whether the watchdog has counted him, as an East Jerusalem resident, is not yet clear.'},
    {'date': '2026-10-06', 'place': 'Haifa', 'text': 'A man died after police used a Taser on him. His name, age and community were not published; an investigation was opened.'},
]

# the election ------------------------------------------------------------
el = N['election']
polls = el['polls']
slates = [
    {'name': 'Joint List', 'who': 'Hadash, Ta’al and Balad, headed by Yousef Jabareen, with Ahmad Tibi and Ofer Cassif on the slate.',
     'polls': [{'poll': p['pollster'], 'date': p['date'], 's': p['joint_list']} for p in polls[:3]],
     'status': 'Cleared to run by the Supreme Court on 2 October. Balad’s chairman Sami Abu Shehadeh withdrew a day earlier.'},
    {'name': 'Ra’am', 'who': 'The United Arab List, led by Mansour Abbas; former police official Yoav Segalovitz is No. 2, the first Jewish candidate on its slate.',
     'polls': [{'poll': p['pollster'], 'date': p['date'], 's': p['raam']} for p in polls[:3]],
     'status': 'Cleared on 2 October. Gadi Eisenkot has said Ra’am will not sit in a government he leads.'},
    {'name': 'The Arab vote', 'who': 'Turnout decides how many seats the two lists win, and whether the change bloc can reach 61.',
     'polls': [{'poll': p['pollster'], 'date': p['date'], 's': p['arab_total'] / 2} for p in []],
     'status': 'Stat-Net forecasts 63% Arab turnout, against about 53% in 2022. In Maariv’s poll 81% of Arab-party supporters said they would surely vote, up from 74% on 8 October.'},
]
election = {
    'date': el['date'],
    'title': 'Two Arab lists, both cleared to run, polling 14 to 16 seats between them',
    'slates': slates,
    'facts': [{'v': '14–16', 'label': 'seats for the two lists in the final polls of 23 October'},
              {'v': '63%', 'label': 'forecast Arab turnout (Stat-Net); about 53% in 2022'},
              {'v': '3.25%', 'label': 'threshold of valid votes, about four seats'},
              {'v': '20:00', 'label': 'free trains and intercity buses from Monday evening to the end of election day'}],
    'src': 'Final polls: Madad for Channel 13, Midgam for Channel 12 and Kantar for Kan, 23 October, via the Times of Israel. Turnout: Stat-Net via the Times of Israel; Lazar for Maariv via Bokra.',
    'key_dates': el['key_dates'],
    'polls': polls,
}

home = {
    'lead': 'police-claim-14-percent-drop-in-arab-murders',
    'entries': ['count-reaches-186-after-shefa-amr-killing', 'life-sentence-maisar-burning-killing', 'deir-hanna-wedding-hall-demolished',
                'two-relatives-arrested-asma-abu-ghanem-killing', 'acri-warns-964m-cut-from-arab-plan', 'two-young-men-killed-segev-shalom-umm-al-fahm',
                'al-dahiya-negev-village-demolished', 'or-yarok-134-arab-road-deaths', 'netanyahu-billion-shekels-shin-bet-crime'],
    'life': ['sakhnin-school-tops-excellence-bagrut', 'tel-aviv-university-honours-said-abu-shakra', 'sakhnin-fans-bus-stoned', 'nazareth-city-palace-music-days'],
    'street': {
        'photo': PMAP.get('_street', ''), 'photo2': PMAP.get('_street2', ''),
        'lbl': 'Protest · Arraba, 3 October',
        'h': 'Twenty-six years on, the march still starts at the graves',
        'p': ['On 3 October Arab towns marked the anniversary of October 2000, when thirteen men were killed by police, twelve of them Arab citizens. '
              'The High Follow-Up Committee led a route through the graves in Jatt, Umm al-Fahm, Muawiya, Nazareth, Kafr Kanna, Kafr Manda and Sakhnin.',
              'The march left Arraba’s old mosque on Daher al-Omar Street at four in the afternoon and ended at the memorial in the school square. '
              'Earlier this year the street kept its own count: in January a shopkeepers’ strike in Sakhnin against protection rackets grew into a march of tens of thousands in Tel Aviv.'],
        'src': 'Bokra, 3 October 2026; Times of Israel, 5 February 2026.',
    },
}
for sid in home['entries'] + [home['lead']] + home['life']:
    assert sid in stories, sid
stories['police-claim-14-percent-drop-in-arab-murders']['weight'] = 2

named = [
    {'label': 'October · counted 183 to 186', 'ctx': 'Four killings entered in the first three weeks of the month.',
     'people': [{'name': 'Mousa Yousef al-Jabour', 'meta': '26 · Rahat · 10 Oct'}, {'name': 'Yassin al-Shawi', 'meta': 'about 20 · Segev Shalom · 12 Oct'},
                {'name': 'Nimer Jabareen', 'meta': '20 · Umm al-Fahm · 13 Oct'}, {'name': 'Ibrahim Bashkar', 'meta': '81 · Shefa-Amr · 23 Oct'}],
     'src': 'Bokra, 10–23 Oct 2026; Times of Israel.'},
    {'label': '25 September · counted 181 and 182', 'ctx': 'A woman found beaten in her building in Haifa; her husband was arrested. That evening a young man from Tamra died after a shooting in Kabul.',
     'people': [{'name': 'Yonit Masswada', 'meta': '30s · Silwan, found in Haifa · 25 Sep'}, {'name': 'Mohammed Yassin', 'meta': 'about 25 · Tamra · 25 Sep'}],
     'src': 'Bokra, 25 Sep 2026.'},
    {'label': 'Police gunfire · 9 this year', 'ctx': 'Alaa Mahameed was unarmed, Haaretz reported, citing the police investigations department; police say he lunged at an officer after a chase on Route 65.',
     'people': [{'name': 'Alaa Mahameed', 'meta': '38 · Umm al-Fahm · 17 Sep'}, {'name': 'Omar Hawari', 'meta': 'al-Reina · in Nazareth · Sep'}],
     'src': 'Times of Israel, 18 Sep 2026; Bokra, 25 Sep 2026.'},
    {'label': '2–3 September · Nazareth', 'ctx': 'Four killed in under 24 hours; police raided compounds in the city and arrested 30.',
     'people': [{'name': 'Noor Nafafea', 'meta': '31 · 2 Sep'}, {'name': 'Noor Khlo', 'meta': '20 · 2 Sep'}, {'name': 'Mustafa Badra', 'meta': '27 · 2 Sep'}, {'name': 'Mahmoud Biatra', 'meta': '30 · 3 Sep'}],
     'src': 'Times of Israel, 4 Sep 2026.'},
    {'label': 'Found 13 September · near Baqa al-Gharbiya', 'ctx': 'Three young men found dead in a burned car; police are treating their deaths as murder.',
     'people': [{'name': 'Zain Odeh', 'meta': '16 · brother of Qassem'}, {'name': 'Qassem Odeh', 'meta': '20'}, {'name': 'Yahya Bassimi', 'meta': '20 · their relative'}],
     'src': 'Times of Israel, 13 Sep 2026.'},
]

files = [
    {'lbl': 'Background · Government', 'h': 'NIS 1 billion and an ‘iron fist’: the Shin Bet joins the fight against crime', 'sid': 'netanyahu-billion-shekels-shin-bet-crime',
     'p': 'In July the cabinet moved about NIS 497 million from the five-year plan for Arab society to the Shin Bet and police. In October the prime minister announced NIS 1 billion more.',
     'src': 'Bokra; Times of Israel, 8 Oct 2026.'},
    {'lbl': 'The years before', 'h': '244 · 230 · 252', 'fig': True, 'href': 'count.html',
     'p': 'Killings in Arab society in 2023, 2024 and 2025. 2023 more than doubled the year before; 2025 was the deadliest year on record.',
     'src': 'Abraham Initiatives figures via the Times of Israel and the Jerusalem Post.'},
    {'lbl': 'Method', 'h': 'Whose count, and why one', 'href': 'method.html',
     'p': 'We keep the Abraham Initiatives’ tally. Police figures count murder cases, not people, and other monitors count differently. When they disagree we name the source; we never average.',
     'src': 'Counts change after deaths in hospital: we correct the ledger, never overwrite it.'},
]

E = {
    'date': '2026-10-24',
    'description': f'The count: {latest["count"]} Arab citizens and residents of Israel killed in crime and violence in 2026, and every story entered against it.',
    'count': count, 'open': open_items,
    'open_note': 'Deaths reported after the 23 October update that the watchdog has not counted, or may not count. A death enters the ledger only when it does.',
    'election': election, 'home': home, 'named': named, 'named_h': 'Named this autumn', 'files': files,
    'roads': N['roads'], 'stories': stories,
}
json.dump(E, open(os.path.join(ROOT, 'tools', 'edition.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(stories), 'stories;', sum(1 for s in stories.values() if s.get('photo')), 'with photos; count', latest['count'])
