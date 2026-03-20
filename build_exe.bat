@echo off
chcp 65001 >nul
echo ============================================================
echo   arXiv 論文取得・要約スクリプト - exe ビルド (onedir)
echo ============================================================
echo.

REM PyInstallerがインストールされているか確認
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller が見つかりません。インストールします...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller のインストールに失敗しました。
        pause
        exit /b 1
    )
)

REM 前回ビルドの残骸を削除
if exist "build" rmdir /s /q build
if exist "dist\arxiv_cli" rmdir /s /q "dist\arxiv_cli"

echo PyInstaller (onedir) でビルドを開始します...
echo.

pyinstaller --onedir --console --noupx --name arxiv_cli arxiv_cli.py

if errorlevel 1 (
    echo.
    echo ❌ ビルドに失敗しました。
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ ビルド完了！
echo.
echo   出力先: dist\arxiv_cli\
echo.
echo   配布時に必要なファイル:
echo     dist\arxiv_cli\ フォルダごとコピーしてください
echo     config.ini は初回実行時に自動生成されます
echo ============================================================
echo.

REM config.ini.template があればコピー（参考用）
if exist "config.ini.template" (
    copy /Y "config.ini.template" "dist\arxiv_cli\config.ini" >nul
    echo config.ini.template を dist\arxiv_cli\config.ini にコピーしました。
)

echo.
pause
