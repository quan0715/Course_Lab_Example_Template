# C++ Lab 測試系統 - AI/TA 維護指南

這是一個專為教學環境設計的 C++ 程式作業測試系統。本文件提供完整的題目管理、系統維護和 AI 操作指南。

**本文件適合**: AI Agent、助教、教師、系統維護者

**學生請閱讀**: [`README_STUDENT.md`](README_STUDENT.md)

---

## 📋 目錄

- [系統概述](#系統概述)
- [快速開始](#快速開始)
- [題目管理](#題目管理)
  - [建立新題目](#建立新題目)
  - [修改現有題目](#修改現有題目)
  - [刪除題目](#刪除題目)
- [測資管理](#測資管理)
- [配置系統](#配置系統)
- [評分機制](#評分機制)
- [檔案結構](#檔案結構)
- [系統維護](#系統維護)
- [疑難排解](#疑難排解)

---

## 系統概述

### 主要特色

- ✅ **自動化測試**: 自動編譯、執行、比對輸出
- ✅ **靈活配置**: 支援超時設定、禁用關鍵字、必要函數檢查
- ✅ **網頁介面**: 友善的圖形化測試介面
- ✅ **跨平台**: Windows、macOS、Linux
- ✅ **詳細報告**: 編譯錯誤、執行結果、差異比對

### 系統運作流程

```
1. 學生撰寫程式 (src/pX.cpp)
   ↓
2. 執行測試系統 (python3 run_tests.py)
   ↓
3. 系統編譯程式 (g++ -std=c++17)
   ↓
4. 執行所有測試案例 (tests/pX/inputs/*.in)
   ↓
5. 比對輸出 (與 tests/pX/outputs/*.out 比對)
   ↓
6. 產生結果報告 (build/pX.score, build/pX.run.log)
```

---

## 快速開始

### 環境需求

- **Python 3.7+**
- **C++ 編譯器** (g++, clang++, 或 MSVC)
- **Python 套件**: Flask, PyYAML, markdown (見 `requirements.txt`)

### 初次設定

```bash
# 1. 建立虛擬環境
python3 -m venv venv

# 2. 啟動虛擬環境
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 驗證環境
python3 scripts/verify_python_setup.py
```

### 基本操作

```bash
# 測試所有題目
python3 run_tests.py

# 測試特定題目
python3 run_tests.py p1

# 啟動網頁介面
python3 run_tests.py --gui
```

系統會在 `http://localhost:8080` 啟動網頁伺服器。

---

## 題目管理

### 建立新題目

#### 方法 1：使用自動化腳本（強烈推薦）

```bash
python3 add_problem.py
```

**腳本會引導您完成**：

1. 輸入題目代號（例如：`p7`、`p8`）
2. 輸入題目名稱
3. 設定配分（預設 25 分）
4. 設定測資數量（預設 5 個）
5. 設定超時限制（預設 1 秒）
6. 選擇性設定禁止關鍵字（如：`for`、`while`）
7. 選擇性設定必須包含的函數（如：`recursion`）

**腳本自動建立的檔案**：

- `tests/{problem_id}/inputs/*.in` - 測資輸入檔案（含空白範本）
- `tests/{problem_id}/outputs/*.out` - 測資輸出檔案（含空白範本）
- `problems/{problem_id}.md` - 題目說明文件
- `src/{problem_id}.cpp` - C++ 程式樣板
- 更新 `config/config.yaml` - 自動加入題目配置

**範例：建立遞迴題目**

```bash
python3 add_problem.py

# 輸入：
題目代號: p8
題目名稱: Fibonacci (Recursion)
配分: 25
測資數量: 5
超時限制: 1
是否有禁止關鍵字 (y/n): y
禁止的關鍵字（逗號分隔）: for,while,do
是否有必須包含的函數 (y/n): y
必須包含的函數（逗號分隔）: fibonacci
```

#### 方法 2：手動建立

如果需要更細緻的控制，可以手動建立：

**步驟 1：建立目錄結構**

```bash
mkdir -p tests/p7/inputs
mkdir -p tests/p7/outputs
```

**步驟 2：建立測資檔案**

```bash
# 建立 5 個測資
touch tests/p7/inputs/{01,02,03,04,05}.in
touch tests/p7/outputs/{01,02,03,04,05}.out
```

**重要注意事項**：

- ❌ **不要建立空的測資檔案** - 系統會跳過空檔案
- ✅ 每個 `.in` 檔案必須有對應的 `.out` 檔案
- ✅ 檔名必須完全一致（`01.in` ↔ `01.out`）

**步驟 3：建立題目說明** (`problems/p7.md`)

````markdown
# p7: 題目名稱

## 題目描述

描述題目內容、背景、要求...

## 輸入格式

- 第一行：...
- 第二行：...

## 輸出格式

- 輸出...

## 範例

### 輸入 1

\```
10 20
\```

### 輸出 1

\```
30
\```

## 限制

- 時間限制：1 秒
- 記憶體限制：256 MB
````

**步驟 4：建立程式範本** (`src/p7.cpp`)

```cpp
// p7: 題目名稱
#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 實作程式

    return 0;
}
```

**步驟 5：更新配置** (`config/config.yaml`)

```yaml
problems:
  p7:
    name: "題目名稱"
    points: 25
    timeout: 1 # 可選，預設為 1 秒
```

---

### 修改現有題目

#### 修改題目說明

編輯 `problems/{problem_id}.md` 檔案，更新題目描述、輸入輸出格式等。

#### 新增測資

```bash
# 新增第 6 個測資
echo "測試輸入內容" > tests/p7/inputs/06.in
echo "預期輸出內容" > tests/p7/outputs/06.out

# 驗證測資
python3 run_tests.py p7
```

#### 修改測資

直接編輯測資檔案：

- `tests/{problem_id}/inputs/*.in` - 輸入檔案
- `tests/{problem_id}/outputs/*.out` - 輸出檔案

**提示**：使用網頁介面 (`python3 run_tests.py --gui`) 可以即時查看測試結果和差異。

#### 刪除測資

```bash
# 刪除測資時，輸入和輸出都要刪除
rm tests/p7/inputs/06.in
rm tests/p7/outputs/06.out
```

#### 修改題目配置

編輯 `config/config.yaml`：

```yaml
problems:
  p7:
    name: "新的題目名稱" # 修改題目名稱
    points: 30 # 修改配分
    timeout: 2 # 修改超時限制（秒）
    forbidden: # 禁止使用的關鍵字
      - for
      - while
    required: # 必須包含的函數
      - myFunction
    cases: # 個別測資配分（可選）
      "01": 10
      "02": 10
      "03": 10
```

**配置選項完整說明**：

| 選項        | 類型 | 說明                             | 預設值   |
| ----------- | ---- | -------------------------------- | -------- |
| `name`      | 字串 | 題目名稱（顯示在網頁介面）       | 必填     |
| `points`    | 整數 | 題目總分                         | 100      |
| `timeout`   | 整數 | 執行超時限制（秒）               | 1        |
| `forbidden` | 列表 | 禁止使用的關鍵字                 | 無       |
| `required`  | 列表 | 必須包含的函數名稱               | 無       |
| `cases`     | 字典 | 個別測資配分（不平均分配時使用） | 平均分配 |

---

### 刪除題目

#### 完整刪除步驟

```bash
# 1. 刪除測資目錄
rm -rf tests/p7

# 2. 刪除題目說明
rm problems/p7.md

# 3. 刪除程式檔案
rm src/p7.cpp
# 或如果使用帶名稱的檔案
rm src/p7_*.cpp

# 4. 清理建置產物（可選）
rm -f build/p7*

# 5. 從配置檔案移除
# 手動編輯 config/config.yaml，刪除 p7 的配置
```

#### 快速刪除腳本

可以建立 `scripts/remove_problem.sh`：

```bash
#!/bin/bash
PROBLEM_ID=$1

if [ -z "$PROBLEM_ID" ]; then
    echo "用法: bash scripts/remove_problem.sh p7"
    exit 1
fi

echo "刪除題目: $PROBLEM_ID"
rm -rf tests/$PROBLEM_ID
rm -f problems/$PROBLEM_ID.md
rm -f src/$PROBLEM_ID.cpp
rm -f src/${PROBLEM_ID}_*.cpp
rm -f build/$PROBLEM_ID*

echo "✓ 已刪除檔案"
echo "⚠ 請手動編輯 config/config.yaml 移除題目配置"
```

使用方式：

```bash
chmod +x scripts/remove_problem.sh
bash scripts/remove_problem.sh p7
```

---

## 測資管理

### 測資檔案要求

#### 必要條件

1. **不要建立空的測資檔案**

   - ❌ 空的 `.in` 或 `.out` 檔案會被系統跳過
   - ✅ 確保每個測資檔案都有實際內容

2. **檔名必須對應**

   - 每個 `.in` 檔案必須有對應的 `.out` 檔案
   - 檔名必須完全一致：`01.in` ↔ `01.out`

3. **檔名格式建議**

   - **推薦**：使用兩位數字 `01.in`, `02.in`, ..., `10.in`
   - 也可使用描述性名稱：`basic.in`, `edge_case.in`, `large.in`
   - 系統會按檔名字母順序執行測試

4. **換行符號**
   - Linux/macOS: 使用 LF (`\n`)
   - Windows: 系統會自動處理 CRLF/LF 差異

### 測資設計原則

#### 涵蓋測試案例類型

1. **基本案例** - 題目範例中的簡單輸入
2. **邊界案例** - 最小值、最大值、空輸入
3. **特殊案例** - 零、負數、重複值
4. **壓力測試** - 大量資料、極限情況
5. **錯誤案例** - 不合法輸入（如果需要處理）

#### 測資範例

**題目**：計算兩數之和

```
tests/p1/
├── inputs/
│   ├── 01.in   # 基本案例：正整數
│   ├── 02.in   # 邊界案例：零
│   ├── 03.in   # 特殊案例：負數
│   ├── 04.in   # 壓力測試：大數
│   └── 05.in   # 混合案例
└── outputs/
    ├── 01.out
    ├── 02.out
    ├── 03.out
    ├── 04.out
    └── 05.out
```

**01.in**:

```
10 20
```

**01.out**:

```
30
```

### 測資驗證

建立或修改測資後，務必執行測試驗證：

```bash
# 測試單一題目
python3 run_tests.py p7

# 使用網頁介面查看詳細結果
python3 run_tests.py --gui
```

---

## 配置系統

### 主配置檔案 (`config/config.yaml`)

```yaml
# 系統設定
app:
  title: "C++ Lab 測試系統" # 網頁介面標題
  description: "程式設計作業自動測試系統" # 網頁介面描述

# 編譯器設定
compiler:
  timeout: 10 # 編譯超時（秒）
  flags: "-std=c++17 -O2" # 編譯選項

# 執行器設定
runner:
  timeout: 5 # 執行超時（秒，全域預設）
  memory_limit: 256 # 記憶體限制（MB，目前未實作）

# 測試設定
test:
  stop_on_first_fail: false # 是否在第一個失敗就停止

# 題目設定
problems:
  p1:
    name: "Sum Sum"
    points: 25
    timeout: 1 # 覆蓋全域 timeout

  p2:
    name: "Array Operations"
    points: 25
    timeout: 2

  p3:
    name: "String Manipulation"
    points: 25

  p4:
    name: "Sorting Algorithm"
    points: 25
    forbidden: # 禁止關鍵字
      - "sort"
      - "stable_sort"

  p5:
    name: "Recursion Practice"
    points: 25
    forbidden:
      - "for"
      - "while"
      - "do"
    required: # 必須包含的函數
      - "factorial"

  p6:
    name: "Complex Problem"
    points: 50 # 較高配分
    timeout: 5 # 較長執行時間
    cases: # 個別測資配分
      "01": 10
      "02": 10
      "03": 15
      "04": 15
```

### 配置選項詳解

#### 全域設定

- **`app.title`**: 網頁介面顯示的標題
- **`app.description`**: 網頁介面的描述文字
- **`compiler.timeout`**: 編譯階段的超時限制（秒）
- **`compiler.flags`**: 傳給 g++ 的編譯選項
- **`runner.timeout`**: 程式執行的預設超時限制（秒）
- **`test.stop_on_first_fail`**: 是否在第一個測試失敗時停止

#### 題目設定

每個題目可以有以下設定：

**必要設定**：

- `name`: 題目名稱（字串）
- `points`: 題目配分（整數）

**可選設定**：

- `timeout`: 執行超時（秒），覆蓋全域設定
- `forbidden`: 禁止使用的關鍵字列表
- `required`: 必須包含的函數名稱列表
- `cases`: 個別測資配分（字典，key 為測資檔名去掉副檔名）

#### 進階：個別測資配分

預設情況下，題目總分會平均分配到所有測資。如果需要不平均分配：

```yaml
problems:
  p6:
    name: "Complex Problem"
    points: 50
    cases:
      "01": 5 # 簡單案例，5分
      "02": 5 # 簡單案例，5分
      "03": 10 # 中等案例，10分
      "04": 15 # 困難案例，15分
      "05": 15 # 困難案例，15分
    # 總計：50 分
```

---

## 評分機制

### 評分規則

#### 全有全無制（預設）

- 題目的**所有測資**都通過 → 獲得該題滿分
- 任何一個測資失敗 → 該題 0 分

#### 範例

假設 p1 有 5 個測資，配 25 分：

| 通過測資 | 得分  | 說明       |
| -------- | ----- | ---------- |
| 5/5 ✅   | 25 分 | 全部通過   |
| 4/5 ❌   | 0 分  | 有一個失敗 |
| 0/5 ❌   | 0 分  | 全部失敗   |

### 個別測資配分（可選）

如果在 `config.yaml` 中設定了 `cases`，則採用個別配分：

```yaml
problems:
  p6:
    points: 50
    cases:
      "01": 10
      "02": 10
      "03": 15
      "04": 15
```

此時：

- 測資 01 通過 → 得 10 分
- 測資 02 通過 → 得 10 分
- 測資 03 通過 → 得 15 分
- 測資 04 通過 → 得 15 分
- **總分 = 各測資得分總和**

### 結果檔案

#### `build/pX.cases` - 測試案例統計

```
格式: 通過數 總測試數
範例: 4 5
```

#### `build/pX.score` - 評分結果

```
格式: 獲得分數 總分
範例: 25 25
```

---

## 檔案結構

### 完整目錄結構

```
input-output-test-module/
├── src/                          # 【學生可修改】程式碼目錄
│   ├── p1.cpp                    # 題目 1 的程式
│   ├── p2.cpp                    # 題目 2 的程式
│   └── ...
│
├── tests/                        # 【維護者管理】測試案例目錄
│   ├── p1/
│   │   ├── inputs/               # 輸入測資
│   │   │   ├── 01.in
│   │   │   ├── 02.in
│   │   │   └── ...
│   │   └── outputs/              # 預期輸出
│   │       ├── 01.out
│   │       ├── 02.out
│   │       └── ...
│   └── ...
│
├── problems/                     # 【維護者管理】題目說明
│   ├── p1.md
│   ├── p2.md
│   └── ...
│
├── config/                       # 【維護者管理】配置檔案
│   └── config.yaml               # 系統主配置
│
├── app/                          # 【系統核心】程式模組
│   ├── compiler.py               # 編譯模組
│   ├── runner.py                 # 執行與測試模組
│   ├── server.py                 # 網頁介面伺服器
│   ├── config.py                 # 配置讀取
│   └── utils.py                  # 工具函數
│
├── templates/                    # 【系統核心】網頁介面模板
├── static/                       # 【系統核心】靜態資源
│
├── scripts/                      # 【輔助工具】腳本
│   ├── setup_env.sh              # 環境設定（macOS/Linux）
│   ├── setup_env.bat             # 環境設定（Windows）
│   ├── verify_python_setup.py   # 環境驗證
│   └── run_tests.sh/bat          # 測試腳本
│
├── build/                        # 【自動產生】編譯產物與測試結果
│   ├── p1                        # 編譯後的執行檔
│   ├── p1.cases                  # 測試案例統計
│   ├── p1.score                  # 評分結果
│   ├── p1.compile.log            # 編譯記錄
│   └── p1.run.log                # 執行記錄
│
├── run_tests.py                  # 【主程式】測試系統入口
├── add_problem.py                # 【輔助工具】新增題目
├── requirements.txt              # Python 依賴套件
├── README.md                     # 本文件（維護者/AI）
├── README_STUDENT.md             # 學生使用文件
└── INSTALLATION.md               # 環境安裝指南
```

### 檔案權限說明

| 目錄/檔案            | 學生      | TA/AI     | 說明       |
| -------------------- | --------- | --------- | ---------- |
| `src/*.cpp`          | ✅ 可修改 | ✅ 可修改 | 學生程式碼 |
| `tests/*/`           | ❌ 唯讀   | ✅ 可修改 | 測試案例   |
| `problems/*.md`      | ❌ 唯讀   | ✅ 可修改 | 題目說明   |
| `config/config.yaml` | ❌ 唯讀   | ✅ 可修改 | 系統配置   |
| `app/`, `templates/` | ❌ 禁止   | ⚠️ 謹慎   | 系統核心   |
| `build/`             | 👁️ 可查看 | 👁️ 可查看 | 自動產生   |

---

## 系統維護

### 日常維護任務

#### 1. 環境更新

```bash
# 啟動虛擬環境
source venv/bin/activate

# 更新套件
pip install --upgrade -r requirements.txt

# 驗證環境
python3 scripts/verify_python_setup.py
```

#### 2. 清理建置產物

```bash
# 清理所有建置檔案
rm -rf build/*

# 清理特定題目
rm -f build/p7*
```

#### 3. 批次測試

```bash
# 測試所有題目
python3 run_tests.py

# 生成測試報告
python3 run_tests.py > test_report.txt
```

#### 4. 備份重要檔案

建議定期備份：

- `tests/` - 測試案例
- `config/` - 配置檔案
- `problems/` - 題目說明

```bash
# 備份範例
tar -czf backup_$(date +%Y%m%d).tar.gz tests/ config/ problems/
```

### 批次處理學生作業

假設收集了多個學生的程式碼：

```bash
#!/bin/bash
# batch_test.sh

for student_dir in submissions/*/; do
    student=$(basename "$student_dir")
    echo "Testing $student..."

    # 複製學生的程式碼
    cp "$student_dir"/*.cpp src/

    # 執行測試
    python3 run_tests.py > "results/${student}_result.txt"

    # 備份成績
    cp build/*.score "results/${student}/"
done
```

### 系統升級

當需要修改系統核心功能時：

1. **備份當前狀態**
2. **在測試環境驗證**
3. **更新文件**
4. **通知使用者**

---

## 疑難排解

### 常見問題

#### Q1: 測試系統找不到題目

**可能原因**：

- 檔案不存在或路徑錯誤
- 配置檔案未更新

**檢查清單**：

- [ ] `src/{problem_id}.cpp` 是否存在
- [ ] `tests/{problem_id}/inputs/` 和 `outputs/` 是否存在
- [ ] `config/config.yaml` 是否包含該題目配置

**解決方法**：

```bash
# 檢查檔案
ls -la src/p7.cpp
ls -la tests/p7/

# 檢查配置
grep "p7:" config/config.yaml
```

#### Q2: 測資無法通過但程式看起來正確

**可能原因**：

- 輸出格式不符（多餘空格、換行）
- 換行符號問題（CRLF vs LF）
- 輸出順序錯誤

**解決方法**：

```bash
# 查看詳細差異
python3 run_tests.py p7

# 使用 diff 比對
./build/p7 < tests/p7/inputs/01.in > tmp.out
diff -u tests/p7/outputs/01.out tmp.out

# 檢查換行符號
file tests/p7/outputs/01.out
```

#### Q3: 編譯失敗

**可能原因**：

- C++ 語法錯誤
- 使用了不支援的 C++ 標準
- 缺少標頭檔

**解決方法**：

```bash
# 查看編譯錯誤
cat build/p7.compile.log

# 手動編譯測試
g++ -std=c++17 -o test src/p7.cpp
```

#### Q4: 程式執行超時

**可能原因**：

- 無窮迴圈
- 演算法效率太低
- 等待輸入但沒有輸入資料

**解決方法**：

```bash
# 調整超時設定（config/config.yaml）
problems:
  p7:
    timeout: 5  # 增加到 5 秒

# 手動測試程式
time ./build/p7 < tests/p7/inputs/01.in
```

#### Q5: 禁止關鍵字檢查不生效

**檢查配置**：

```yaml
problems:
  p7:
    forbidden:
      - "for" # 確保格式正確
      - "while"
```

**驗證**：

```bash
# 檢查程式碼是否包含禁止關鍵字
grep -n "for\|while" src/p7.cpp
```

#### Q6: Windows 上的換行符號問題

**問題**：Windows 使用 CRLF，Linux/macOS 使用 LF

**解決方法**：

```bash
# 轉換為 LF（推薦）
dos2unix tests/p7/outputs/*.out

# 或在 Git 中設定自動轉換
git config core.autocrlf true
```

### 除錯技巧

#### 1. 使用網頁介面

```bash
python3 run_tests.py --gui
```

網頁介面提供：

- 視覺化的測試結果
- 逐行差異比對
- 編譯錯誤高亮顯示

#### 2. 查看詳細日誌

```bash
# 查看編譯日誌
cat build/p7.compile.log

# 查看執行日誌
cat build/p7.run.log
```

#### 3. 手動執行測試

```bash
# 編譯
g++ -std=c++17 -o test_p7 src/p7.cpp

# 執行單一測資
./test_p7 < tests/p7/inputs/01.in

# 比對輸出
./test_p7 < tests/p7/inputs/01.in | diff - tests/p7/outputs/01.out
```

---

## GitHub Classroom 設定

本系統整合了 GitHub Classroom 進行作業繳交和自動評分。

### 自動評分流程

當學生 push 程式碼到 GitHub 時：

1. **觸發 GitHub Actions** - `.github/workflows/autograding.yml`
2. **設定環境** - 安裝 Python、C++ 編譯器、依賴套件
3. **執行測試** - 運行 `python run_tests.py`
4. **收集結果** - 讀取 `build/*.score` 檔案
5. **產生報告** - 在 Actions Summary 和 PR 留言顯示結果
6. **判定通過** - 所有測試通過則 workflow 成功

### GitHub Classroom 初始設定

#### 1. 建立 Template Repository

1. 在 GitHub 上建立一個新的 repository
2. 將本專案的所有檔案推送上去：
   ```bash
   git remote add origin https://github.com/您的組織/cpp-lab-template.git
   git branch -M main
   git push -u origin main
   ```
3. 在 repository 設定中，勾選 **"Template repository"**

#### 2. 設定 GitHub Classroom

1. 前往 https://classroom.github.com/
2. 建立新的 Classroom（如果還沒有）
3. 建立新的 Assignment
4. 選擇剛才建立的 template repository
5. 設定：
   - Assignment title: 例如 "C++ Lab Assignment 1"
   - Deadline: 設定截止日期
   - Individual/Group: 選擇 Individual
   - 勾選 "Enable feedback pull requests"

#### 3. 發送邀請連結給學生

從 Classroom 取得邀請連結，發送給學生。學生點擊後會自動建立他們自己的 repository。

### GitHub Actions Workflow 說明

Workflow 檔案位置：`.github/workflows/autograding.yml`

#### 主要步驟

1. **環境設定**：

   - Ubuntu Latest
   - Python 3.11
   - G++ 編譯器

2. **執行測試**：

   - 運行 `python run_tests.py`
   - 儲存輸出到 `test_results.txt`

3. **分數計算**：

   - 讀取所有 `build/*.score` 檔案
   - 計算總分和最高分
   - 產生摘要報告

4. **PR 評論**（如果是 Pull Request）：

   - 在 PR 中自動留言顯示測試結果
   - 表格形式顯示各題得分

5. **上傳報告**：
   - 將測試結果和日誌上傳為 Artifacts
   - 保留 30 天

#### 自訂 Workflow

如果需要修改評分邏輯，編輯 `.github/workflows/autograding.yml`：

```yaml
# 修改 Python 版本
- name: 設定 Python 環境
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # 改為其他版本

# 修改超時時間
jobs:
  test:
    timeout-minutes: 10  # 改為其他時間

# 修改分數計算邏輯
# 在 "收集測試結果" 步驟中修改
```

### 查看學生成績

#### 方法一：在 GitHub Classroom

1. 進入您的 Classroom
2. 點擊 Assignment
3. 查看學生列表和提交狀態
4. 點擊個別學生查看詳細資訊

#### 方法二：在學生的 Repository

1. 進入學生的 repository
2. 點擊 **Actions** 標籤
3. 查看最新的 workflow run
4. 展開 "test" job 查看詳細輸出
5. 在 Summary 頁面查看分數統計

#### 方法三：使用 GitHub API（批次處理）

可以撰寫腳本批次收集所有學生的成績：

```bash
# 範例：使用 GitHub CLI 收集成績
gh api \
  -H "Accept: application/vnd.github+json" \
  /repos/組織/repo/actions/runs \
  | jq '.workflow_runs[0]'
```

### 成績匯出腳本範例

創建 `scripts/export_grades.py`：

```python
#!/usr/bin/env python3
"""
從 GitHub Actions 匯出所有學生的成績
需要安裝: pip install PyGithub
"""

import os
from github import Github

# GitHub Token
token = os.environ.get('GITHUB_TOKEN')
g = Github(token)

org = g.get_organization('您的組織名稱')
repos = org.get_repos()

print("學生,總分,最高分")

for repo in repos:
    if repo.name.startswith('assignment-'):
        # 取得最新的 workflow run
        workflows = repo.get_workflow_runs()
        if workflows.totalCount > 0:
            latest = workflows[0]
            # 讀取 artifacts 或 logs
            # ...
```

### 學生常見問題處理

#### 學生說測試在本地通過但 GitHub 上失敗

**可能原因**：

1. **環境差異**：

   - 本地使用不同的編譯器或版本
   - 路徑或換行符號問題

2. **未推送最新程式碼**：

   - 確認學生是否執行了 `git push`
   - 檢查 commit 時間戳記

3. **修改了不該修改的檔案**：
   - 檢查 git diff
   - 確認只修改了 `src/` 下的檔案

**解決方法**：

```bash
# 請學生提供 GitHub Actions 的完整日誌
# 比對本地和 GitHub 的測試結果
# 確認程式碼版本一致
```

#### Workflow 執行時間過長

如果測試時間超過限制：

1. **調整超時設定**：

   ```yaml
   jobs:
     test:
       timeout-minutes: 20 # 增加到 20 分鐘
   ```

2. **優化測試**：
   - 減少測試案例數量
   - 降低測試資料大小
   - 調整編譯選項

#### Actions 配額用完

GitHub 免費帳號有 Actions 使用時間限制：

1. **監控使用量**：

   - Organization Settings → Billing
   - 查看 Actions 使用時間

2. **優化策略**：
   - 只在 main 分支觸發
   - 限制測試次數
   - 使用 self-hosted runners

### 進階設定

#### 修改網頁伺服器 Port

系統預設使用 **port 8080**（避免與 macOS AirPlay Receiver 的 port 5000 衝突）。

如需修改，編輯 `app/server.py` 的最後一行：

```python
app.run(host='0.0.0.0', port=您的埠號, debug=True)
```

例如改為 port 3000：

```python
app.run(host='0.0.0.0', port=3000, debug=True)
```

#### 自動發送成績通知

可以設定 workflow 在測試完成後發送通知：

```yaml
- name: 發送通知
  if: always()
  uses: actions/github-script@v7
  with:
    script: |
      // 發送 Email 或 Slack 通知
```

#### 防止作弊檢查

添加額外的檢查步驟：

```yaml
- name: 檢查禁用關鍵字
  run: |
    if grep -r "system(" src/; then
      echo "錯誤：禁止使用 system() 函數"
      exit 1
    fi
```

#### 整合 CodeQL 安全掃描

在 `.github/workflows/` 添加 `codeql.yml`：

```yaml
name: CodeQL

on:
  push:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v2
      - uses: github/codeql-action/analyze@v2
```

---

## AI Agent 操作指南

### 當要求建立新題目時

1. **使用自動化腳本**：

   ```bash
   python3 add_problem.py
   ```

2. **填寫完整資訊**：

   - 題目代號（如 p8）
   - 題目名稱
   - 配分
   - 測資數量
   - 超時限制
   - 禁止關鍵字（如果有）
   - 必須函數（如果有）

3. **編輯生成的檔案**：

   - 完善 `problems/pX.md` 的題目說明
   - 填寫 `tests/pX/inputs/*.in` 的測資
   - 填寫 `tests/pX/outputs/*.out` 的預期輸出

4. **驗證測試**：
   ```bash
   python3 run_tests.py pX
   ```

### 當要求修改題目時

1. **識別修改類型**：

   - 題目說明 → 編輯 `problems/pX.md`
   - 測資 → 編輯 `tests/pX/inputs/*.in` 和 `outputs/*.out`
   - 配分/超時 → 編輯 `config/config.yaml`
   - 限制條件 → 編輯 `config/config.yaml` 的 `forbidden` 或 `required`

2. **執行修改**

3. **驗證修改**：
   ```bash
   python3 run_tests.py pX
   ```

### 當要求刪除題目時

1. **確認題目代號**
2. **執行刪除**：
   ```bash
   rm -rf tests/pX
   rm problems/pX.md
   rm src/pX.cpp
   rm -f build/pX*
   ```
3. **更新配置**：手動從 `config/config.yaml` 移除該題目
4. **確認刪除**：
   ```bash
   python3 run_tests.py  # 不應出現 pX
   ```

### 最佳實踐

1. ✅ 優先使用自動化腳本
2. ✅ 每次變更後都執行測試驗證
3. ✅ 測資要涵蓋邊界案例
4. ✅ 題目說明要清晰完整
5. ✅ 適當設定超時限制
6. ❌ 不要建立空的測資檔案
7. ❌ 不要直接修改 `app/` 核心程式碼（除非必要）

---

## 附錄

### 常用指令速查

```bash
# 環境管理
source venv/bin/activate          # 啟動虛擬環境（macOS/Linux）
venv\Scripts\activate              # 啟動虛擬環境（Windows）
deactivate                         # 關閉虛擬環境

# 測試執行
python3 run_tests.py               # 測試所有題目
python3 run_tests.py p1            # 測試單一題目
python3 run_tests.py --gui         # 網頁介面
python3 run_tests.py --help        # 查看說明

# 題目管理
python3 add_problem.py             # 新增題目
bash scripts/remove_problem.sh p7  # 刪除題目（需先建立腳本）

# 環境驗證
python3 scripts/verify_python_setup.py  # 驗證環境設定

# 清理
rm -rf build/*                     # 清理所有建置產物
rm -f build/p7*                    # 清理特定題目
```

### 相關文件

- **[README_STUDENT.md](README_STUDENT.md)** - 學生使用指南
- **[INSTALLATION.md](INSTALLATION.md)** - 環境安裝詳細步驟

---

## 授權與貢獻

本專案為教學用途的模板專案，可自由修改和使用。

**維護建議**：

- 定期備份 `tests/`、`config/`、`problems/` 目錄
- 使用版本控制（Git）追蹤所有變更
- 記錄重要的配置變更

---

**最後更新**: 2024 年 11 月

如有問題或建議，請聯繫系統管理員。
