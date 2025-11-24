@echo off
REM 自動環境設定腳本 (Windows)
REM 此腳本會自動建立虛擬環境並安裝所有必要套件

setlocal EnableDelayedExpansion

REM 切換到專案根目錄（此腳本在 scripts\ 目錄中）
cd /d "%~dp0\.."

echo.
echo ============================================================
echo C++ Lab 測試系統 - 自動環境設定
echo ============================================================
echo.

REM 檢查 Python 是否安裝
echo ============================================================
echo 1. 檢查 Python 安裝
echo ============================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] 找不到 python 指令
    echo.
    echo 請先安裝 Python 3.7 或更新版本
    echo Windows: 請參考 INSTALLATION.md 的安裝說明
    echo.
    echo 小提示: 可以嘗試使用 py 指令:
    echo   py --version
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [成功] 已找到 %PYTHON_VERSION%

REM 檢查 Python 版本（需要 3.7+）
python -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] Python 版本過舊，需要 Python 3.7 或更新版本
    echo.
    pause
    exit /b 1
)
echo [成功] Python 版本符合要求

REM 建立虛擬環境
echo.
echo ============================================================
echo 2. 建立虛擬環境
echo ============================================================
echo.

if exist "venv\" (
    echo [警告] 虛擬環境目錄 venv\ 已存在
    set /p CHOICE="是否要刪除並重新建立？ (y/N): "
    if /i "!CHOICE!"=="y" (
        echo [警告] 正在刪除舊的虛擬環境...
        rmdir /s /q venv
    ) else (
        echo [警告] 跳過虛擬環境建立
        set SKIP_VENV=1
    )
)

if not defined SKIP_VENV (
    echo 正在建立虛擬環境（這可能需要 10-30 秒）...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [錯誤] 虛擬環境建立失敗
        pause
        exit /b 1
    )
    echo [成功] 虛擬環境建立完成
)

REM 啟動虛擬環境
echo.
echo ============================================================
echo 3. 啟動虛擬環境
echo ============================================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [錯誤] 找不到虛擬環境啟動腳本
    echo [錯誤] 請確認 venv\ 目錄已正確建立
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] 虛擬環境啟動失敗
    echo.
    echo 如果您使用 PowerShell，可能需要執行:
    echo   Set-ExecutionPolicy RemoteSigned
    echo.
    echo 或改用命令提示字元 (cmd)
    pause
    exit /b 1
)
echo [成功] 虛擬環境已啟動

REM 升級 pip
echo.
echo ============================================================
echo 4. 升級 pip
echo ============================================================
echo.

echo 正在升級 pip 到最新版本...
python -m pip install --upgrade pip --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [警告] pip 升級失敗，但可以繼續安裝套件
) else (
    echo [成功] pip 升級完成
)

REM 安裝套件
echo.
echo ============================================================
echo 5. 安裝必要套件
echo ============================================================
echo.

if not exist "requirements.txt" (
    echo [錯誤] 找不到 requirements.txt 檔案
    pause
    exit /b 1
)

echo 正在安裝套件（這可能需要 30-60 秒）...
pip install -r requirements.txt --quiet

if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] 套件安裝失敗
    echo.
    echo 可能原因：
    echo   - 網路連線問題
    echo   - PyPI 伺服器無法訪問
    echo   - 套件版本衝突
    echo.
    echo 請嘗試：
    echo   1. 檢查網路連線
    echo   2. 重新執行此腳本
    echo   3. 手動執行: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [成功] 套件安裝完成

REM 驗證安裝
echo.
echo ============================================================
echo 6. 驗證環境設定
echo ============================================================
echo.

set VERIFICATION_FAILED=0

if exist "scripts\verify_python_setup.py" (
    python scripts\verify_python_setup.py
    if %ERRORLEVEL% NEQ 0 (
        set VERIFICATION_FAILED=1
        echo [警告] 環境驗證未完全通過，但您仍可以嘗試使用系統
    )
) else (
    echo [警告] 找不到驗證腳本，跳過驗證
)

REM 完成
echo.
echo ============================================================
echo 設定完成！
echo ============================================================
echo.

if %VERIFICATION_FAILED%==0 (
    echo 環境已設定完成。每次使用時，請記得啟動虛擬環境：
) else (
    echo 環境設定已完成，但驗證有警告。每次使用時，請記得啟動虛擬環境：
)
echo.
echo   venv\Scripts\activate
echo.
echo 接下來可以執行：
echo   python run_tests.py        # 執行所有測試
echo   python run_tests.py --gui  # 啟動網頁介面
echo.
echo 更多使用說明請參考 README_STUDENT.md
echo.

pause

