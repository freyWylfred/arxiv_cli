# -*- mode: python ; coding: utf-8 -*-
# ========================================
# arxiv_cli.spec
# ========================================
# PyInstaller ビルド設定ファイル
#
# ビルド方法:
#   pyinstaller arxiv_cli.spec
#
# または:
#   build_exe.bat を実行
# ========================================

import sys
import os

block_cipher = None

a = Analysis(
    ['arxiv_cli.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'feedparser',
        'requests',
        'fitz',
        'fitz.fitz',
        'openai',
        'pandas',
        'openpyxl',
        'openpyxl.worksheet.hyperlink',
        'configparser',
        'urllib.parse',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'PIL',
        'IPython',
        'jupyter',
        'notebook',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='arxiv_cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,          # コンソールウィンドウを表示（ログ出力のため）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='arxiv_cli',
)
