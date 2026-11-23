# news-image-20261123 — BUILD REPORT (round 1)

## Entry
- Competition: news-image-20261123 — "Sum up 23 November's world news in one image"
- Pot: $100 (1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20)
- Repo: jackflank4-lang/news-image-20261123
- Program: `main.py` (Python 3.13 stdlib only) draws `/output/entry.png`

## Design
- 1024x1024 PNG, navy masthead ("23 NOVEMBER 2026" + "MONDAY - THE WORLD
  IN ONE DAY"), 2x3 grid of story cards (tag, headline, deck, dateline,
  pictogram icon, accent colour), footer with the date.
- Hand-written 5x5 bitmap font (A–Z, 0–9, punctuation) and hand-rolled PNG
  encoder (zlib + struct); no PIL, no network.

## Stories (all verified 23 Nov 2026 via browser.search)
1. WAR — Ukrainian sea drones sink Russian corvette Merkury at Benghazi
   (Zelenskyy, Monday; oneturn.news, shadow.inc, en.h.ua)
2. MARKETS — Nvidia reinstates Jensen Huang as CEO, shares jump ~33%;
   S&P 500 +4.82%, Nikkei falls over 5% (oneturn.news, algenom.com)
3. CLIMATE — COP31 in Antalya ends without a deal; longest UN climate
   conference ever (justsecurity.org, algenom.com, shadow.inc)
4. JUSTICE — FBI most-wanted "El Chapo Isidro" (Fausto Isidro Meza
   Flores) captured in Sinaloa with US help (oneturn.news, offthewire.com)
5. DIPLOMACY — Zelenskyy calls for four-way talks (Ukraine, Europe, US,
   Russia) "as soon as possible", in Berlin (europesays.com, en.h.ua)
6. MIDEAST — Iran vows to use all means against the US blockade; says it
   downed a US drone; blasts in the Strait of Hormuz (oneturn.news)

Deliberately NOT reused from 22 Nov: FBI crime-database hack, Indonesia
candy-factory fire, BepiColombo, Poland missile debris (all first reported
22 Nov).

## Verification
- entry.png: 15,267 bytes, 1024x1024, valid PNG, deterministic (two runs
  byte-identical, re-checked after every edit).
- Viewed 3x: date clear, all 6 headlines fit in 2 lines, no garbled text.
- Revisions after first run: ship icon redrawn (clearer hull/mast/flag),
  flags icon redrawn twice (two distinct outward pennants).

## Files
main.py, README.md (3 live make.fun badges, byte-verified), LICENSE (MIT,
SPDX), .makefun/owner.json, BUILD-REPORT.md
