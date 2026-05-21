# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Chinese-language resource sharing blog (资源分享网站) built with **Hexo 7.3.0** using the **AnZhiYu** theme. The site publishes software/tool recommendation articles, hosted at https://resource.suporka.site and deployed to GitHub Pages.

## Commands

- `npm run build` — Generate static site via `hexo generate`
- `npm run clean` — Clean generated files via `hexo clean`
- `npm run server` — Start local dev server via `hexo server`
- `npm run deploy` — Deploy via `hexo deploy`

## GitHub Actions Deployment

The CI workflow (`.github/workflows/deploy.yml`) auto-deploys when pushing to the **`github`** branch:
1. Checkout → Setup Node.js 20 → npm install → npm run build
2. Deploy `public/` folder to the `gh-pages` branch using `JamesIves/github-pages-deploy-action`

The default branch is `main`; deployments are triggered from the `github` branch.

## Architecture

### Content scraping pipeline (4 scraper scripts at repo root)

| Script | Language | Source | Key Feature |
|--------|----------|--------|-------------|
| `scrape_article.py` | Python | General web | Downloads images as-is |
| `scrape_zhihu.py` | Python | Zhihu (知乎) | Handles Zhihu-specific HTML (figure tags, data-src) |
| `scrape_win11.py` | Python | General web | Converts all images to WebP (Pillow) |
| `scrape_leyugg.js` | Node.js | leyugg.com | Converts images to WebP (Sharp), supports HTTPS with rejectUnauthorized: false |

All scrapers follow the same pattern:
- Fetch HTML → extract title + content area using multiple CSS selectors → download/convert images to `source/imgs/` → generate Markdown with front matter → save to `source/_posts/`
- Front matter includes: `title`, `date`, `tags: [技术]`
- Image references in Markdown use relative paths: `/imgs/filename.webp`

### Site structure

- `_config.yml` — Hexo site configuration (title, URL, theme, plugins)
- `_config.anzhiyu.yml.yml` — AnZhiYu theme configuration (nav, social, comments via giscus, search, analytics, effects)
- `source/_posts/` — Markdown blog posts (currently 31 posts about software tools)
- `source/imgs/` — Locally stored post images
- `themes/anzhiyu/` — AnZhiYu theme files
- `scaffolds/` — Hexo post/page/draft templates
- `public/` — Generated static output (gitignored generally)

### Key site features configured

- Comments via **giscus** (GitHub Discussions)
- **Local search** enabled
- **Baidu analytics** (f6bb241491985fb5715c4dfd8a9d3b1f)
- **Dark mode** with system auto-switch
- **Pjax** for SPA-like navigation
- **Lazyload** for images
- **Music player** (netease, playlist ID: 630710167)
- DISMUTA (自定义) / 简繁转换 enabled