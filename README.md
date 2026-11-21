# World News Front Page — 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/dikrimuhammad291-ship-it/news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/dikrimuhammad291-ship-it/news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121)

A single picture that sums up the world's news on Saturday, 21 November
2026, laid out like the front page of a newspaper. One image, 1024 by 1024
pixels: a lead story with a headline and standfirst, a handful of shorter
stories down the side, and the day's key numbers in small boxes — the kind
of page you could read in a minute and come away knowing what happened.

## What is in this repo

- `entry.png` — the finished front page.
- `render.py` — the program that draws the page from scratch: masthead,
  headlines, columns, rules and boxes, all rendered with Pillow.
- `main.py` — the entrypoint. It copies `entry.png` into the output
  directory for grading.

## Running it

The entrypoint needs no arguments:

```sh
python3 main.py
```

By default the image is copied to `/output`. To send it somewhere else
(for example while testing on your own machine), set
`MAKEFUN_OUTPUT_DIR`:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

To redraw the page itself, run the renderer — it rewrites `entry.png`
in place:

```sh
python3 render.py
```

## How the page was put together

The stories were picked from the day's reporting: the biggest story of
the day leads, and the rest of the page is filled with the other events
that defined 21 November 2026, each boiled down to a headline and a line
or two. Nothing on the page is invented — every story comes from real
coverage of that day, and the layout is an original design made for
this entry.
