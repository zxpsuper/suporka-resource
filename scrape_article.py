# -*- coding: utf-8 -*-
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import hashlib

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def download_image(url, save_dir):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 从URL中提取文件名
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename:
            # 如果URL中没有文件名，生成一个
            filename = hashlib.md5(url.encode()).hexdigest()[:8] + '.jpg'
        
        # 确保文件名有效
        filename = get_valid_filename(filename)
        filepath = os.path.join(save_dir, filename)
        
        # 如果文件已存在，添加序号
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(save_dir, base + '_' + str(counter) + ext)
            counter += 1
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print('下载图片成功: ' + filepath)
        return os.path.basename(filepath)
    except Exception as e:
        print('下载图片失败 ' + url + ': ' + str(e))
        return None

def scrape_article(url):
    # 创建目录
    posts_dir = 'source/_posts'
    imgs_dir = 'source/imgs'
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(imgs_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print('正在爬取网页: ' + url)
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 获取标题
    title = soup.title.string if soup.title else 'Untitled'
    # 清理标题
    title = title.split('|')[0].strip()
    
    # 获取文章内容 - 尝试查找主要内容区域
    article_content = None
    
    # 常见的文章内容选择器
    content_selectors = [
        'article',
        '.post-content',
        '.article-content',
        '.content',
        '#content',
        '.main-content',
        '.post'
    ]
    
    for selector in content_selectors:
        article_content = soup.select_one(selector)
        if article_content:
            break
    
    if not article_content:
        # 如果没有找到，使用body
        article_content = soup.body
    
    # 下载所有图片
    print('正在下载图片...')
    img_tags = article_content.find_all('img')
    img_url_mapping = {}
    
    for img in img_tags:
        src = img.get('src') or img.get('data-src')
        if src:
            full_url = urljoin(url, src)
            local_filename = download_image(full_url, imgs_dir)
            if local_filename:
                img_url_mapping[full_url] = local_filename
                img_url_mapping[src] = local_filename  # 也映射相对路径
    
    # 转换为Markdown
    print('正在转换为Markdown...')
    
    # 提取文本内容并处理图片
    markdown_content = []
    
    # 添加front matter
    from datetime import datetime
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    front_matter = '''---
title: ''' + title + '''
date: ''' + date_str + '''
tags:
  - 技术
---

'''
    markdown_content.append(front_matter)
    
    # 简单的HTML到Markdown转换
    def process_element(element):
        result = []
        
        for child in element.children:
            if child.name is None:
                # 文本节点
                text = child.strip()
                if text:
                    result.append(text)
            elif child.name == 'h1':
                result.append('\n# ' + child.get_text().strip() + '\n')
            elif child.name == 'h2':
                result.append('\n## ' + child.get_text().strip() + '\n')
            elif child.name == 'h3':
                result.append('\n### ' + child.get_text().strip() + '\n')
            elif child.name == 'h4':
                result.append('\n#### ' + child.get_text().strip() + '\n')
            elif child.name == 'p':
                result.append('\n' + process_element(child) + '\n')
            elif child.name == 'br':
                result.append('\n')
            elif child.name == 'img':
                src = child.get('src') or child.get('data-src', '')
                alt = child.get('alt', '')
                if src in img_url_mapping:
                    result.append('![' + alt + '](/imgs/' + img_url_mapping[src] + ')')
                else:
                    result.append('![' + alt + '](' + src + ')')
            elif child.name == 'a':
                href = child.get('href', '')
                text = child.get_text().strip()
                result.append('[' + text + '](' + href + ')')
            elif child.name == 'strong' or child.name == 'b':
                result.append('**' + child.get_text().strip() + '**')
            elif child.name == 'em' or child.name == 'i':
                result.append('*' + child.get_text().strip() + '*')
            elif child.name == 'ul':
                result.append('\n')
                for li in child.find_all('li', recursive=False):
                    result.append('- ' + process_element(li).strip() + '\n')
            elif child.name == 'ol':
                result.append('\n')
                for i, li in enumerate(child.find_all('li', recursive=False), 1):
                    result.append(str(i) + '. ' + process_element(li).strip() + '\n')
            elif child.name == 'li':
                result.append(process_element(child))
            elif child.name == 'code':
                result.append('`' + child.get_text() + '`')
            elif child.name == 'pre':
                code_text = child.get_text()
                result.append('\n```\n' + code_text + '\n```\n')
            elif child.name == 'blockquote':
                quote_text = process_element(child).strip()
                lines = quote_text.split('\n')
                quoted = '\n'.join('> ' + line for line in lines)
                result.append('\n' + quoted + '\n')
            else:
                # 递归处理其他元素
                result.append(process_element(child))
        
        return ''.join(result)
    
    markdown_content.append(process_element(article_content))
    
    # 生成最终的Markdown
    final_markdown = ''.join(markdown_content)
    
    # 清理多余的空行
    final_markdown = re.sub(r'\n{3,}', '\n\n', final_markdown)
    
    # 保存Markdown文件
    safe_title = get_valid_filename(title)
    md_filename = safe_title + '.md'
    md_filepath = os.path.join(posts_dir, md_filename)
    
    # 如果文件名已存在，添加日期
    if os.path.exists(md_filepath):
        md_filename = date_str + '-' + safe_title + '.md'
        md_filepath = os.path.join(posts_dir, md_filename)
    
    with open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(final_markdown)
    
    print('\n成功!')
    print('Markdown文件: ' + md_filepath)
    print('图片目录: ' + imgs_dir)
    
    return md_filepath

if __name__ == '__main__':
    url = 'https://geektutu.com/post/quick-golang.html'
    scrape_article(url)
