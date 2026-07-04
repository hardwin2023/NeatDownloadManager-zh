#!/bin/bash
# 编译翻译后的 xib 文件为 nib

XIB_DIR="/Users/mac/WorkBuddy/2026-07-05-01-43-45/ndm-zh/work/xib_translated"
OUT_DIR="/Users/mac/WorkBuddy/2026-07-05-01-43-45/ndm-zh/work/translated_nibs"
APP_RES="/Applications/NeatDownloadManager.app/Contents/Resources"

mkdir -p "$OUT_DIR"

cd "$XIB_DIR"

for f in *.xib; do
    name="${f%.xib}"
    echo -n "编译 $name... "

    if [ -d "${APP_RES}/${name}.nib" ]; then
        # Directory-format nib
        tmpdir="/tmp/nib_${name}"
        rm -rf "$tmpdir"
        mkdir -p "$tmpdir"

        ibtool --compile "${tmpdir}/keyedobjects.nib" "$f" 2>/dev/null

        # Copy 110000 variant from original
        cp "${APP_RES}/${name}.nib/keyedobjects-110000.nib" "$tmpdir/" 2>/dev/null

        # Create output
        outdir="${OUT_DIR}/${name}.nib"
        rm -rf "$outdir"
        mkdir -p "$outdir"
        cp "${tmpdir}/keyedobjects.nib" "$outdir/"
        cp "${tmpdir}/keyedobjects-110000.nib" "$outdir/" 2>/dev/null

        rm -rf "$tmpdir"
        echo "done (dir)"
    else
        # Single-file nib
        ibtool --compile "${OUT_DIR}/${name}.nib" "$f" 2>/dev/null
        echo "done (file)"
    fi
done

echo "=== 全部编译完成 ==="
ls -la "$OUT_DIR"
