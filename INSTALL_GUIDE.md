# Neat Download Manager 汉化详细安装指南

## 前置条件

1. **已安装 Neat Download Manager**
   - 从官网下载：https://neatdownloadmanager.com
   - 安装到 `/Applications/NeatDownloadManager.app`

2. **已安装 Xcode Command Line Tools**（提供 `codesign` 命令）
   ```bash
   xcode-select --install
   ```

3. **已安装 Python 3**（仅生成自定义汉化时需要）
   ```bash
   python3 --version
   ```

---

## 安装步骤

### 第一步：下载汉化补丁

```bash
git clone https://github.com/hardwin/NeatDownloadManager-zh.git
cd NeatDownloadManager-zh
```

或直接从 GitHub 下载 ZIP 压缩包并解压。

### 第二步：运行安装脚本

```bash
./install.sh
```

脚本会自动完成所有操作。如果你更喜欢手动操作，请参考以下步骤。

### 手动安装

#### 1. 关闭 Neat Download Manager

```bash
pkill -f NeatDownloadManager
```

#### 2. 备份原始应用（强烈推荐）

```bash
cp -R /Applications/NeatDownloadManager.app ~/Desktop/NeatDownloadManager.app.backup
```

#### 3. 移除代码签名

macOS 会保护已签名的应用，直接修改会报 "Operation not permitted" 错误。需要先移除签名：

```bash
codesign --remove-signature /Applications/NeatDownloadManager.app
```

#### 4. 复制汉化后的 NIB 文件

```bash
cp -R translated_nibs/*.nib /Applications/NeatDownloadManager.app/Contents/Resources/
```

#### 5. 重新签名

```bash
codesign --force --deep --sign - /Applications/NeatDownloadManager.app
```

#### 6. 验证签名

```bash
codesign --verify --deep --strict /Applications/NeatDownloadManager.app
```

如果没有输出任何错误信息，说明签名验证通过。

#### 7. 启动应用

```bash
open /Applications/NeatDownloadManager.app
```

NDM 是状态栏应用，启动后会在菜单栏显示图标。点击图标即可看到汉化后的界面。

---

## 首次打开可能遇到的问题

### 问题 1："无法打开，因为无法验证开发者"

汉化后应用使用 ad-hoc 自签名，Gatekeeper 可能会拦截。

**解决方法：**

1. 打开"系统设置" → "隐私与安全性"
2. 在底部找到关于 NeatDownloadManager 的提示
3. 点击"仍要打开"

或者：

1. 在 Finder 中找到 NeatDownloadManager.app
2. 右键点击 → 选择"打开"
3. 在弹出的对话框中点击"打开"

### 问题 2："操作无法完成，因为您没有足够的权限"

```bash
# 检查应用权限
ls -la /Applications/NeatDownloadManager.app

# 如果需要，修复权限
sudo chown -R $(whoami):admin /Applications/NeatDownloadManager.app
```

### 问题 3：应用闪退

可能是 NIB 文件损坏。请重新运行安装脚本，或从备份恢复：

```bash
cp -R ~/Desktop/NeatDownloadManager.app.backup/* /Applications/NeatDownloadManager.app/
codesign --force --deep --sign - /Applications/NeatDownloadManager.app
```

---

## 卸载汉化

### 方法一：使用备份恢复

```bash
pkill -f NeatDownloadManager
cp -R ~/Desktop/NeatDownloadManager.app.backup/* /Applications/NeatDownloadManager.app/
open /Applications/NeatDownloadManager.app
```

### 方法二：重新下载安装

从官网 https://neatdownloadmanager.com 重新下载并安装，会覆盖汉化版本。

### 方法三：使用 install.sh 脚本恢复

```bash
./install.sh --restore
```

---

## 自定义翻译

如果你想修改某些翻译用语，可以编辑 `translate_nib.py` 中的 `TRANSLATIONS` 字典：

```python
TRANSLATIONS = {
    "About NeatDownloadManager": "关于 NeatDownloadManager",  # 修改右侧中文
    "Download": "下载",
    # ... 添加或修改翻译
}
```

修改后重新运行：

```bash
python3 translate_nib.py
# 然后重新安装
./install.sh
```

---

## 常见问题

**Q: 汉化后浏览器扩展还能用吗？**
A: 可以。汉化仅修改应用界面文件，不影响浏览器扩展功能。

**Q: NDM 更新后汉化还在吗？**
A: 不在。NDM 更新会覆盖所有文件，需要重新运行汉化脚本。

**Q: 状态栏菜单的文字为什么还是英文？**
A: 状态栏菜单的部分文字（如 "All Downloads"、"Show Window" 等）硬编码在可执行二进制文件中，不在 NIB 文件内。本补丁仅汉化 NIB 界面文件中的文字。如需完整汉化，需要修改可执行二进制，风险较高。

**Q: 支持 Windows 版吗？**
A: 不支持。本项目仅针对 macOS 版。Windows 版使用不同的界面技术。
