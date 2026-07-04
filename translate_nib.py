"""
Neat Download Manager macOS 中文汉化脚本
==========================================

完整汉化 NDM 1.3 的所有界面文字，包括：
1. 13 个 NIB 界面文件（主窗口、设置、下载、MKV下载、URL、属性、错误、完成、等待、浏览器、认证、退出、关于）
2. 主窗口 Base.lproj/NeatMainWindow.nib（macOS 本地化目录）
3. 可执行二进制中的侧边栏分类标签（Video/Audio/Compressed/Document/Misc → 完成/未完成/压缩包/文档/杂）

使用方法：
    python3 translate_nib.py
    
需要：
- Python 3.9+ (plistlib 包含 UID 类)
- NeatDownloadManager.app 位于 /Applications/

技术原理：
- NIB 文件是 NSKeyedArchiver 序列化的二进制 plist
- 使用 plistlib (FMT_BINARY) 加载和保存
- 二进制中字符串以 \\x00 分隔，可用更短的中文替换（用 \\x00 填充）
"""

import plistlib as pl
import os
import sys
import re
import shutil

# ==========================================
# 翻译映射表
# ==========================================

# 主窗口翻译 (Base.lproj/NeatMainWindow.nib)
MAIN_WINDOW_TRANSLATIONS = {
    'Neat Download Manager 1.3': 'Neat 下载管理器 1.3',
    'New URL': '新建下载',
    'Resume': '继续',
    'Browsers': '浏览器',
    'About': '关于',
    'Delete': '删除',
    'Total Quit': '完全退出',
    'Settings': '设置',
    'Stop': '停止',
    'Redownload': '重新下载',
    'Show Window': '显示窗口',
    'Open Folder': '打开文件夹',
    'Open': '打开',
    'Properties': '属性',
    ' File Name': ' 文件名',
    'Size': '大小',
    'Status': '状态',
    'Bandwidth': '带宽',
    'Remaining Time': '剩余时间',
    'Last Try': '上次尝试',
    'Google Chrome': '谷歌浏览器',
}

# 关于窗口
ABOUT_TRANSLATIONS = {
    'About Neat Download Manager': '关于 Neat 下载管理器',
    'Neat Download Manager 1.3': 'Neat 下载管理器 1.3',
    'Application Name:': '应用名称：',
    'Application Version:': '应用版本：',
    'MacOS Version:': 'macOS 版本：',
    'Copyright:': '版权：',
    'Check For Update': '检查更新',
    'Buy License': '购买授权',
    'Visit Website': '访问网站',
}

# 设置窗口
SETTING_TRANSLATIONS = {
    'Settings': '设置',
    'Max Connections per Download': '每个下载的最大连接数',
    'Bandwidth Limit per Download (KB/s)': '每个下载的带宽限制（KB/秒）',
    'Show Download Completion Dialog': '显示下载完成对话框',
    'Create Category Folders': '创建分类文件夹',
    'Download Directory': '下载目录',
    'No Proxy/Socks': '无代理/Socks',
    'HTTP Proxy': 'HTTP 代理',
    'Socks Proxy': 'Socks 代理',
    'Proxy/Socks': '代理/Socks',
    'Use Browser Cookies': '使用浏览器 Cookie',
    'Monitor Clipboard': '监控剪贴板',
    'Run at Login': '开机自启',
    'Quit on Close': '关闭时退出',
    'Check for Updates': '检查更新',
    'Browser Integration': '浏览器集成',
    'Browser Extension': '浏览器扩展',
    'OK': '确定',
    'Cancel': '取消',
    'Apply': '应用',
    'Reset': '重置',
}

# 下载窗口
DOWNLOAD_TRANSLATIONS = {
    'Limit Bandwidth to': '限制带宽为',
    'Remember on Resume': '续传时记住',
    'Show Completion Dialog': '显示完成对话框',
    'Download URL': '下载链接',
    'Save As': '另存为',
    'Start Download': '开始下载',
    'Pause': '暂停',
    'Resume': '继续',
    'Cancel': '取消',
    'Retry': '重试',
    'Delete': '删除',
    'Properties': '属性',
    'Open': '打开',
    'Open Folder': '打开文件夹',
    'Redownload': '重新下载',
    'Speed Limit': '速度限制',
    'Connections': '连接数',
    'URL': '链接',
    'File Name': '文件名',
    'File Size': '文件大小',
    'Downloaded': '已下载',
    'Status': '状态',
    'Remaining Time': '剩余时间',
    'Last Try': '上次尝试',
}

# URL 窗口
URL_TRANSLATIONS = {
    'Enter URL': '输入链接',
    'OK': '确定',
    'Cancel': '取消',
    'Paste': '粘贴',
    'Clear': '清空',
    'Add to Queue': '加入队列',
    'Start Now': '立即开始',
}

# 错误窗口
ERROR_TRANSLATIONS = {
    'Error': '错误',
    'OK': '确定',
    'Cancel': '取消',
    'Retry': '重试',
    'Invalid URL or Unsupported Protocol.': '链接无效或协议不支持。',
    'Invalid FTP Address.': 'FTP 地址无效。',
    'No file name specified in the address.': '地址中未指定文件名。',
    'Connection failed.': '连接失败。',
    'Download failed.': '下载失败。',
    'File not found.': '文件未找到。',
    'Access denied.': '访问被拒绝。',
    'Server error.': '服务器错误。',
}

# 完成窗口
COMPLETE_TRANSLATIONS = {
    'Download Complete': '下载完成',
    'Open': '打开',
    'Open Folder': '打开文件夹',
    'OK': '确定',
    'Close': '关闭',
    'File Name:': '文件名：',
    'File Size:': '文件大小：',
    'Download Time:': '下载耗时：',
    'Average Speed:': '平均速度：',
}

# 等待窗口
WAIT_TRANSLATIONS = {
    'Please Wait...': '请稍候...',
    'Connecting...': '连接中...',
    'Downloading...': '下载中...',
    'Cancel': '取消',
}

# 浏览器窗口
BROWSER_TRANSLATIONS = {
    'Browser Integration': '浏览器集成',
    'Google Chrome': '谷歌浏览器',
    'Mozilla Firefox': '火狐浏览器',
    'Safari': 'Safari',
    'Opera': 'Opera',
    'Microsoft Edge': '微软 Edge',
    'Install Extension': '安装扩展',
    'Uninstall Extension': '卸载扩展',
    'Open Extension Page': '打开扩展页面',
}

# 认证窗口
AUTH_TRANSLATIONS = {
    'Authentication Required': '需要身份验证',
    'Username:': '用户名：',
    'Password:': '密码：',
    'OK': '确定',
    'Cancel': '取消',
    'Save Password': '保存密码',
    'Server:': '服务器：',
    'Realm:': '域：',
}

# 退出窗口
QUIT_TRANSLATIONS = {
    'Quit Neat Download Manager?': '退出 Neat 下载管理器？',
    'Downloads are in progress.': '下载正在进行中。',
    'Quit': '退出',
    'Cancel': '取消',
    'Are you sure you want to quit?': '确定要退出吗？',
}

# 属性窗口
PROPERTY_TRANSLATIONS = {
    'Properties': '属性',
    'URL': '链接',
    'File Name': '文件名',
    'File Size': '文件大小',
    'Downloaded': '已下载',
    'Status': '状态',
    'Date Added': '添加日期',
    'Last Try': '上次尝试',
    'Download Path': '下载路径',
    'Save As': '另存为',
    'Speed Limit': '速度限制',
    'Connections': '连接数',
    'Headers': '请求头',
    'OK': '确定',
    'Cancel': '取消',
    'Apply': '应用',
}

# 自定义按钮
CUSTOM_BUTTON_TRANSLATIONS = {
    'New URL': '新建下载',
    'Resume': '继续',
    'Stop': '停止',
    'Delete': '删除',
    'Settings': '设置',
    'About': '关于',
}

# 整合所有 NIB 翻译
NIB_TRANSLATIONS = {
    'NeatMainWindow': MAIN_WINDOW_TRANSLATIONS,
    'NeatAboutWindow': ABOUT_TRANSLATIONS,
    'NeatSettingWindow': SETTING_TRANSLATIONS,
    'NeatDownloadWindow': DOWNLOAD_TRANSLATIONS,
    'NeatDownloadWindowMKV': DOWNLOAD_TRANSLATIONS,
    'NeatUrlWindow': URL_TRANSLATIONS,
    'NeatErrorWindow': ERROR_TRANSLATIONS,
    'NeatCompleteWindow': COMPLETE_TRANSLATIONS,
    'NeatWaitWindow': WAIT_TRANSLATIONS,
    'NeatBrowsersWindow': BROWSER_TRANSLATIONS,
    'NeatAuthWindow': AUTH_TRANSLATIONS,
    'NeatQuitWindow': QUIT_TRANSLATIONS,
    'NeatPropertiesWindow': PROPERTY_TRANSLATIONS,
    'NeatCustomButton': CUSTOM_BUTTON_TRANSLATIONS,
}

# 二进制中的侧边栏分类标签
# 原: Complete\0Incomplete\0Compressed\0Document\0Misc\0
BINARY_CATEGORIES = {
    'pos1': {
        'offset': 1586332,
        'length': 45,
        'original': b'Complete\x00Incomplete\x00Compressed\x00Document\x00Misc\x00',
        'translation': [('Complete', '完成'), ('Incomplete', '未完成'),
                        ('Compressed', '压缩包'), ('Document', '文档'), ('Misc', '杂')],
    },
    'pos2': {
        'offset': 605042,
        'length': 29,
        'original': b'Complete\x00Incomplete\x00Document\x00',
        'translation': [('Complete', '完成'), ('Incomplete', '未完成'),
                        ('Document', '文档')],
    },
}


# ==========================================
# 核心函数
# ==========================================

def translate_nib_file(nib_path, translations, output_path):
    """
    翻译单个 nib 文件（二进制 plist 格式）
    
    Args:
        nib_path: 源 nib 文件路径
        translations: {英文: 中文} 映射
        output_path: 输出 nib 文件路径
    Returns:
        替换数量
    """
    with open(nib_path, 'rb') as f:
        data = pl.load(f)
    
    objects = data.get('$objects', [])
    replaced = 0
    for i, obj in enumerate(objects):
        if isinstance(obj, str) and obj in translations:
            objects[i] = translations[obj]
            replaced += 1
    
    os.makedirs(os.path.dirname(output_path) if os.path.isdir(output_path) == False and '/' in output_path else '.', exist_ok=True)
    
    # 关键：使用 FMT_BINARY 保持二进制格式
    with open(output_path, 'wb') as f:
        pl.dump(data, f, fmt=pl.FMT_BINARY)
    
    return replaced


def translate_nib_directory(nib_dir, translations, output_dir):
    """
    翻译整个 nib 目录（含 keyedobjects.nib 和 keyedobjects-110000.nib）
    """
    total = 0
    for fname in os.listdir(nib_dir):
        if fname.endswith('.nib'):
            src = os.path.join(nib_dir, fname)
            dst = os.path.join(output_dir, fname)
            n = translate_nib_file(src, translations, dst)
            total += n
            print(f"  {fname}: 替换 {n} 处")
    return total


def translate_binary(bin_path, output_path):
    """
    翻译二进制中的侧边栏分类标签
    """
    with open(bin_path, 'rb') as f:
        data = bytearray(f.read())
    
    total = 0
    for key, info in BINARY_CATEGORIES.items():
        offset = info['offset']
        length = info['length']
        original = info['original']
        trans = info['translation']
        
        # 验证原内容
        actual = bytes(data[offset:offset+length])
        if actual != original:
            print(f"  警告: 区域 {key} (偏移 {offset}) 内容不匹配")
            print(f"    期望: {original!r}")
            print(f"    实际: {actual!r}")
            continue
        
        # 构建新内容
        new = b''
        for en, zh in trans:
            new += zh.encode('utf-8') + b'\x00'
        
        # 用 \x00 填充到原长度
        if len(new) < length:
            new += b'\x00' * (length - len(new))
        elif len(new) > length:
            print(f"  错误: 区域 {key} 新内容 {len(new)} 字节超过原 {length} 字节，跳过")
            continue
        
        data[offset:offset+length] = new
        total += 1
        print(f"  区域 {key} (偏移 {offset}, {length} 字节): 已替换")
    
    with open(output_path, 'wb') as f:
        f.write(data)
    return total


# ==========================================
# 主流程
# ==========================================

def main():
    app_path = '/Applications/NeatDownloadManager.app'
    work_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(work_dir, 'translated_nibs')
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(app_path):
        print(f"错误: 找不到 {app_path}")
        sys.exit(1)
    
    res_dir = os.path.join(app_path, 'Contents/Resources')
    
    total_nib = 0
    print("=" * 60)
    print("NIB 文件汉化")
    print("=" * 60)
    for nib_name, translations in NIB_TRANSLATIONS.items():
        # 主窗口在 Base.lproj 下
        if nib_name == 'NeatMainWindow':
            nib_path = os.path.join(res_dir, 'Base.lproj', f'{nib_name}.nib')
        else:
            nib_path = os.path.join(res_dir, f'{nib_name}.nib')
        
        if not os.path.exists(nib_path):
            print(f"  跳过 {nib_name}: 文件不存在")
            continue
        
        if os.path.isdir(nib_path):
            # 目录格式
            if nib_name == 'NeatMainWindow':
                out_subdir = os.path.join(output_dir, 'Base.lproj', f'{nib_name}.nib')
            else:
                out_subdir = os.path.join(output_dir, f'{nib_name}.nib')
            n = translate_nib_directory(nib_path, translations, out_subdir)
        else:
            # 单文件格式
            out_file = os.path.join(output_dir, f'{nib_name}.nib')
            n = translate_nib_file(nib_path, translations, out_file)
            print(f"  {nib_name}: 替换 {n} 处")
        total_nib += n
    
    print(f"\nNIB 总翻译: {total_nib} 处")
    
    # 二进制标签
    print("\n" + "=" * 60)
    print("二进制侧边栏分类标签汉化")
    print("=" * 60)
    bin_path = os.path.join(app_path, 'Contents/MacOS/NeatDownloadManager')
    output_bin = os.path.join(work_dir, 'translated_nibs', 'NeatDownloadManager')
    
    if os.path.exists(bin_path):
        n = translate_binary(bin_path, output_bin)
        os.chmod(output_bin, 0o755)
        print(f"\n二进制标签: {n} 处区域已替换")
        print(f"已输出到: {output_bin}")
    else:
        print(f"  警告: 找不到 {bin_path}")


if __name__ == '__main__':
    main()
