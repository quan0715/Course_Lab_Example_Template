# Agent 操作指南

本文檔說明如何管理 C++ Lab 測試系統的題目。

## 一、建立新題目

### 方法 1：使用自動化腳本（推薦）

```bash
python3 add_problem.py
```

腳本會引導你完成以下步驟：
1. 輸入題目代號（例如：p7, p8）
2. 輸入題目名稱
3. 設定配分（預設 25 分）
4. 設定測資數量（預設 5 個）
5. 設定超時限制（預設 1 秒）
6. 選擇性設定禁止關鍵字
7. 選擇性設定必須包含的函數

**腳本會自動建立**：
- `tests/{problem_id}/inputs/` - 測資輸入目錄（含空白測資檔案）
- `tests/{problem_id}/outputs/` - 測資輸出目錄（含空白測資檔案）
- `problems/{problem_id}.md` - 題目說明文件
- `src/{problem_id}.cpp` - C++ 程式樣板
- 更新 `config/config.yaml` - 自動加入題目配置

### 方法 2：手動建立

#### 步驟 1：建立測資目錄結構

```bash
mkdir -p tests/p7/inputs
mkdir -p tests/p7/outputs
```

#### 步驟 2：建立測資檔案

在 `tests/p7/inputs/` 建立輸入檔案：
```bash
# 建立 5 個測資
touch tests/p7/inputs/{01,02,03,04,05}.in
```

在 `tests/p7/outputs/` 建立對應的輸出檔案：
```bash
touch tests/p7/outputs/{01,02,03,04,05}.out
```

**重要**：
- 輸入檔名必須以 `.in` 結尾
- 輸出檔名必須與輸入檔名對應（例如：`01.in` 對應 `01.out`）
- **不要建立空的測資檔案**，測試系統會跳過空測資

#### 步驟 3：建立題目說明文件

在 `problems/` 目錄建立 `p7.md`：

```markdown
# p7: 題目名稱

## 題目描述
描述題目內容...

## 輸入格式
描述輸入格式...

## 輸出格式
描述輸出格式...

## 範例
### 輸入 1
\```
範例輸入
\```

### 輸出 1
\```
範例輸出
\```
```

#### 步驟 4：建立程式檔案

在 `src/` 目錄建立 `p7.cpp`：

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

#### 步驟 5：更新配置檔案

編輯 `config/config.yaml`，在 `problems` 區段加入：

```yaml
problems:
  p7:
    name: 題目名稱
    points: 25
    timeout: 1  # 可選，預設為 1 秒
```

---

## 二、修改現有題目

### 修改題目說明

編輯 `problems/{problem_id}.md` 檔案，更新題目描述、輸入輸出格式等。

### 修改測資

#### 新增測資

1. 在 `tests/{problem_id}/inputs/` 新增 `.in` 檔案
2. 在 `tests/{problem_id}/outputs/` 新增對應的 `.out` 檔案
3. **確保測資檔案不是空的**

範例：
```bash
# 新增第 6 個測資
echo "測試輸入" > tests/p7/inputs/06.in
echo "預期輸出" > tests/p7/outputs/06.out
```

#### 修改測資

直接編輯 `tests/{problem_id}/inputs/*.in` 和 `tests/{problem_id}/outputs/*.out` 檔案。

#### 刪除測資

```bash
rm tests/p7/inputs/06.in
rm tests/p7/outputs/06.out
```

### 修改配置

編輯 `config/config.yaml`：

```yaml
problems:
  p7:
    name: 新的題目名稱        # 修改題目名稱
    points: 30                # 修改配分
    timeout: 2                # 修改超時限制（秒）
    forbidden:                # 禁止使用的關鍵字
      - for
      - while
    required:                 # 必須包含的函數
      - myFunction
    cases:                    # 個別測資配分（可選）
      '01': 10
      '02': 10
      '03': 10
```

**配置選項說明**：
- `name`: 題目名稱（顯示在網頁介面）
- `points`: 題目總分
- `timeout`: 執行超時限制（秒），預設為 1
- `forbidden`: 禁止使用的關鍵字列表（可選）
- `required`: 必須包含的函數名稱列表（可選）
- `cases`: 個別測資的配分（可選，用於不平均分配）

---

## 三、刪除題目

### 完整刪除步驟

#### 步驟 1：刪除測資目錄

```bash
rm -rf tests/p7
```

#### 步驟 2：刪除題目說明

```bash
rm problems/p7.md
```

#### 步驟 3：刪除程式檔案

```bash
rm src/p7.cpp
# 或如果使用帶名稱的檔案
rm src/p7_*.cpp
```

#### 步驟 4：從配置檔案移除

編輯 `config/config.yaml`，刪除對應的題目配置：

```yaml
problems:
  # p7:  # 刪除或註解掉整個 p7 區塊
  #   name: Test
  #   points: 25
```

#### 步驟 5：清理建置產物（可選）

```bash
rm -f build/p7*
```

### 快速刪除腳本

可以建立一個刪除腳本 `scripts/remove_problem.sh`：

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
bash scripts/remove_problem.sh p7
```

---

## 四、測資要求與注意事項

### 測資檔案要求

1. **不要建立空的測資檔案**
   - 空的 `.in` 或 `.out` 檔案會被測試系統跳過
   - 確保每個測資檔案都有實際內容

2. **檔名對應**
   - 每個 `.in` 檔案必須有對應的 `.out` 檔案
   - 檔名必須完全一致（例如：`01.in` 對應 `01.out`）

3. **檔名格式**
   - 建議使用兩位數字：`01.in`, `02.in`, ...
   - 也可使用其他命名：`basic.in`, `edge_case.in`, ...

4. **換行符號**
   - Linux/macOS: 使用 LF (`\n`)
   - Windows: 系統會自動處理 CRLF/LF 差異

### 測試驗證

建立或修改測資後，執行測試驗證：

```bash
# 測試單一題目
python3 run_tests.py p7

# 測試所有題目
python3 run_tests.py

# 使用網頁介面測試
python3 run_tests.py --gui
```

---

## 五、常見操作範例

### 範例 1：建立遞迴題目

```bash
python3 add_problem.py
```

輸入：
- 題目代號: `p8`
- 題目名稱: `Fibonacci (Recursion)`
- 配分: `25`
- 測資數量: `5`
- 超時限制: `1`
- 是否有禁止關鍵字: `y`
- 禁止的關鍵字: `for,while,do`
- 是否有必須包含的函數: `y`
- 必須包含的函數: `fibonacci`

### 範例 2：修改題目配分

編輯 `config/config.yaml`：

```yaml
problems:
  p1:
    name: Sum Sum
    points: 30  # 從 25 改為 30
```

### 範例 3：新增測資到現有題目

```bash
# 新增第 6 個測資
echo "10 20" > tests/p1/inputs/06.in
echo "30" > tests/p1/outputs/06.out

# 測試
python3 run_tests.py p1
```

---

## 六、檔案結構總覽

```
.
├── src/
│   └── {problem_id}.cpp          # 程式檔案
├── tests/
│   └── {problem_id}/
│       ├── inputs/
│       │   ├── 01.in
│       │   ├── 02.in
│       │   └── ...
│       └── outputs/
│           ├── 01.out
│           ├── 02.out
│           └── ...
├── problems/
│   └── {problem_id}.md           # 題目說明
├── config/
│   └── config.yaml               # 題目配置
└── build/
    ├── {problem_id}              # 編譯後的執行檔
    ├── {problem_id}.cases        # 測試結果
    └── {problem_id}.score        # 分數記錄
```

---

## 七、疑難排解

### 問題：測試系統找不到題目

**檢查**：
1. `src/{problem_id}.cpp` 是否存在
2. `tests/{problem_id}/inputs/` 和 `outputs/` 是否存在
3. `config/config.yaml` 是否包含該題目配置

### 問題：測資無法通過

**檢查**：
1. 輸出檔案的換行符號是否正確
2. 輸出是否有多餘的空白或換行
3. 使用 `python3 run_tests.py p7` 查看詳細的差異比對

### 問題：編譯失敗

**檢查**：
1. C++ 語法是否正確
2. 查看 `build/{problem_id}.compile.log` 的錯誤訊息
3. 確認使用 C++17 標準

---

## 八、最佳實踐

1. **使用自動化腳本**：優先使用 `add_problem.py` 建立新題目
2. **測資命名**：使用兩位數字命名（01, 02, ...）方便排序
3. **測資驗證**：建立測資後立即測試驗證
4. **文檔完整**：確保 `problems/{problem_id}.md` 有完整的題目說明
5. **版本控制**：使用 Git 追蹤所有變更
6. **定期清理**：刪除不需要的題目和測資
