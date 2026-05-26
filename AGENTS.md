# AGENTS.md

This file provides guidance to the AI agent when working with code in this repository.

## Deployment branch

CI deploys on push to the **`github`** branch, NOT `main`. The `gh-pages` branch is auto-generated; never edit it directly.

## Theme config override

Do NOT edit `themes/anzhiyu/_config.yml` directly. All theme customizations go in `_config.anzhiyu.yml.yml` (note the double `.yml.yml` extension — this is intentional for Hexo's theme override mechanism).

## Scraper scripts

Four scraper scripts at the repo root generate post content:
- `scrape_article.py`, `scrape_zhihu.py`, `scrape_win11.py` — Python; use `python <script>.py <url>`
- `scrape_leyugg.js` — Node.js; uses `rejectUnauthorized: false` for HTTPS (intentional)

All scrapers output Markdown to `source/_posts/` and images to `source/imgs/`. Front matter always includes `tags: [技术]`.

## Commit style

Commits follow the pattern: `feat: 更新文章` (Chinese description after the colon is normal here).
