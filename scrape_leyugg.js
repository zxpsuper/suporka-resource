const fs = require('fs');
const path = require('path');
const https = require('https');
const axios = require('axios');
const cheerio = require('cheerio');
const sharp = require('sharp');

function getValidFilename(s) {
    return String(s).trim().replace(/\s+/g, '_').replace(/[^\w.-]/g, '');
}

async function downloadAndConvertImage(url, saveDir) {
    try {
        const response = await axios({
            url,
            method: 'GET',
            responseType: 'arraybuffer',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            timeout: 10000,
            httpsAgent: new https.Agent({ rejectUnauthorized: false })
        });

        const parsed = new URL(url);
        let filename = path.basename(parsed.pathname);
        if (!filename || filename === '/') {
            filename = require('crypto').createHash('md5').update(url).digest('hex').slice(0, 8) + '.webp';
        } else {
            const base = path.parse(filename).name;
            filename = base + '.webp';
        }

        filename = getValidFilename(filename);
        let filepath = path.join(saveDir, filename);

        const base = path.parse(filename).name;
        const ext = path.parse(filename).ext;
        let counter = 1;
        while (fs.existsSync(filepath)) {
            filepath = path.join(saveDir, base + '_' + counter + ext);
            counter++;
        }

        await sharp(response.data)
            .webp({ quality: 85 })
            .toFile(filepath);

        console.log('下载并转换图片成功:', filepath);
        return path.basename(filepath);
    } catch (e) {
        console.error('下载图片失败', url, ':', e.message);
        return null;
    }
}

function processElement($, element, imgUrlMapping) {
    const result = [];

    $(element).contents().each((_, child) => {
        if (child.type === 'text') {
            const text = $(child).text().trim();
            if (text) result.push(text);
        } else if (child.type === 'tag') {
            const tagName = child.name.toLowerCase();
            const text = $(child).text().trim();

            switch (tagName) {
                case 'h1':
                    result.push('\n# ' + text + '\n');
                    break;
                case 'h2':
                    result.push('\n## ' + text + '\n');
                    break;
                case 'h3':
                    result.push('\n### ' + text + '\n');
                    break;
                case 'h4':
                    result.push('\n#### ' + text + '\n');
                    break;
                case 'p':
                    result.push('\n' + processElement($, child, imgUrlMapping) + '\n');
                    break;
                case 'br':
                    result.push('\n');
                    break;
                case 'img':
                    const src = $(child).attr('src') || $(child).attr('data-src') || '';
                    const alt = $(child).attr('alt') || '';
                    if (imgUrlMapping[src]) {
                        result.push('![' + alt + '](/imgs/' + imgUrlMapping[src] + ')');
                    } else {
                        result.push('![' + alt + '](' + src + ')');
                    }
                    break;
                case 'a':
                    const href = $(child).attr('href') || '';
                    result.push('[' + text + '](' + href + ')');
                    break;
                case 'strong':
                case 'b':
                    result.push('**' + text + '**');
                    break;
                case 'em':
                case 'i':
                    result.push('*' + text + '*');
                    break;
                case 'ul':
                    result.push('\n');
                    $(child).children('li').each((_, li) => {
                        result.push('- ' + processElement($, li, imgUrlMapping).trim() + '\n');
                    });
                    break;
                case 'ol':
                    result.push('\n');
                    $(child).children('li').each((i, li) => {
                        result.push((i + 1) + '. ' + processElement($, li, imgUrlMapping).trim() + '\n');
                    });
                    break;
                case 'li':
                    result.push(processElement($, child, imgUrlMapping));
                    break;
                case 'code':
                    result.push('`' + $(child).text() + '`');
                    break;
                case 'pre':
                    result.push('\n```\n' + $(child).text() + '\n```\n');
                    break;
                case 'blockquote':
                    const quoteText = processElement($, child, imgUrlMapping).trim();
                    const lines = quoteText.split('\n');
                    const quoted = lines.map(line => '> ' + line).join('\n');
                    result.push('\n' + quoted + '\n');
                    break;
                default:
                    result.push(processElement($, child, imgUrlMapping));
            }
        }
    });

    return result.join('');
}

async function scrapeArticle(url) {
    const postsDir = 'source/_posts';
    const imgsDir = 'source/imgs';
    fs.mkdirSync(postsDir, { recursive: true });
    fs.mkdirSync(imgsDir, { recursive: true });

    console.log('正在爬取网页:', url);
    const response = await axios({
        url,
        method: 'GET',
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        },
        timeout: 10000,
        httpsAgent: new https.Agent({ rejectUnauthorized: false })
    });

    const $ = cheerio.load(response.data);
    let title = $('title').text() || 'Untitled';
    title = title.split('|')[0].trim();

    let articleContent = null;
    const contentSelectors = [
        'article', '.post-content', '.article-content', '.content',
        '#content', '.main-content', '.post', '.single-content', '.entry-content'
    ];

    for (const selector of contentSelectors) {
        articleContent = $(selector);
        if (articleContent.length > 0) break;
    }

    if (!articleContent || articleContent.length === 0) {
        articleContent = $('body');
    }

    console.log('正在下载并转换图片...');
    const imgTags = articleContent.find('img');
    const imgUrlMapping = {};

    for (let i = 0; i < imgTags.length; i++) {
        const img = $(imgTags[i]);
        let src = img.attr('src') || img.attr('data-src');
        if (src) {
            const fullUrl = new URL(src, url).href;
            const localFilename = await downloadAndConvertImage(fullUrl, imgsDir);
            if (localFilename) {
                imgUrlMapping[fullUrl] = localFilename;
                imgUrlMapping[src] = localFilename;
            }
        }
    }

    console.log('正在转换为Markdown...');

    const dateStr = new Date().toISOString().split('T')[0];
    const frontMatter = `---
title: ${title}
date: ${dateStr}
tags:
  - 技术
---

`;

    const content = processElement($, articleContent, imgUrlMapping);
    let finalMarkdown = frontMatter + content;
    finalMarkdown = finalMarkdown.replace(/\n{3,}/g, '\n\n');

    const safeTitle = getValidFilename(title);
    let mdFilename = safeTitle + '.md';
    let mdFilepath = path.join(postsDir, mdFilename);

    if (fs.existsSync(mdFilepath)) {
        mdFilename = dateStr + '-' + safeTitle + '.md';
        mdFilepath = path.join(postsDir, mdFilename);
    }

    fs.writeFileSync(mdFilepath, finalMarkdown, 'utf-8');

    console.log('\n成功!');
    console.log('Markdown文件:', mdFilepath);
    console.log('图片目录:', imgsDir);

    return mdFilepath;
}

if (require.main === module) {
    (async () => {
        try {
            await scrapeArticle('https://leyugg.com/pixpin.html');
        } catch (e) {
            console.error('爬取失败:', e);
        }
    })();
}

module.exports = { scrapeArticle };
