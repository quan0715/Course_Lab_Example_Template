#!/usr/bin/env python3
"""
Python 環境驗證腳本
檢查 Python 版本和必要套件是否已正確安裝
"""

import sys
import os
from pathlib import Path

# 顏色輸出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header(text):
    """印出標題"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """印出成功訊息"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """印出錯誤訊息"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    """印出警告訊息"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def check_python_version():
    """檢查 Python 版本"""
    print_header("檢查 Python 版本")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"當前 Python 版本: {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_error(f"Python 版本過舊！需要 Python 3.7 或更新版本")
        print(f"  請前往 https://www.python.org/downloads/ 下載最新版本")
        return False
    else:
        print_success(f"Python 版本符合要求（需要 3.7+）")
        return True

def check_package(package_name, import_name=None):
    """檢查套件是否已安裝"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', '未知')
        print_success(f"{package_name} 已安裝（版本: {version}）")
        return True
    except ImportError:
        print_error(f"{package_name} 未安裝")
        return False

def check_packages():
    """檢查所有必要套件"""
    print_header("檢查必要套件")
    
    packages = [
        ('Flask', 'flask'),
        ('PyYAML', 'yaml'),
        ('Markdown', 'markdown'),
    ]
    
    all_installed = True
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_installed = False
    
    if not all_installed:
        print()
        print_warning("有套件未安裝！")
        print("  請執行以下命令安裝所有套件:")
        print(f"  {Colors.BOLD}pip install -r requirements.txt{Colors.RESET}")
        return False
    
    return True

def check_directory_structure():
    """檢查專案目錄結構"""
    print_header("檢查專案目錄結構")
    
    # 取得專案根目錄
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    required_dirs = [
        'src',
        'tests',
        'config',
        'templates',
        'app',
        'scripts',
    ]
    
    required_files = [
        'run_tests.py',
        'requirements.txt',
        'config/config.yaml',
    ]
    
    all_exist = True
    
    # 檢查目錄
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print_success(f"目錄存在: {dir_name}/")
        else:
            print_error(f"目錄不存在: {dir_name}/")
            all_exist = False
    
    # 檢查檔案
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print_success(f"檔案存在: {file_name}")
        else:
            print_error(f"檔案不存在: {file_name}")
            all_exist = False
    
    return all_exist

def check_virtual_environment():
    """檢查是否在虛擬環境中"""
    print_header("檢查虛擬環境")
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print_success("目前在虛擬環境中執行")
        return True
    else:
        print_warning("目前不在虛擬環境中")
        print("  建議使用虛擬環境以避免套件衝突")
        print("  請參考 INSTALLATION.md 建立虛擬環境")
        return False

def main():
    """主程式"""
    print(f"\n{Colors.BOLD}C++ Lab 測試系統 - Python 環境驗證{Colors.RESET}")
    
    results = []
    
    # 執行各項檢查
    results.append(("Python 版本", check_python_version()))
    results.append(("虛擬環境", check_virtual_environment()))
    results.append(("必要套件", check_packages()))
    results.append(("目錄結構", check_directory_structure()))
    
    # 顯示總結
    print_header("驗證總結")
    
    all_passed = True
    for check_name, passed in results:
        if passed:
            print_success(f"{check_name}: 通過")
        else:
            print_error(f"{check_name}: 失敗")
            all_passed = False
    
    # 根據作業系統決定要顯示的 Python 命令
    python_cmd = "python" if sys.platform == "win32" else "python3"
    
    print()
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 環境設定完成！您可以開始使用測試系統了{Colors.RESET}")
        print()
        print("接下來可以執行:")
        print(f"  {Colors.BOLD}{python_cmd} run_tests.py{Colors.RESET}        # 執行所有測試")
        print(f"  {Colors.BOLD}{python_cmd} run_tests.py --gui{Colors.RESET}  # 啟動網頁介面")
        print()
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ 環境設定尚未完成{Colors.RESET}")
        print()
        print("請解決上述問題後再次執行此腳本驗證")
        print("如需協助，請參考 INSTALLATION.md 或 README_STUDENT.md")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

