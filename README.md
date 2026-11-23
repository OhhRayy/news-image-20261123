# news-image-20261123 — Monday Edition

Entry for the make.fun bounty **"Sum up 23 November's world news in one image"**
(slug `news-image-20261123`, $100, closes 25 Nov 2026 00:00 UTC).

A one-page newspaper front page, "THE WORLD IN ONE DAY — MONDAY, 23 NOVEMBER 2026",
summing up six stories, all first reported on Monday 23 November 2026:

1. **KOSPI crashes 5%** — AI sell-off slams Seoul; Korea readies a 10-trillion-won rescue fund.
2. **M6.5 deep quake hits Vanuatu** — 601 km down at 02:40 UTC; no tsunami threat.
3. **NZ bat out a draw** — Mitchell & Phillips defy India on day five in Wellington.
4. **Modi meets Nepal's Balen Shah** — ceremonial welcome and first bilateral talks in Delhi.
5. **NHS launches AI cancer trial** — EDITH, the world's largest AI breast-screening trial (700,000 women).
6. **UN demands probe into ship strikes** — after sea drones sank a Russian warship off Benghazi.

Full story list with first-reported evidence:
[`../news-image-20261123-stories.md`](../news-image-20261123-stories.md)
(in the builder's workspace; the repo itself is self-contained).

## Files

- `entry.png` — the entry image (1024×1024, drawn by `draw.py` with Pillow).
- `main.py` — the entry program: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (stdlib only, deterministic — both runs write identical bytes).
- `draw.py` — the build-time script that drew `entry.png` (needs Pillow; not run by the grader).
- `LICENSE` — MIT.

## Verify locally

```sh
python3 draw.py          # rebuild entry.png (optional)
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum out1/entry.png out2/entry.png   # must match
```
