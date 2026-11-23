[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/jackflank4-lang/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/jackflank4-lang/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123/reward?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# 23 November 2026 World News in One Image

A program that draws one newspaper-style poster summing up Monday
23 November 2026's world news, as a 1024x1024 PNG at `/output/entry.png`.

## Run

```sh
python3 main.py
```

The program uses only the Python 3.13 standard library (no network, no
PIL): it draws with a hand-written 5x5 bitmap font and a hand-rolled PNG
encoder, so the output is byte-for-byte deterministic across runs.

## Stories in the image

1. **WAR — Benghazi, Libya:** Ukrainian sea drones sink the Russian
   corvette Merkury at Benghazi port (Zelenskyy, Monday).
2. **MARKETS — New York:** Jensen Huang is back as Nvidia CEO; shares
   jump about 33%, the S&P 500 rises 4.8%, the Nikkei falls over 5%.
3. **CLIMATE — Antalya, Turkiye:** COP31 ends without a deal, the
   longest UN climate conference in history.
4. **JUSTICE — Sinaloa, Mexico:** FBI most-wanted fugitive
   "El Chapo Isidro" (Fausto Isidro Meza Flores) captured with US help.
5. **DIPLOMACY — Berlin:** Zelenskyy calls for four-way talks
   (Ukraine, Europe, US, Russia) "as soon as possible".
6. **MIDEAST — Strait of Hormuz:** Iran vows to use all means against
   the US blockade; Tehran says it downed a US drone.

## Layout

Navy masthead with the date, then a 2x3 grid of story cards: tag,
headline, short deck, dateline and a small pictogram, each with its own
accent colour.

## License

MIT. See [LICENSE](LICENSE).
