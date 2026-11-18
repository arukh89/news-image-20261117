# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/arukh89/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/arukh89/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image summing up the world news of Tuesday 17 November 2026: U.S. strikes on Iran's Qeshm Island, the Crimea Bridge span collapse, Japan scrambling fighter jets over an airspace breach, and the U.S. losing its measles-free status — plus Quad and Shenzhen briefs. The artwork is original flat illustration drawn by `render.py` from verified reports of that day; no photograph or copied artwork is used.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) writes `entry.png` (1024×1024, under 1 MiB) to `/output/entry.png`. It copies the same bytes on every run, with no network access. `render.py` is the build-time drawing script that produced `entry.png`; it is not run by the grader.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
