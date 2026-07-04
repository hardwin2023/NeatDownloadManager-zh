#!/usr/bin/env python3
"""
Neat Download Manager NIB 汉化脚本
将 xib (XML plist) 中的英文 UI 字符串替换为中文翻译
"""

import os
import re
import sys

# ============================================================
# 翻译映射表 (英文 → 中文)
# 仅翻译用户可见的 UI 文字，跳过类名/标识符/选择器/颜色名等
# ============================================================

TRANSLATIONS = {
    # --- 关于窗口 ---
    "About NeatDownloadManager": "关于 NeatDownloadManager",
    "( Basic Version - Free License )": "( 基础版 - 免费许可证 )",
    "Copyright © 2021 Javad Motallebi , All rights reserved.": "版权所有 © 2021 Javad Motallebi，保留所有权利。",
    "Website : neatdownloadmanager.com": "网站：neatdownloadmanager.com",
    "Contact : support@neatdownloadmanager.com": "联系方式：support@neatdownloadmanager.com",
    "Check For Update": "检查更新",
    "OK": "确定",

    # --- 设置窗口 ---
    "Neat Download Manager Settings": "Neat Download Manager 设置",
    "General": "常规",
    "Download Directory": "下载目录",
    "Directory doesn't exist": "目录不存在",
    "Max Connections  per Download": "每个下载最大连接数",
    "8 Connections Recommended": "推荐 8 个连接",
    "0 or blank for No limit": "0 或留空表示不限速",
    "Bandwidth Limit per Download (KB/s)": "单个下载带宽限制 (KB/s)",
    "Show Download Completion Dialog": "显示下载完成对话框",
    "Create Category Folders ( e.g.  Video, Document, ...  )": "创建分类文件夹（如：视频、文档等）",
    "Start Application on System Startup ( Recommended )": "开机时启动应用（推荐）",
    "Default User-Agent": "默认 User-Agent",
    "Use this UA for both Manual and Browser-Sent Downloads ( Be Careful )": "手动和浏览器发送的下载均使用此 UA（请谨慎使用）",
    "Please Correct Red-Labeled Item": "请修正标红的项",
    "When first Connection Starts Downloading  , :": "当首个连接开始下载时：",
    "Create Additional Connections All at Once": "同时创建所有附加连接",
    "Create Additional Connections One by One": "逐一创建附加连接",
    "Protocol": "协议",
    "FTP Protocol": "FTP 协议",
    "HTTPS Protocol": "HTTPS 协议",
    "Address": "地址",
    "Port": "端口",
    "User": "用户名",
    "Password": "密码",
    "Passwords": "密码管理",
    "Credentials": "凭证",
    "Remove": "移除",
    "Reset": "重置",
    "Proxy / Socks": "代理 / Socks",
    "Proxy/Socks": "代理/Socks",
    "No Proxy/Socks": "无代理/Socks",
    "HTTP Proxy": "HTTP 代理",
    "Socks Proxy": "Socks 代理",
    "Socks V4": "Socks V4",
    "Socks V5": "Socks V5",

    # --- 下载窗口 ---
    "Download": "下载",
    "Pause": "暂停",
    "Apply": "应用",
    "Cancel": "取消",
    "Close": "关闭",
    "Options": "选项",
    "Bandwidth": "带宽",
    "Connections": "连接数",
    "Limit Bandwidth  to": "限制带宽为",
    "( 0 or blank = No limit )": "( 0 或留空 = 不限速 )",
    "Remember on Resume": "恢复时记住",
    "Show Completion Dialog": "显示完成对话框",
    "Status": "状态",
    "Link": "链接",
    "Downloaded": "已下载",
    "File Size": "文件大小",
    "Remaining Time": "剩余时间",
    "Resumable": "可断点续传",
    "Segments :": "分片：",
    "KB/sec": "KB/秒",
    "Starting...": "启动中...",
    "No": "否",
    "Unknown": "未知",

    # --- MKV 下载窗口 ---
    "Video": "视频",
    "Audio": "音频",
    "Video Status": "视频状态",
    "Audio Status": "音频状态",
    "Video:": "视频：",
    "Audio:": "音频：",
    "Total Bandwidth": "总带宽",
    "Total Downloaded": "总已下载",
    "Total File Size": "文件总大小",
    "Size:": "大小：",

    # --- URL 窗口 ---
    "New URL": "新建 URL",
    "URL:": "URL：",

    # --- 属性窗口 ---
    "Download Properties": "下载属性",
    "Page Title :": "页面标题：",
    "Page URL :": "页面 URL：",
    "Browser :": "浏览器：",
    "Added on :": "添加日期：",
    "Last Try :": "上次尝试：",
    "Saved to :": "保存至：",
    "Size :": "大小：",
    "Status :": "状态：",
    "URL :": "URL：",
    "(Editable)": "(可编辑)",
    "Open Folder": "打开文件夹",
    "Show Page": "显示页面",
    "Log File": "日志文件",
    "Title": "标题",

    # --- 错误窗口 ---
    "Error": "错误",
    "Error :": "错误：",

    # --- 完成窗口 ---
    "Download Completed": "下载完成",
    "Open": "打开",

    # --- 退出窗口 ---
    "Quit Application Totally": "完全退出应用",
    "Are you sure you want to Quit Totally ?": "确定要完全退出吗？",
    "Hide in Status Menu Area": "隐藏到状态菜单区域",
    "You can hide NeatDownloadManager in Status Menu area by clicking on the MainWindow close button and then bring it to front by clicking on the Status Menu item.":
        "您可以点击主窗口的关闭按钮将 NeatDownloadManager 隐藏到状态菜单区域，然后点击状态菜单项将其重新调出。",

    # --- 认证窗口 ---
    "Authentication": "身份验证",
    "User Name": "用户名",
    "Remember": "记住",

    # --- 等待窗口 ---
    "Renew URL": "更新 URL",
    "The URL has been changed or Download Session has expired.\nYou should Resend URL from Browser to NeatDownloadManager.":
        "URL 已更改或下载会话已过期。\n您需要从浏览器重新发送 URL 到 NeatDownloadManager。",

    # --- 浏览器窗口 ---
    "Browsers": "浏览器",
    "Add Chrome Extension": "添加 Chrome 扩展",
    "Add Firefox Extension": "添加 Firefox 扩展",
    "Add Edge Extension": "添加 Edge 扩展",
    "Installed": "已安装",
    "Show Download Panel on Web Media Players": "在网页媒体播放器上显示下载面板",
    "* Sends download links from Chrome to the application. * Catches Video/Audio links on many websites.\n* YouTube is not supported ( Chrome store doesn't allow )\n* Compatible with Chromium-based browsers like Opera, Brave, ...":
        "* 将下载链接从 Chrome 发送到本应用。* 捕获多种网站的视频/音频链接。\n* 不支持 YouTube（Chrome 商店不允许）\n* 兼容 Opera、Brave 等 Chromium 内核浏览器...",
    "* Sends download links from Firefox to the application. * Catches Video/Audio links on many websites.\n* YouTube is supported partially.":
        "* 将下载链接从 Firefox 发送到本应用。* 捕获多种网站的视频/音频链接。\n* 部分支持 YouTube。",
    "* Sends download links from Edge to the application. * Catches Video/Audio links on many websites.\n* YouTube is supported partially.":
        "* 将下载链接从 Edge 发送到本应用。* 捕获多种网站的视频/音频链接。\n* 部分支持 YouTube。",
    "A Safari extension (with limited functionality and known issues) is available too. In Safari 'Develop' menu select 'Allow Unsigned Extensions' and then activate it in Safari-&gt;Preferences-&gt;Extensions (Safari 14 and later)  Note: When the extension catches a download, user should cancel the download inside the browser manually.":
        "也提供 Safari 扩展（功能有限且有已知问题）。在 Safari 的\"开发\"菜单中选择\"允许未签名的扩展\"，然后在 Safari-&gt;偏好设置-&gt;扩展中启用（Safari 14 及以上版本）。注意：当扩展捕获下载时，用户需手动在浏览器中取消下载。",
}


def translate_xib(xib_path, output_path):
    """翻译 xib 文件中的英文字符串"""
    with open(xib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = 0
    for eng, chs in TRANSLATIONS.items():
        # Match <string>exact_text</string>
        # Use a function to handle special regex characters
        escaped = re.escape(eng)
        pattern = f'<string>{escaped}</string>'
        replacement = f'<string>{chs}</string>'
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            replacements += count

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return replacements


def main():
    xib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'xib')
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'xib_translated')

    os.makedirs(out_dir, exist_ok=True)

    total = 0
    for fname in sorted(os.listdir(xib_dir)):
        if not fname.endswith('.xib'):
            continue
        src = os.path.join(xib_dir, fname)
        dst = os.path.join(out_dir, fname)
        count = translate_xib(src, dst)
        total += count
        print(f"  {fname}: {count} 处翻译")

    print(f"\n总计翻译: {total} 处")


if __name__ == '__main__':
    main()
