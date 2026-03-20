@echo off
chcp 65001 >nul
echo ============================================================
echo   arXiv 論文取得・要約スクリプト - exe ビルド
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

echo PyInstaller でビルドを開始します...
echo.

pyinstaller arxiv_cli.spec

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
echo     - dist\arxiv_cli\arxiv_cli.exe  （実行ファイル）
echo     - dist\arxiv_cli\config.ini      （設定ファイル）
echo ============================================================
echo.

REM config.ini を dist フォルダにコピー
if exist "config.ini.template" (
    copy /Y "config.ini.template" "dist\arxiv_cli\config.ini" >nul
    echo config.ini.template を dist\arxiv_cli\config.ini にコピーしました。
) else if exist "config.ini" (
    copy /Y "config.ini" "dist\arxiv_cli\config.ini" >nul
    echo config.ini を dist\arxiv_cli\ にコピーしました。
)

echo.
pause
