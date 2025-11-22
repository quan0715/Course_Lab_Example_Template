#!/usr/bin/env python3
"""
簡化版新增題目腳本
只詢問基本資訊,建立樣板檔案供後續編輯
"""

import os
import sys
import yaml
from pathlib import Path

# 顏色代碼
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def get_input(prompt, default=None):
    """取得使用者輸入"""
    if default:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "
    
    user_input = input(prompt_text).strip()
    return user_input if user_input else default

def create_problem_markdown_template(problem_id, problem_name):
    """建立題目說明樣板"""
    return f"""# {problem_id}: {problem_name}

## 題目描述
TODO: 請在此描述題目內容

## 輸入格式
TODO: 描述輸入格式

## 輸出格式
TODO: 描述輸出格式

## 範例

### 輸入 1
```
TODO: 範例輸入
```

### 輸出 1
```
TODO: 範例輸出
```

## 配分
- 總分: 25 分
- 測資數量: 5 個

## 限制條件
TODO: 如有特殊限制條件請在此說明
- 超時限制: 1 秒
"""

def create_cpp_template(problem_id, problem_name):
    """建立 C++ 程式樣板"""
    return f"""// {problem_id}: {problem_name}
// TODO: 請實作此題目

#include <iostream>
using namespace std;

int main() {{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    // TODO: 在此實作你的程式
    
    return 0;
}}
"""

def main():
    print(f"\n{Colors.BOLD}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'C++ Lab 新增題目工具'.center(50)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*50}{Colors.ENDC}\n")
    
    # 取得基本目錄
    base_dir = Path(__file__).parent.absolute()
    config_file = base_dir / "config" / "config.yaml"
    
    if not config_file.exists():
        print_error(f"找不到配置文件: {config_file}")
        sys.exit(1)
    
    # 載入現有配置
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 顯示現有題目
    existing = sorted(config.get('problems', {}).keys())
    print_info(f"現有題目: {', '.join(existing)}")
    
    # 取得基本資訊
    problem_id = get_input("\n題目代號 (例如: p7, p8)")
    if not problem_id:
        print_error("題目代號不能為空")
        sys.exit(1)
    
    if problem_id in config.get('problems', {}):
        confirm = get_input(f"題目 {problem_id} 已存在,是否覆蓋? (y/N)", "n")
        if confirm.lower() not in ['y', 'yes']:
            print_info("取消操作")
            sys.exit(0)
    
    problem_name = get_input("題目名稱", "新題目")
    points = int(get_input("配分", "25"))
    num_cases = int(get_input("測資數量", "5"))
    timeout = int(get_input("超時限制(秒)", "1"))
    
    # 詢問進階選項
    has_forbidden = get_input("是否有禁止關鍵字? (y/N)", "n").lower() in ['y', 'yes']
    forbidden = []
    if has_forbidden:
        forbidden_input = get_input("禁止的關鍵字 (逗號分隔)", "")
        if forbidden_input:
            forbidden = [k.strip() for k in forbidden_input.split(',')]
    
    has_required = get_input("是否有必須包含的函數? (y/N)", "n").lower() in ['y', 'yes']
    required = []
    if has_required:
        required_input = get_input("必須包含的函數 (逗號分隔)", "")
        if required_input:
            required = [r.strip() for r in required_input.split(',')]
    
    # 確認
    print(f"\n{Colors.BOLD}{'='*50}{Colors.ENDC}")
    print(f"題目代號: {problem_id}")
    print(f"題目名稱: {problem_name}")
    print(f"配分: {points}")
    print(f"測資數量: {num_cases}")
    print(f"超時限制: {timeout} 秒")
    if forbidden:
        print(f"禁止關鍵字: {', '.join(forbidden)}")
    if required:
        print(f"必須包含: {', '.join(required)}")
    
    confirm = get_input(f"\n確定要建立題目 {problem_id}? (Y/n)", "y")
    if confirm.lower() not in ['y', 'yes', '']:
        print_info("取消操作")
        sys.exit(0)
    
    print(f"\n{Colors.BOLD}開始建立檔案...{Colors.ENDC}\n")
    
    # 建立測資目錄
    test_dir = base_dir / "tests" / problem_id
    (test_dir / "inputs").mkdir(parents=True, exist_ok=True)
    (test_dir / "outputs").mkdir(parents=True, exist_ok=True)
    
    # 建立測資檔案
    for i in range(1, num_cases + 1):
        case_num = f"{i:02d}"
        (test_dir / "inputs" / f"{case_num}.in").touch()
        (test_dir / "outputs" / f"{case_num}.out").touch()
    
    print_success(f"建立測資目錄: tests/{problem_id}/ ({num_cases} 個測資)")
    
    # 建立題目說明檔案
    problems_dir = base_dir / "problems"
    problems_dir.mkdir(exist_ok=True)
    
    md_file = problems_dir / f"{problem_id}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(create_problem_markdown_template(problem_id, problem_name))
    
    print_success(f"建立題目說明: problems/{problem_id}.md")
    
    # 建立程式檔案
    src_dir = base_dir / "src"
    src_dir.mkdir(exist_ok=True)
    
    src_file = src_dir / f"{problem_id}.cpp"
    if not src_file.exists() or problem_id in config.get('problems', {}):
        with open(src_file, 'w', encoding='utf-8') as f:
            f.write(create_cpp_template(problem_id, problem_name))
        print_success(f"建立程式檔案: src/{problem_id}.cpp")
    else:
        print_info(f"程式檔案已存在,跳過: src/{problem_id}.cpp")
    
    # 更新 config.yaml
    if 'problems' not in config:
        config['problems'] = {}
    
    problem_config = {
        'name': problem_name,
        'points': points
    }
    
    if timeout != 1:
        problem_config['timeout'] = timeout
    
    if forbidden:
        problem_config['forbidden'] = forbidden
    
    if required:
        problem_config['required'] = required
    
    config['problems'][problem_id] = problem_config
    
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print_success(f"更新配置檔案: config/config.yaml")
    
    # 完成訊息
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}完成! 題目 {problem_id} 已建立{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*50}{Colors.ENDC}\n")
    
    print_info("接下來請:")
    print(f"  1. 編輯 problems/{problem_id}.md 填寫題目描述")
    print(f"  2. 編輯 src/{problem_id}.cpp 實作解答")
    print(f"  3. 在 tests/{problem_id}/inputs/ 和 outputs/ 填入測資")
    print(f"  4. 執行測試: python3 run_tests.py\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}操作已取消{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_error(f"發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
