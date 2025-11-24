# C++ Lab 測試系統 - 維護者指南

專為教學環境設計的 C++ 程式作業自動測試系統。

**目標讀者**: AI Agent、助教、教師、系統維護者

**學生請閱讀**: [`README_STUDENT.md`](README_STUDENT.md)

---

## 📋 目錄

- [系統架構](#系統架構)
- [專案結構](#專案結構)
- [配置檔案](#配置檔案)
- [題目管理](#題目管理)
- [測資管理](#測資管理)
- [評分機制](#評分機制)
- [GitHub Classroom](#github-classroom)
- [疑難排解](#疑難排解)

---

## 系統架構

### 核心組件

```
┌─────────────────────────────────────────────────────┐
│                   run_tests.py                      │
│                    (主程式)                          │
└───────────┬────────────────────────┬────────────────┘
            │                        │
    ┌───────▼────────┐      ┌────────▼──────────┐
    │   CLI 模式      │      │   GUI 模式        │
    │                │      │   (Flask Server)  │
    └───────┬────────┘      └────────┬──────────┘
            │                        │
            └────────┬───────────────┘
                     │
         ┌───────────▼────────────┐
         │     app/ 核心模組      │
         ├────────────────────────┤
         │  • compiler.py         │ → 編譯 C++ 程式
         │  • runner.py           │ → 執行測試並比對輸出
         │  • config.py           │ → 讀取配置檔案
         │  • server.py           │ → 網頁介面伺服器
         │  • utils.py            │ → 工具函數
         └────────────────────────┘
                     │
         ┌───────────▼────────────┐
         │   資料來源              │
         ├────────────────────────┤
         │                        │
         │  config/config.yaml    │ ← 系統配置
         │  tests/*/inputs/       │ ← 測試輸入
         │  tests/*/outputs/      │ ← 預期輸出
         │  src/*.cpp             │ ← 學生程式碼
         │                        │
         └────────────────────────┘
                     │
         ┌───────────▼────────────┐
         │   輸出結果              │
         ├────────────────────────┤
         │                        │
         │  build/*.score         │ ← 評分結果
         │  build/*.cases         │ ← 測試案例統計
         │  build/*.compile.log   │ ← 編譯記錄
         │  build/*.run.log       │ ← 執行記錄
         │                        │
         └────────────────────────┘
```

### 運作流程

```
1. 讀取配置
   ↓ config.py 讀取 config/config.yaml
   
2. 掃描題目
   ↓ 根據 config.yaml 中的題目列表
   
3. 編譯程式
   ↓ compiler.py: g++ -std=c++17 -O2 src/pX.cpp -o build/pX
   
4. 執行測試
   ↓ runner.py: 遍歷 tests/pX/inputs/*.in
   ↓          : 執行並捕獲輸出
   ↓          : 與 tests/pX/outputs/*.out 比對
   
5. 計算分數
   ↓ 根據通過的測試案例數量計分
   
6. 產生報告
   ↓ 寫入 build/pX.score, build/pX.cases, build/pX.run.log
```

---

## 專案結構

```
Course_Lab_Example_Template/
│
├── src/                         ← 學生程式碼
│   ├── p1.cpp
│   ├── p2.cpp
│   └── ...
│
├── tests/                       ← 測試資料
│   ├── p1/
│   │   ├── inputs/              ← 測試輸入
│   │   │   ├── 01.in
│   │   │   ├── 02.in
│   │   │   └── ...
│   │   └── outputs/             ← 預期輸出
│   │       ├── 01.out
│   │       ├── 02.out
│   │       └── ...
│   └── p2/
│       └── ...
│
├── problems/                    ← 題目說明文件
│   ├── p1.md
│   ├── p2.md
│   └── ...
│
├── config/                      ← 配置檔案
│   └── config.yaml              ← 系統主配置
│
├── app/                         ← 系統核心模組
│   ├── __init__.py
│   ├── compiler.py              ← 編譯模組
│   ├── runner.py                ← 執行與測試模組
│   ├── server.py                ← 網頁介面伺服器
│   ├── config.py                ← 配置讀取
│   └── utils.py                 ← 工具函數
│
├── templates/                   ← 網頁介面模板 (Jinja2)
│   ├── index.html
│   ├── problem.html
│   └── ...
│
├── static/                      ← 靜態資源
│   └── style.css
│
├── scripts/                     ← 輔助腳本
│   ├── setup_env.sh             ← 環境設定 (macOS/Linux)
│   ├── setup_env.bat            ← 環境設定 (Windows)
│   └── verify_python_setup.py   ← 環境驗證
│
├── build/                       ← 編譯產物與測試結果 (自動產生)
│   ├── p1                       ← 編譯後的執行檔
│   ├── p1.score                 ← 評分結果
│   ├── p1.cases                 ← 測試案例統計
│   ├── p1.compile.log           ← 編譯記錄
│   ├── p1.run.log               ← 執行記錄
│   └── ...
│
├── .github/workflows/           ← GitHub Actions 自動評分
│   └── classroom.yml
│
├── run_tests.py                 ← 主程式
├── add_problem.py               ← 新增題目工具
├── requirements.txt             ← Python 依賴套件
├── README.md                    ← 本文件 (維護者)
├── README_STUDENT.md            ← 學生使用指南
└── INSTALLATION.md              ← 環境安裝指南
```

### 檔案權限說明

| 目錄/檔案            | 學生      | TA/維護者 | 用途           |
| -------------------- | --------- | --------- | -------------- |
| `src/*.cpp`          | ✅ 可修改 | ✅ 可修改 | 學生程式碼     |
| `tests/*/`           | 👁️ 唯讀   | ✅ 可修改 | 測試資料       |
| `problems/*.md`      | 👁️ 唯讀   | ✅ 可修改 | 題目說明       |
| `config/config.yaml` | ❌ 禁止   | ✅ 可修改 | 系統配置       |
| `app/`, `templates/` | ❌ 禁止   | ⚠️ 謹慎   | 系統核心       |
| `build/`             | 👁️ 可查看 | 👁️ 可查看 | 自動產生的結果 |

---

## config.yaml

系統的所有配置都在 `config/config.yaml` 檔案中。

**完整配置說明請參考**: **[CONFIG.md](CONFIG.md)**

### 快速參考

**基本結構**：
```yaml
app:
  title: "C++ Lab 測試系統"
  description: "程式設計作業自動測試系統"

compiler:
  timeout: 10
  flags: "-std=c++17 -O2"

runner:
  timeout: 5

problems:
  p1:
    name: "題目名稱"
    points: 25
    timeout: 1          # 可選
    forbidden: []       # 可選
    required: []        # 可選
    cases: {}           # 可選
```

### 常用配置範例

**基本題目**：
```yaml
problems:
  p1:
    name: "Simple Sum"
    points: 25
```

**禁止迴圈，強制遞迴**：
```yaml
problems:
  p3:
    name: "Recursion Only"
    points: 25
    forbidden: ["for", "while", "do"]
    required: ["factorial"]
```

**個別測資配分**：
```yaml
problems:
  p4:
    name: "Weighted Tests"
    points: 50
    cases:
      "01": 10
      "02": 15
      "03": 25
```

> 📖 **詳細說明、所有選項、FAQ 請參考 [CONFIG.md](CONFIG.md)**


---

## 題目管理

### 新增題目

#### 方法 1：使用自動化腳本（推薦）

```bash
python3 add_problem.py
```

腳本會提示輸入：
1. 題目代號（如 `p7`）
2. 題目名稱
3. 配分（預設 25）
4. 測資數量（預設 5）
5. 超時限制（預設 1 秒）
6. 禁止關鍵字（可選）
7. 必須函數（可選）

**自動建立的檔案**：
- `tests/{problem_id}/inputs/*.in` - 測資輸入（空白範本）
- `tests/{problem_id}/outputs/*.out` - 測資輸出（空白範本）
- `problems/{problem_id}.md` - 題目說明
- `src/{problem_id}.cpp` - C++ 程式樣板
- 更新 `config/config.yaml`

#### 方法 2：手動建立

**步驟 1：建立目錄結構**
```bash
mkdir -p tests/p7/inputs tests/p7/outputs
```

**步驟 2：建立測資檔案**
```bash
# 建立測資（不要建立空檔案！）
echo "10 20" > tests/p7/inputs/01.in
echo "30" > tests/p7/outputs/01.out
```

**步驟 3：建立題目說明** `problems/p7.md`
```markdown
# p7: 題目名稱

## 題目描述
...

## 輸入格式
...

## 輸出格式
...

## 範例
...
```

**步驟 4：建立程式範本** `src/p7.cpp`
```cpp
#include <iostream>
using namespace std;

int main() {
    // 實作程式
    return 0;
}
```

**步驟 5：更新配置** `config/config.yaml`
```yaml
problems:
  p7:
    name: "題目名稱"
    points: 25
```

**步驟 6：驗證**
```bash
python3 run_tests.py p7
```

### 修改題目

| 修改內容     | 編輯檔案                   | 說明                   |
| ------------ | -------------------------- | ---------------------- |
| 題目說明     | `problems/pX.md`           | Markdown 格式          |
| 測試輸入     | `tests/pX/inputs/*.in`     | 純文字檔案             |
| 預期輸出     | `tests/pX/outputs/*.out`   | 純文字檔案             |
| 題目名稱     | `config/config.yaml`       | 修改 `name` 欄位       |
| 配分         | `config/config.yaml`       | 修改 `points` 欄位     |
| 超時限制     | `config/config.yaml`       | 修改 `timeout` 欄位    |
| 禁止關鍵字   | `config/config.yaml`       | 修改 `forbidden` 列表  |
| 必須函數     | `config/config.yaml`       | 修改 `required` 列表   |
| 個別測資配分 | `config/config.yaml`       | 修改 `cases` 字典      |

**修改後記得驗證**：
```bash
python3 run_tests.py pX
```

### 刪除題目

**完整刪除步驟**：
```bash
# 1. 刪除測資目錄
rm -rf tests/p7

# 2. 刪除題目說明
rm problems/p7.md

# 3. 刪除程式檔案
rm src/p7.cpp

# 4. 清理建置產物
rm -f build/p7*

# 5. 手動編輯 config/config.yaml
# 移除 p7 的配置區塊
```

---

## 測資管理

### 測資檔案要求

#### ❌ 禁止事項
- **不要建立空的測資檔案** - 系統會跳過空檔案
- **不要使用不一致的檔名** - `01.in` 必須對應 `01.out`

#### ✅ 必要條件
1. 每個 `.in` 檔案必須有對應的 `.out` 檔案
2. 測資檔案必須有實際內容（不能為空）
3. 檔名格式建議：`01.in`, `02.in`, ... 或 `basic.in`, `edge.in`, ...

#### 檔名格式建議
- **推薦**：兩位數字 `01.in`, `02.in`, ..., `10.in`
- **也可**：描述性名稱 `basic.in`, `edge_case.in`, `large_input.in`
- **排序**：系統按檔名字母順序執行測試

### 測資設計原則

建議涵蓋以下類型：

1. **基本案例** - 題目範例中的簡單輸入
2. **邊界案例** - 最小值、最大值、空輸入
3. **特殊案例** - 零、負數、重複值
4. **壓力測試** - 大量資料、極限情況
5. **錯誤案例** - 不合法輸入（如果需要處理）

### 測資範例

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

### 新增/修改測資

```bash
# 新增測資
echo "測試輸入" > tests/p7/inputs/06.in
echo "預期輸出" > tests/p7/outputs/06.out

# 驗證測資
python3 run_tests.py p7
```

---

## 評分機制

### 全有全無制（預設）

- **所有測資都通過** → 獲得該題滿分
- **任何一個測資失敗** → 該題 0 分

**範例**：
假設 p1 有 5 個測資，配 25 分

| 通過測資 | 得分  |
| -------- | ----- |
| 5/5 ✅   | 25 分 |
| 4/5 ❌   | 0 分  |
| 0/5 ❌   | 0 分  |

### 個別測資配分（可選）

在 `config.yaml` 中設定 `cases`：

```yaml
problems:
  p6:
    points: 50
    cases:
      "01": 10  # 測資 01 通過得 10 分
      "02": 10  # 測資 02 通過得 10 分
      "03": 15  # 測資 03 通過得 15 分
      "04": 15  # 測資 04 通過得 15 分
```

此時採用**部分計分**：
- 測資 01 通過 → +10 分
- 測資 02 通過 → +10 分
- 測資 03 失敗 → +0 分
- 測資 04 通過 → +15 分
- **總分 = 35 分**

### 結果檔案

系統會產生以下檔案在 `build/` 目錄：

| 檔案                | 格式                 | 範例       | 說明           |
| ------------------- | -------------------- | ---------- | -------------- |
| `pX.score`          | `獲得分數 總分`      | `25 25`    | 評分結果       |
| `pX.cases`          | `通過數 總測試數`    | `4 5`      | 測試案例統計   |
| `pX.compile.log`    | 純文字               | -          | 編譯記錄       |
| `pX.run.log`        | 純文字               | -          | 執行記錄       |

---

## GitHub Classroom

### 自動評分流程

當學生 push 程式碼到 GitHub：

```
1. 觸發 GitHub Actions (.github/workflows/classroom.yml)
   ↓
2. 設定環境（Ubuntu + Python + g++）
   ↓
3. 安裝依賴（pip install -r requirements.txt）
   ↓
4. 執行測試（python run_tests.py）
   ↓
5. 收集結果（讀取 build/*.score）
   ↓
6. 產生報告（顯示在 Actions Summary）
   ↓
7. 判定通過（所有測試通過 = workflow 成功）
```

### Workflow 配置

檔案位置：`.github/workflows/classroom.yml`

**主要組成**：
- **環境設定**：Ubuntu Latest + Python 3.11 + g++
- **測試執行**：`python run_tests.py`
- **分數計算**：讀取 `build/*.score` 並計算總分
- **報告產生**：顯示在 GitHub Actions Summary
- **Artifacts**：上傳測試結果和日誌（保留 30 天）

### 查看學生成績

**方法 1：GitHub Classroom 儀表板**
1. 進入 Classroom
2. 點擊 Assignment
3. 查看學生列表和提交狀態

**方法 2：學生 Repository 的 Actions**
1. 進入學生的 repository
2. 點擊 **Actions** 標籤
3. 查看最新的 workflow run
4. 在 Summary 查看分數統計

---

## 疑難排解

### 測試系統找不到題目

**檢查清單**：
- [ ] `src/{problem_id}.cpp` 是否存在
- [ ] `tests/{problem_id}/inputs/` 和 `outputs/` 是否存在
- [ ] `config/config.yaml` 是否包含該題目配置
- [ ] 測資檔案是否為空

**解決方法**：
```bash
# 檢查檔案
ls -la src/p7.cpp
ls -la tests/p7/

# 檢查配置
grep "p7:" config/config.yaml
```

### 測資無法通過但程式看起來正確

**可能原因**：
- 輸出格式不符（多餘空格、換行）
- 換行符號問題（CRLF vs LF）

**解決方法**：
```bash
# 使用網頁介面查看差異
python3 run_tests.py --gui

# 手動比對
./build/p7 < tests/p7/inputs/01.in > tmp.out
diff -u tests/p7/outputs/01.out tmp.out
```

### 編譯失敗

**解決方法**：
```bash
# 查看編譯錯誤
cat build/p7.compile.log

# 手動編譯測試
g++ -std=c++17 -o test src/p7.cpp
```

### 程式執行超時

**可能原因**：
- 無窮迴圈
- 演算法效率太低

**解決方法**：
調整 `config/config.yaml` 中的 timeout：
```yaml
problems:
  p7:
    timeout: 5  # 增加到 5 秒
```

---

## 常用指令

```bash
# 環境管理
source venv/bin/activate              # 啟動虛擬環境 (macOS/Linux)
venv\Scripts\activate                 # 啟動虛擬環境 (Windows)

# 測試執行
python3 run_tests.py                  # 測試所有題目
python3 run_tests.py p1               # 測試單一題目
python3 run_tests.py --gui            # 啟動網頁介面

# 題目管理
python3 add_problem.py                # 新增題目（互動式）

# 環境驗證
python3 scripts/verify_python_setup.py

# 清理
rm -rf build/*                        # 清理所有建置產物
```

---

## 相關文件

- **[README_STUDENT.md](README_STUDENT.md)** - 學生使用指南
- **[INSTALLATION.md](INSTALLATION.md)** - 環境安裝詳細步驟

---

**維護建議**：
- 定期備份 `tests/`、`config/`、`problems/` 目錄
- 使用版本控制（Git）追蹤所有變更
- 測資設計要涵蓋各種邊界情況

**最後更新**: 2024 年 11 月
