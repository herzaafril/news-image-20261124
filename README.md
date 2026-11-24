# The World in One Day — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/herzaafril/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/herzaafril/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

make.fun bounty entry: [**news-image-20261124**](https://make.fun/bounty/news-image-20261124) — "Sum up 24 November's
world news in one image", by @herza-afril.

## The image

A 1024×1024 newspaper dashboard, drawn entirely in code with PIL
(`draw.py` — no AI-generated imagery, no network, deterministic: re-running
produces byte-identical output). It carries **31 stories**, every one
verified as having happened — or first been reported — on Tuesday
24 November 2026, across six regions:

- **Leads:** Asia's record chip rally (Taiex +9.0%) · Nepal quake 5.6 ·
  Sanofi buys Insmed for $41bn
- **Second tier:** Kerch Bridge struck again · Abu Dhabi talks end with no
  deal · Solomon Islands ditches its China pact · Shenzhou-24 crew named
  (first foreign astronaut on Tiangong) · Seoul scrambles jets as Russian
  planes enter its air zone
- **Plus 23 more**, from the Gukesh–Sindarov title match in Geneva to
  Wall Street's split close (Dow over 50,000) and Lula's snub of Milei

A timeline strip marks four timed events (01:32 UTC quake, 04:35 UTC UN
port warning, 08:06 UTC Sanofi deal, 14:00 UTC FIDE Game 1); a numbered
world map pins every story; and a DATE CHECK footer names the stale
stories the entry deliberately excluded — most of them Monday 23 November
news that rival entries present as Tuesday's (NATO space vow, Estonia
warning, Megaspeed blacklist, Puigdemont amnesty, EU 22nd sanctions,
Trump hush-money ruling, the Nepal PM visit, the 700,000-dead report,
COP31, the Merkury sinking, Huang's +31% Nvidia jump, and more).

Claims that could not be verified are tagged CLAIM on the image (Iran's
Hormuz mine claims, the DR Congo rebels' shoot-down claim).

## Files

- `draw.py` — draws `entry.png` (run: `python3 draw.py`)
- `entry.png` — the 1024×1024 entry image (≤ 1 MiB)
- `main.ts` — validates `entry.png` (exists, non-empty, ≤ 1 MiB, PNG
  magic bytes) and copies it to the output directory
- `LICENSE` — MIT (starter licence)

## Sources

Reuters, AP, Yonhap, CNA/Focus Taiwan, Nikkei Indexes, Sanofi,
China Manned Space Agency, South Korea Joint Chiefs of Staff, BBC,
Al Jazeera, and others. Full per-story sources and the date-trap
verification log live in the build notes (`work-news24/notes.md`).
