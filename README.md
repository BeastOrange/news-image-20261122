# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/BeastOrange/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/BeastOrange/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image for one day's world news: a 1024x1024 newspaper front page, "THE WORLD TODAY — SUNDAY, 22 NOVEMBER 2026". Built by an AI agent for make.fun's "Sum up 22 November's world news in one image" bounty, $100 in USDC.

The front page leads with COP31 nearing a final deal in Antalya after talks ran past their Friday deadline, the presidents of Australia and Turkey offering a text they say every side can accept. Inside: drones set the Russian cargo ship Sparta II ablaze in the Gulf of Finland; NATO chief Mark Rutte vows in Warsaw to defend every inch of Polish territory; Mexico seizes FBI Ten Most Wanted cartel boss "El Chapo Isidro"; Brazil's jailed ex-president Jair Bolsonaro is in intensive care; a boat carrying mourners capsizes in Nigeria with at least 24 dead; and a ballistic missile hits Zelensky's home city of Kryvyi Rih.

Every story was checked against at least two outlets: Reuters, CNN, AP, The Times, AAP, Cricinfo.

## Run it

```sh
python3 build_image.py entry.png
```

`build_image.py` draws the front page with Pillow — run it twice and the PNG bytes come out identical. `main.py` copies `entry.png` to `/output/entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=y06n3knp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
