# Neat Download Manager 中文汉化

> Neat Download Manager (NDM) macOS 版界面简体中文汉化补丁

## 项目简介

Neat Download Manager 是一款免费的 macOS/Windows 下载管理器，支持多线程下载、断点续传、浏览器扩展集成等功能。但官方仅提供英文界面，本项目为其 macOS 版提供简体中文汉化。

本项目通过直接修改应用内的二进制 NIB 界面文件（`keyedobjects.nib`）中的字符串对象，并修改可执行二进制中的侧边栏分类标签，实现界面汉化。

## 汉化覆盖范围

| 窗口 | 汉化内容 | 状态 |
|------|----------|------|
| 主窗口 (Main) | 工具栏、列标题、菜单、右键菜单 | ✅ 完成 |
| 关于窗口 (About) | 窗口标题、版权信息、按钮 | ✅ 完成 |
| 设置窗口 (Settings) | 所有标签、按钮、协议选项、代理设置 | ✅ 完成 |
| 下载窗口 (Download) | 工具栏、状态标签、带宽/连接数选项 | ✅ 完成 |
| MKV 下载窗口 | 视频/音频标签、状态信息 | ✅ 完成 |
| URL 窗口 | 新建下载对话框 | ✅ 完成 |
| 属性窗口 (Properties) | 所有属性标签、按钮 | ✅ 完成 |
| 浏览器窗口 (Browsers) | 扩展安装说明、浏览器描述 | ✅ 完成 |
| 认证窗口 (Auth) | 用户名/密码/记住选项 | ✅ 完成 |
| 错误窗口 (Error) | 错误标题、日志文件按钮 | ✅ 完成 |
| 完成窗口 (Complete) | 下载完成提示、打开按钮 | ✅ 完成 |
| 退出窗口 (Quit) | 退出确认、隐藏选项 | ✅ 完成 |
| 等待窗口 (Wait) | URL 过期提示 | ✅ 完成 |
| 侧边栏分类 | Complete/Incomplete/Compressed/Document/Misc | ✅ 完成 |

**总计 200+ 条 UI 字符串翻译，覆盖所有 13 个 NIB 界面文件 + 可执行二进制中的侧边栏分类标签。**

> **注意**：可执行二进制中硬编码的部分状态/错误信息（如 "Download In Progress"、"Application is Up To Date" 等）未汉化。这些文字主要通过程序代码动态设置，覆盖它们需要更复杂的二进制 patch 方案。

## 系统要求

- macOS 10.10 或更高版本
- Neat Download Manager 1.3 (Build 24)
- 已安装 Xcode Command Line Tools（提供 `codesign` 命令）

## 快速安装

### 方式一：自动安装脚本（推荐）

```bash
# 1. 下载本项目
git clone https://github.com/hardwin/NeatDownloadManager-zh.git
cd NeatDownloadManager-zh

# 2. 运行安装脚本
./install.sh
```

脚本会自动完成以下操作：
- 检查 NDM 是否已安装
- 备份原始 nib 文件
- 替换为汉化版本
- 移除旧签名并重新 ad-hoc 签名
- 验证签名完整性

### 方式二：手动安装

```bash
# 1. 关闭正在运行的 NDM
pkill -f NeatDownloadManager

# 2. 备份原始文件（可选但推荐）
cp -R /Applications/NeatDownloadManager.app /Applications/NeatDownloadManager.app.backup

# 3. 移除代码签名（macOS 会保护已签名应用）
codesign --remove-signature /Applications/NeatDownloadManager.app

# 4. 替换 nib 文件
cp -R translated_nibs/*.nib /Applications/NeatDownloadManager.app/Contents/Resources/

# 5. 重新 ad-hoc 签名
codesign --force --deep --sign - /Applications/NeatDownloadManager.app

# 6. 验证签名
codesign --verify --deep --strict /Applications/NeatDownloadManager.app

# 7. 启动应用
open /Applications/NeatDownloadManager.app
```

## 卸载/恢复

### 恢复英文原版

```bash
# 方式一：使用备份
cp -R /Applications/NeatDownloadManager.app.backup/* /Applications/NeatDownloadManager.app/

# 方式二：重新下载安装
# 从官网 https://neatdownloadmanager.com 重新下载安装
```

## 生成自己的汉化补丁

如果你想修改翻译或为其他版本生成汉化，可以使用项目中的 Python 脚本：

```bash
# 1. 确保安装了 Python 3
python3 --version

# 2. 运行汉化脚本（从当前安装的 NDM 生成汉化 nib）
python3 translate_nib.py

# 3. 汉化后的 nib 文件在 work/translated_nibs/ 目录
```

翻译映射表在 `translate_nib.py` 的 `TRANSLATIONS` 字典中，修改对应的中英文即可。

## 技术原理

### 为什么不能直接用文本编辑器修改？

Neat Download Manager 的 NIB 文件是 **二进制 plist 格式**（`keyedobjects.nib`），不是可读的文本。直接用文本编辑器修改会破坏文件结构。

### 为什么不用 macOS 标准的本地化机制？

NDM 没有使用 macOS 标准的本地化机制：
- 没有 `Localizable.strings` 文件
- 没有 `zh-Hans.lproj` 等本地化目录
- 可执行文件中没有调用 `NSBundle localizedStringForKey:` 等本地化 API
- 所有 UI 文字硬编码在 NIB 文件和可执行二进制中

因此无法通过简单地添加语言文件来汉化。

### 本项目的方案

使用 Python 的 `plistlib` 库直接解析二进制 NIB 文件（NSKeyedArchiver 格式），在 `$objects` 数组中查找并替换英文字符串为中文翻译，然后以二进制格式保存。这种方法：

- ✅ 不依赖 Xcode/ibtool
- ✅ 保持文件结构完整
- ✅ 支持任意长度的 UTF-8 中文字符串
- ✅ 同时处理单文件 NIB 和目录格式 NIB

### 代码签名

修改应用资源后，原有的 Developer ID 签名和 Apple 公证会失效。本项目使用 `codesign --force --deep --sign -` 进行 ad-hoc 重签（自签名）。重签后：

- 应用可以正常运行
- Gatekeeper 可能提示"无法验证开发者"，需在"系统设置 → 隐私与安全性"中点击"仍要打开"
- 或在 Finder 中右键点击应用 → 选择"打开"

## 文件结构

```
NeatDownloadManager-zh/
├── README.md                 # 本说明文件
├── INSTALL_GUIDE.md          # 详细安装指南
├── install.sh                # 自动安装脚本
├── translate_nib.py          # 汉化生成脚本（含翻译映射表）
├── translated_nibs/           # 汉化后的 nib 文件
│   ├── NeatAboutWindow.nib
│   ├── NeatAuthWindow.nib
│   ├── NeatBrowsersWindow.nib
│   ├── NeatCompleteWindow.nib
│   ├── NeatCustomButton.nib
│   ├── NeatDownloadWindow.nib/
│   │   ├── keyedobjects.nib
│   │   └── keyedobjects-110000.nib
│   ├── NeatDownloadWindowMKV.nib/
│   ├── NeatErrorWindow.nib
│   ├── NeatPropertiesWindow.nib
│   ├── NeatQuitWindow.nib
│   ├── NeatSettingWindow.nib/
│   ├── NeatUrlWindow.nib
│   └── NeatWaitWindow.nib
└── docs/
    └── translation_table.md  # 完整翻译对照表
```

## 兼容性

- 测试版本：Neat Download Manager 1.3 (Build 24), 2021-07-18
- 测试系统：macOS (Darwin)
- 应用更新后需重新汉化

## 已知限制

1. **可执行二进制中的硬编码字符串未汉化**：部分状态栏提示和错误信息（如 "Download In Progress"、"All Downloads"、"Application is Up To Date" 等）硬编码在可执行文件中，本补丁未覆盖。这些需要十六进制编辑，风险较高。
2. **应用更新会覆盖汉化**：每次 NDM 更新后，需重新运行汉化脚本。
3. **签名状态变化**：汉化后应用失去官方 Developer ID 签名和 Apple 公证，改为 ad-hoc 自签名。

## 许可证

本项目仅提供汉化补丁，不包含 Neat Download Manager 本身。Neat Download Manager 的版权归其原作者 Javad Motallebi 所有。

汉化补丁代码采用 MIT 许可证发布，可自由使用、修改和分发。

## 致谢

- [Neat Download Manager](https://neatdownloadmanager.com) - 感谢 Javad Motallebi 开发的优秀免费下载管理器
- 所有为本项目提供建议和反馈的用户
