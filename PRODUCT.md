# Product

## Platform

web

## Stack

Static HTML/CSS/JS, no framework. Python helper scripts generate the marks, fonts, photos and pages (same pattern as TakTek's Canary Palestine and Olive Palestine prototypes). Delivered on GitHub Pages under TakTek-Dev only when the user says «ارفع». Commits only on request.

Build order: `python -I tools/fonts.py` → `brand.py` → `edition.py` → `photos.py` → `build.py` → `pages.py` → `book.py` → `links.py` → `og.py` (+ `node --experimental-websocket tools/shot.mjs http://localhost:8189/tools/out/og.html assets/og.png 1200 630 view`). Bump `V` in tools/shell.py on any asset change. Never hand-edit the built HTML.

## Users

English-speaking readers who follow Palestinian citizens of Israel ("the Inside", al-Dakhil): diaspora Palestinians, journalists, researchers, rights workers, solidarity audiences. They want the count of the killed, what happened since, and the rest of the community's news, each with its source.

## Product Purpose

The Inside – Palestine: news of Palestinian citizens of Israel, kept as a record. No logo existed; identity from zero. Three earlier samples (1 Towns, 2 Long Read, 3 Ledger) in research/*.dc.html; the client liked 3, the Ledger, whose front page is the count.

## Brand Commitments

- Red is the bookkeeper's rule: the count, the closing stroke, a correction. Nothing else is red.
- Corrected, never erased: a changed figure is struck through and stays legible.
- Every story names its source; every photo is captioned with place, date, author and licence; no photo stands for a story it does not show; no photographs of the dead.
- Faces used by other TakTek prototypes and the samples are off-limits; IBM Plex banned. No cream or beige grounds.
- No staff, readership or partners may be invented. The letter and search are prototypes.
