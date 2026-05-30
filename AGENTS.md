# AGENTS.md

## 项目概述

中文资源分享博客，基于 Hexo 7.3.0 + AnZhiYu 主题，通过 GitHub Actions 部署到 GitHub Pages。

## 常用命令

- `npm run build` — 生成静态站点 (hexo generate)
- `npm run clean` — 清理生成文件 (hexo clean)
- `npm run server` — 启动本地开发服务器 (hexo server)
- `npm run deploy` — 部署 (hexo deploy，CI 中不使用)

## 部署

- 推送到 **`github`** 分支时 CI 自动部署（不是 `main`）
- 工作流：`.github/workflows/deploy.yml`
- 使用 Node.js 20 构建，将 `public/` 部署到 `gh-pages` 分支

## 爬虫脚本

仓库根目录有四个爬虫脚本用于内容创建：

| 脚本 | 语言 | 特点 |
|------|------|------|
| `scrape_article.py` | Python | 通用网页，原样下载图片 |
| `scrape_zhihu.py` | Python | 知乎专用 HTML 处理 |
| `scrape_win11.py` | Python | 图片转 WebP (Pillow) |
| `scrape_leyugg.js` | Node.js | 图片转 WebP (Sharp)，HTTPS 跳过证书验证 |

### 爬虫模式
- 获取 HTML → 通过 CSS 选择器提取标题/内容 → 下载/转换图片到 `source/imgs/` → 生成带 front matter 的 Markdown → 保存到 `source/_posts/`
- Front matter：`title`、`date`、`tags: [技术]`
- 图片引用：`/imgs/filename.webp`

### 依赖
- Python 爬虫：`requests`、`beautifulsoup4`、`lxml`、`Pillow`（见 `requirements.txt`）
- Node.js 爬虫：`axios`、`cheerio`、`sharp`（在 `package.json` 中）

## 站点结构

- `source/_posts/` — Markdown 博文（35 篇）
- `source/imgs/` — 文章图片
- `_config.yml` — Hexo 配置（主题：anzhiyu）
- `_config.anzhiyu.yml.yml` — 主题配置（giscus 评论、本地搜索、暗黑模式、Pjax、lazyload）
- `public/` — 生成的静态输出（gitignore）

## 关键约定

- 所有爬虫将图片保存到 `source/imgs/` 并转换为 WebP
- Markdown 使用相对图片路径：`/imgs/filename.webp`
- 文章 front matter 使用 `tags: [技术]`
- 中文内容，配置中 `language: zh-CN`
- 主题使用 giscus 评论、本地搜索、暗黑模式（跟随系统自动切换）

## Pjax 注意事项

- 主题启用 Pjax（SPA 式导航），第三方脚本需要在 `pjax:complete` 事件中重新初始化
- 卜蒜子统计脚本在 `main.js` 中只注入一次，Pjax 导航后需要重新注入
- 修复位置：`themes/anzhiyu/layout/includes/third-party/pjax.pug` 的 `pjax:complete` 处理器

## 已知问题

- Python 爬虫需要先安装 `requirements.txt`
- Node.js 爬虫使用 `rejectUnauthorized: false` 跳过 HTTPS 证书验证
- 部署分支是 `github`，不是 `main`
- 主题配置文件扩展名为双 `.yml.yml`
- `public/` 目录被 gitignore 但由构建生成