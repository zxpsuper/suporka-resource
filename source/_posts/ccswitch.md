---
title: CC Switch — AI 编程 CLI 的万能遥控器
date: 2026-05-21
cover: /imgs/cc-switch.webp
top_img: /imgs/cc-switch.webp
description: CC Switch 是一款开源的跨平台桌面工具，统一管理 Claude Code、Codex、Gemini CLI 等主流 AI 编程 CLI，支持一键切换提供商、MCP/Skills 统一管理、用量追踪等功能。
keywords: [CC Switch,AI编程,Claude Code,Codex,Gemini CLI,MCP,Skills]
categories:
  - 软件
tags:
  - AI
  - 开发工具
---

如果你在用 AI 编程工具写代码，那你大概率遇到过这些情况：

Claude Code 一个配置格式，Codex 又是一个格式，Gemini CLI 还不一样。想换个 API 提供商？手动改 JSON、改 TOML、改 `.env` 文件，一套操作下来头都大了。

更别说 MCP 配置、Skills 管理要在不同工具之间各配一遍，纯纯的重复劳动。

有没有一个工具能把这些统一管起来？

有。这就是 **CC Switch**——一个开源的跨平台桌面应用，让你用一个界面管理所有主流 AI 编程 CLI 工具。

目前在 GitHub 上已有 **76,000+ Star**，是 AI 开发工具领域增长最快的开源项目之一。

---

## 什么是 CC Switch？

CC Switch 是一款基于 Tauri 2 构建的原生桌面应用（Rust + React），支持 Windows、macOS 和 Linux 三大平台。它可以统一管理以下 AI 编程 CLI 工具：

- **Claude Code**
- **Codex**（OpenAI）
- **Gemini CLI**（Google）
- **OpenCode**
- **OpenClaw**
- **Hermes Agent**

它的核心理念很简单——**所有配置、一个界面、随意切换**。

---

## 核心功能

### 1. 50+ 提供商预设，一键切换

内置 50+ 提供商预设，覆盖官方渠道和主流中转服务：

- AWS Bedrock、NVIDIA NIM
- MiniMax、SiliconFlow 等国内平台
- 各类社区中转服务

你只需要复制 API Key，点击导入即可使用。切换提供商时也只需点一下，再也不用翻文件夹找配置文件了。

> 系统托盘也支持直接切换，不用打开主界面，效率拉满。

### 2. 统一管理 MCP 与 Skills

MCP（Model Context Protocol）服务器和 Skills 是 AI 编程 CLI 的重要扩展能力，但不同工具的配置各不相同。

CC Switch 提供了一个统一的管理面板，支持：
- **MCP 管理** — 跨 4 个应用同步配置，支持 Deep Link 导入
- **Prompts 管理** — Markdown 编辑器，跨应用同步 CLAUDE.md / AGENTS.md / GEMINI.md
- **Skills 管理** — 从 GitHub 仓库或 ZIP 文件一键安装到所有应用


### 3. 代理与故障转移

内置本地代理功能，支持：
- 格式自动转换
- **自动故障转移** — 一个提供商挂了自动切换到备用
- **熔断机制** — 保护你的 API 调用不被异常拖垮
- **健康监控** — 实时查看各提供商状态
- **请求整流** — 智能路由优化

### 4. 用量与费用追踪

担心 AI 编程 API 花太多钱？CC Switch 内置了用量仪表盘：
- 实时追踪各提供商的花费、请求数、Token 消耗
- 趋势图表展示
- 详细的请求日志
- 支持自定义单模型定价

每一分钱花在哪，清清楚楚。

### 5. 会话管理

可以跨应用浏览、搜索和恢复历史对话。Claude Code、Codex、Gemini CLI 的聊天记录集中管理，想找回之前某次对话的内容不用翻终端输出了。

### 6. 云同步

支持将配置同步到多个设备：
- Dropbox、OneDrive、iCloud、NAS 自定义目录
- WebDAV 服务器同步
- 配置随身走，换电脑不重配

---

## 数据安全

CC Switch 的数据全部存储在本地 SQLite 数据库中，不会上传到任何第三方服务器：

- 数据文件：`~/.cc-switch/cc-switch.db`
- 原子写入机制 — 防止配置写入时损坏
- 自动备份 — 保留最近 10 个版本
- 卸载前自动备份 Skills 数据，保留最近 20 个版本

即使你卸载了 CC Switch，对应的 CLI 工具依然可以正常工作——它遵循"最小侵入"设计原则。

---

## 下载安装

CC Switch 完全开源免费（MIT 协议）。跨平台支持：

### Windows

下载 `CC-Switch-{版本}-Windows.msi` 安装包或 `Windows-Portable.zip` 便携版。

### macOS

推荐通过 Homebrew 安装：

```bash
brew install --cask cc-switch
```

或下载 `.dmg` 安装包，已通过 Apple 公证，可直接安装。

### Linux

支持 `.deb`（Debian/Ubuntu）、`.rpm`（Fedora/RHEL）和 `.AppImage` 通用格式。

---

## 结语

如果你正在使用 AI 编程 CLI 工具，而且手上有多个 API 提供商或者多台设备，CC Switch 绝对能帮你省下大量时间。它把 AI 编程工具的后勤工作做到极致——管配置、管 MCP、管 Skills、管费用、管会话，让你只管专心写代码。

**官网：** [ccswitch.io](https://ccswitch.io)
**GitHub：** [github.com/farion1231/cc-switch](https://github.com/farion1231/cc-switch)

**备份下载地址：** [CC Switch](https://pan.quark.cn/s/3b706c3b28a0)