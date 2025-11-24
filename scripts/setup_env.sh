#!/usr/bin/env bash
#
# 自動環境設定腳本 (macOS/Linux)
# 此腳本會自動建立虛擬環境並安裝所有必要套件
#

set -e  # 遇到錯誤時停止執行

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# 印出標題
print_header() {
    echo ""
    echo -e "${BOLD}${BLUE}============================================================${NC}"
    echo -e "${BOLD}${BLUE}$1${NC}"
    echo -e "${BOLD}${BLUE}============================================================${NC}"
    echo ""
}

# 印出成功訊息
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# 印出錯誤訊息
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# 印出警告訊息
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 切換到專案根目錄（此腳本在 scripts/ 目錄中）
cd "$(dirname "$0")/.."

print_header "C++ Lab 測試系統 - 自動環境設定"

# 檢查 Python 3 是否安裝
print_header "1. 檢查 Python 安裝"

if ! command -v python3 &> /dev/null; then
    print_error "找不到 python3 指令"
    echo ""
    echo "請先安裝 Python 3.7 或更新版本"
    echo "macOS: 請參考 INSTALLATION.md 的安裝說明"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
print_success "已找到 $PYTHON_VERSION"

# 檢查 Python 版本
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    print_error "Python 版本過舊（需要 3.7+）"
    exit 1
fi

print_success "Python 版本符合要求"

# 建立虛擬環境
print_header "2. 建立虛擬環境"

if [ -d "venv" ]; then
    print_warning "虛擬環境目錄 venv/ 已存在"
    read -p "是否要刪除並重新建立？ (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_warning "正在刪除舊的虛擬環境..."
        rm -rf venv
    else
        print_warning "跳過虛擬環境建立"
        SKIP_VENV=1
    fi
fi

if [ -z "$SKIP_VENV" ]; then
    echo "正在建立虛擬環境（這可能需要 10-30 秒）..."
    python3 -m venv venv
    print_success "虛擬環境建立完成"
fi

# 啟動虛擬環境
print_header "3. 啟動虛擬環境"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    if [ $? -eq 0 ]; then
        print_success "虛擬環境已啟動"
    else
        print_error "虛擬環境啟動失敗"
        exit 1
    fi
else
    print_error "找不到虛擬環境啟動腳本"
    print_error "請確認 venv/ 目錄已正確建立"
    exit 1
fi

# 升級 pip
print_header "4. 升級 pip"

echo "正在升級 pip 到最新版本..."
python -m pip install --upgrade pip --quiet

if [ $? -eq 0 ]; then
    print_success "pip 升級完成"
else
    print_warning "pip 升級失敗，但可以繼續安裝套件"
fi

# 安裝套件
print_header "5. 安裝必要套件"

if [ ! -f "requirements.txt" ]; then
    print_error "找不到 requirements.txt 檔案"
    exit 1
fi

echo "正在安裝套件（這可能需要 30-60 秒）..."
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    print_success "套件安裝完成"
else
    print_error "套件安裝失敗"
    echo ""
    echo "可能原因："
    echo "  - 網路連線問題"
    echo "  - PyPI 伺服器無法訪問"
    echo "  - 套件版本衝突"
    echo ""
    echo "請嘗試："
    echo "  1. 檢查網路連線"
    echo "  2. 重新執行此腳本"
    echo "  3. 手動執行: pip install -r requirements.txt"
    exit 1
fi

# 驗證安裝
print_header "6. 驗證環境設定"

VERIFICATION_FAILED=0

if [ -f "scripts/verify_python_setup.py" ]; then
    python scripts/verify_python_setup.py
    if [ $? -ne 0 ]; then
        VERIFICATION_FAILED=1
        print_warning "環境驗證未完全通過，但您仍可以嘗試使用系統"
    fi
else
    print_warning "找不到驗證腳本，跳過驗證"
fi

# 完成
print_header "設定完成！"

if [ $VERIFICATION_FAILED -eq 0 ]; then
    echo "環境已設定完成。每次使用時，請記得啟動虛擬環境："
else
    echo "環境設定已完成，但驗證有警告。每次使用時，請記得啟動虛擬環境："
fi
echo ""
echo -e "${BOLD}  source venv/bin/activate${NC}"
echo ""
echo "接下來可以執行："
echo -e "${BOLD}  python3 run_tests.py${NC}        # 執行所有測試"
echo -e "${BOLD}  python3 run_tests.py --gui${NC}  # 啟動網頁介面"
echo ""
echo "更多使用說明請參考 README_STUDENT.md"
echo ""

