
# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def create_markdown_file(title, content, date_str, tags, posts_dir):
    front_matter = '''---
title: ''' + title + '''
date: ''' + date_str + '''
tags:
'''
    for tag in tags:
        front_matter += '  - ' + tag + '\n'
    front_matter += '---\n\n'
    
    final_content = front_matter + content
    
    safe_title = get_valid_filename(title)
    md_filename = safe_title + '.md'
    md_filepath = os.path.join(posts_dir, md_filename)
    
    if os.path.exists(md_filepath):
        md_filename = date_str + '-' + safe_title + '.md'
        md_filepath = os.path.join(posts_dir, md_filename)
    
    with open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print('生成文章成功: ' + md_filepath)
    return md_filepath

def main():
    posts_dir = 'source/_posts'
    imgs_dir = 'source/imgs'
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(imgs_dir, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    articles = [
        {
            'title': '好用软件推荐01——FDM下载器',
            'tags': ['软件', '工具'],
            'content': '''装任何软件之前必备一个好的下载器，好的下载器能减少软件下载时间，降低焦虑感。

目前主流的是用IDM，但IDM有两个缺点：
- 不支持磁力链接和 BT 下载
- IDM 是收费软件

那么有没有一款开源且免费功能强大的下载器呢？有，那就是本文主角——FDM。它具备以下几个特点：

- 支持中文
- 支持HTTP/HTTP/FTP/BT 
- 支持多平台（Windows、macOS、Android 和 Linux ）
- 界面简洁无广告
- 开源免费

FDM是IDM的技术模仿者，采用了与IDM一样的多线程分拆与压缩下载技术，这两者在下载效率上几无差距。

**FDM vs 普通浏览器下载速度对比：**

配合上浏览器拓展，点击网站上的下载链接就能打开FDM下载，很是舒服。

**官方下载地址：** [Free Download Manager - 從網路下載任何東西](https://www.freedownloadmanager.org/)

官网下载版本最新最安全，不过可能速度较慢。
'''
        },
        {
            'title': '好用软件推荐02——Snipaste截图工具',
            'tags': ['软件', '工具'],
            'content': '''截图的需求在我们日常使用中很是常见，很多软件内部也集成了截图功能，如微信，QQ等等。但是有时候仅仅只是想截个图就打开如此庞大的软件未免有点大材小用。

有没有一款开源免费又小巧强大的截屏软件呢？有，那就是本文的主角——Snipaste。

Snipaste 是由两个单词 snip(裁剪) + paste(粘贴)组成，其安装包只有 12 M，十分小巧。

可以在官网或是应用商店进行下载：
- **官网：** [Snipaste](https://www.snipaste.com/)
- **应用商店：** [Snipaste 截图+贴图 - Microsoft Store](https://www.microsoft.com/store/productId/9P7WCNK81RLL)

下面说说它的特色功能：

**1. 截图贴图十分便捷**
不同于微信的组合快捷键，Snipaste 截图（F1），贴图（F3）十分便捷。

**2. 有截图置顶功能**
这个功能很是方便，微信是没有置顶功能的。很多时候想对比两张或多张图的区别很是麻烦切来切去的，而Snipaste可以做到多张图片同时置顶，在对比差异或者图片拼接的时候很是方便。

**3. 橡皮擦功能**
微信截图写文字/画笔/马赛克后，想取消最开始某个只能依次按撤回按钮，而 Snipaste 具有橡皮擦功能则很好解决了这一痛点。

**4. 调整截图质量**
Snipaste 支持设置截图质量，在首选项-输出-图像质量中可以自行调整，默认是 -1 即自动调整成图质量。

**5. 吸取像素颜色值**
F1 截图后鼠标移至目标像素位置即可显示颜色值，按 C 可以复制颜色值，对于设计师和前端开发者很是实用！

其他功能像 框选/箭头/画笔/马赛克/文本 的功能应有尽有，可以说是非常强大。

非要挑个不足的话就是不支持图片文本识别和加入表情，如果你对这两个功能十分看重，那还是乖乖用回微信自带的截图功能吧。

**温馨提示：** 可以在首选项设置中开启“开机自启”，这样就方便截图操作，反正占内存也不大！
'''
        },
        {
            'title': '好用软件推荐03——Captura录屏工具',
            'tags': ['软件', '工具'],
            'content': '''「好用软件推荐」系列一直坚持输出“开源、小巧、免费、无广告”的应用。

今天给大家带来的一款录屏应用——Captura。

**介绍：**
Captura 是国外开发者 MathewSachin 个人开源在 github 的应用。体积小巧只有2.45 M, 但功能却十分强大。

**功能特性：**
- 支持区域录屏
- 支持 gif 录制
- 支持屏幕截屏
- 可以选择是否显示鼠标
- 记录鼠标点击、键盘按键
- 支持计时器
- 支持声音录制
- 也可以从网络摄像头捕获

**Github下载地址：** [Captura v8.0.0 · GitHub](https://github.com/MathewSachin/Captura/releases)

**安装使用：**

1. 下载安装完毕第一步选择切换语言

2. **录制屏幕：**
   你可以选择 shareAvi 模式录制 .avi 视频而无需下载其他东西。
   Captura 也可以依赖于另一个开源免费的多媒体程序框架 FFmpeg 输出 MP4/Stream 等多种格式，功能更强大。
   [Download FFmpeg](https://ffmpeg.org/download.html)

3. **Gif 录制：**
   可以选中全屏或者区域录制 GIF，十分便捷，也可以少去一个Gif 录制工具。

麻雀虽小，但五脏俱全！

PS: Window 自带的 xbox 也可以录屏，不过是全屏。如果你没有特别的需求用自带的也够用了！
'''
        },
        {
            'title': '好用软件推荐04——VLC视频播放器',
            'tags': ['软件', '工具'],
            'content': '''**背景：**

之前在使用 Captura 录屏的时候发现 .avi 格式用爱奇艺万能联播播放很模糊，让我一度以为这个软件有问题。后来用 Window 自带的播放器打开 .avi 视频就很清晰，然而 Window 自带播放器在播放 MP4 格式的时候又只有声音没有画面，再度让我怀疑 Captura 的实力。

直到我遇到了这个强大的视频播放器 VLC 才明白：哦，原来是播放器的问题啊！！

**介绍：**

VLC 是一款免费开源的视频播放器，无广告无捆绑，安装包只有40MB，还支持多平台，包括 Windows、 Linux、Mac OS 、 iOS、 Unix、Android，功能十分强大，目前已有 2 亿多下载量！

**官网：** [VLC：官方网站 - 全平台的自由多媒体解决方案！ - VideoLAN](https://www.videolan.org/vlc/)

**特性：**

**1. 支持硬件解码**
VLC 默认开启硬件解码，通过硬件（GPU）进行视频的解码工作。使用 GPU 解码能够降低 CPU 的工作负荷，降低功耗。播放出来的视频较为流畅，并且能够延长移动设备播放视频的时间。

**2. 支持绝大多数格式视频**
VLC 内置的解码器也很厉害，无需手动安装解码包，就可以播放绝大多数的视频，像是 MPEG-2、 MPEG-4、 H.264,、MKV、 WebM、 WMV、DivX、DVD/VCD、MP3 等等编码的视频都可以播放。

**3. 支持视频格式转化**
在播放列表中选中文件，右键选择保存，选择转化格式和转换目标文件夹，点击开始等待进度条走完则转换成功。又节省了一个视频格式转化器！
'''
        },
        {
            'title': '好用软件推荐05——Dev-sidecar',
            'tags': ['软件', '工具'],
            'content': '''之前推荐的开源软件很多是发布在 Github 上的，而国内的 Github 访问速度又很慢，时常打不开网址，今天就推荐一款访问加速应用——Dev-sidecar。

**介绍：**
Dev-sidecar 中文名”开发者边车“，通过本地代理的方式将 https 请求代理到一些国内的加速通道上。

**特性：**
- DNS 优选
- 请求拦截
- Github 加速
- Stack Overflow 加速
- NPM 加速

**下载安装：**

1. 下载安装包，[官方网址](https://github.com/docmirror/dev-sidecar)
2. 安装根证书
3. 启动代理服务和系统代理

之后打开 Github 可见明显看到访问速度快了许多！

**其他分享：** 两个文件代下网站：
- [GitHub 加速下载 - 在线工具 (ur1.fun)](https://ur1.fun/)
- [GitHub 文件加速 (99988866.xyz)](https://99988866.xyz/)
'''
        },
        {
            'title': '好用软件推荐06——7-zip',
            'tags': ['软件', '工具'],
            'content': '''文件压缩与解压缩在日常工作学习中使用十分普遍。市场中很多压缩软件要么体积庞大，要么带有广告，使用起来十分不方便。

今天推荐一款开源压缩软件——7-zip!

**介绍：**
7-zip是一款免费开源的压缩软件，具有LZMA和LZMA2压缩的7z格式的高压缩比，而其安装包只有1.5MB!

**支持平台：** Windows 11 / 10 / 8 / 7 / Vista / XP / 2022 / 2019 / 2016 / 2012 / 2008 / 2003 / 2000.

**支持的格式：**
- **支持压缩和解压：** 7z, XZ, BZIP2, GZIP, TAR, ZIP and WIM
- **仅支持解压：** APFS, AR, ARJ, CAB, CHM, CPIO, CramFS, DMG, EXT, FAT, GPT, HFS, IHEX, ISO, LZH, LZMA, MBR, MSI, NSIS, NTFS, QCOW2, RAR, RPM, SquashFS, UDF, UEFI, VDI, VHD, VHDX, VMDK, XAR and Z.

并且，对于ZIP和GZIP格式，7-ZIP的压缩比比PKZip和WinZip提供的压缩比高2-10%.

**主要优势：**
- 7z和ZIP格式的强大AES-256加密
- 7z格式的自提取功能
- 与Windows Shell集成
- 强大的文件管理器
- 强大的命令行版本
- FAR Manager插件
- 87种语言的本地化

7-zip集成在右键菜单中，压缩解压十分方便。右键选择添加到压缩包可以进行更高级的压缩选项，如修改压缩格式，压缩方法，压缩等级，加密等等。

麻雀虽小却五脏俱全，十分强大。
'''
        }
    ]
    
    for article in articles:
        create_markdown_file(
            article['title'],
            article['content'],
            date_str,
            article['tags'],
            posts_dir
        )
    
    print('\n所有文章生成完成！')

if __name__ == '__main__':
    main()
