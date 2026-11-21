# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Skyzo07/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Skyzo07/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image summing up **Saturday 21 November 2026**'s world news — a front page:
masthead with the date, one large lead panel, five more stories in a clean grid,
each with a pictogram drawn in code, and the date named again in the bottom strip.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (stdlib only) copies the repository's `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, validating PNG magic, 1024×1024 size and the
1 MiB cap before and after the copy, plus a post-copy sha256 check.
`render.py` (stdlib only, no network, deterministic) is the program that drew
`entry.png` from scratch: a hand-written 5×7 bitmap font and pictograms built
from rectangles, lines, circles and polygons.

## The six stories

1. **Lead — Conflict, Europe: Missiles land in Poland.** Two Russian missiles
   and a suspected drone came down in Poland during allied drills; NATO called
   it a "grave violation", PM Tusk a deliberate provocation. No injuries in
   Poland. Source: Associated Press.
2. **Justice: Myanmar guilty of genocide.** The World Court's first-ever
   genocide verdict (9–6) over the Rohingya; the ruling is final. Source:
   Human Rights Watch.
3. **Markets: Wall St plunges into correction.** S&P 500 −3.7%, Nasdaq −5.3%,
   Nvidia −14% on a reported SEC probe. Source: Reuters market coverage.
4. **Climate: COP31 talks in overtime.** The draft deal omits fossil fuels;
   **no deal had been agreed yet** — the image shows talks in overtime, not a
   done deal. Source: Associated Press.
5. **Disaster, Peru: Magnitude 6.8 quake.** Junín tremor felt 320 km away in
   Lima; no casualties reported. Source: Reuters.
6. **Health, hope: Cancer pill — tumours vanish.** Early trial: tumours gone
   in 1 in 12 patients. An early trial, not a cure. Source: BBC News.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
