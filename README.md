# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/AriyaSrfZ/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/AriyaSrfZ/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world news of Friday 20 November 2026: a
front page led by the Trump–Xi–Putin peace declaration from Shenzhen,
with Kyiv, Riyadh, The Hague, COP31, Anthropic's market debut and a
record Van Gogh sale — plus a ticker of the day's other stories.

The image is drawn entirely by code (`draw.py`, Pillow): a newspaper
front page with schematic flags and pictograms, no photographs and no
copied artwork. Every story was reported on 20 November 2026
(SCMP, BBC, Dawn, Bangkok Post, Scoop).

## Run it

```sh
python3 draw.py        # redraw entry.png from the day's stories
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. The program runs with no network.

---

<sub>Entered on [make.fun](https://make.fun/?ref=gw24vq8v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
