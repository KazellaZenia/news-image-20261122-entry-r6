# THE SUNDAY GLOBE — news-image-20261122, round 6

Built for [make.fun's "Sum up 22 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261122) ($100 in USDC).

A one-page newspaper front page summing up the world's news of
Sunday 22 November 2026: 39 real, dated stories — 3 big illustrated
leads with full drawn scenes, 10 small illustrated leads, 26 briefs,
a 6-number strip, a 7-region bar, a date-check strip and a sourcing
footer. Masthead: THE SUNDAY GLOBE.

- `render.py` — draws `entry.png` (1024x1024, Pillow + DejaVu, local
  run only; the grader never runs it).
- `main.py` — standard library only; copies `entry.png` into
  `$MAKEFUN_OUTPUT_DIR` and writes nowhere else.
- `entry.png` — the rendered page (deterministic: two runs are
  byte-identical).

Lead stories: COP31 final text goes to a vote in Antalya (no
fossil-fuel mention, 35% electrification by 2035, 1.5°C overshoot
admitted); Russia's 186-drone night over Ukraine, 161 downed; Hong
Kong's Election Committee vote (856 candidates, 723 seats, 95.6%
turnout). New in round 6: Iran's rolling power cuts, India's record
720/9 in Wellington, US stocks in correction, the EU–Indonesia trade
deal, Bolsonaro in intensive care. Sources: Reuters, AP, AFP, BBC,
Al Jazeera, Kyiv Independent, The Guardian. All drawings are original.

What changed vs round 5 (judge 984,958, #100/6,668): 39 stories
instead of 36; five new verified small leads; the COP31 headline is
corrected (the text went to a vote — it did not "seal a deal"); the
three big-lead panels are full drawn scenes instead of single icons;
every lead carries a number badge.
