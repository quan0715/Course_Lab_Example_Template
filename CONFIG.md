# config.yaml 配置文件說明

本文件詳細說明 `config/config.yaml` 的配置選項和使用方式。

**目標讀者**: TA、教師、系統維護者

---

## 📋 目錄

- [檔案位置](#檔案位置)
- [基本結構](#基本結構)
- [全域設定](#全域設定)
- [題目設定](#題目設定)
- [配置範例](#配置範例)
- [常見問題](#常見問題)

---

## 檔案位置

```
config/config.yaml
```

這是系統的**唯一配置檔案**，所有題目、編譯、測試設定都在此檔案中。

---

## 基本結構

```yaml
# 系統全域設定
app:
  title: "C++ Lab 測試系統"
  description: "程式設計作業自動測試系統"

# 編譯器設定
compiler:
  timeout: 10
  flags: "-std=c++17 -O2"

# 執行器設定
runner:
  timeout: 5
  memory_limit: 256

# 測試設定
test:
  stop_on_first_fail: false

# 題目配置
problems:
  p1:
    name: "題目名稱"
    points: 25
    # ... 其他設定
```

---

## 全域設定

### app - 應用程式設定

網頁介面的顯示設定。

| 選項          | 類型 | 必填 | 說明         | 預設值 | 範例                       |
| ------------- | ---- | ---- | ------------ | ------ | -------------------------- |
| `title`       | 字串 | ❌   | 網頁標題     | -      | `"C++ Lab 測試系統"`       |
| `description` | 字串 | ❌   | 網頁描述文字 | -      | `"程式設計作業自動測試系統"` |

**範例**：
```yaml
app:
  title: "資料結構作業測試系統"
  description: "2024 年秋季班程式作業"
```

### compiler - 編譯器設定

控制 C++ 程式的編譯行為。

| 選項      | 類型 | 必填 | 說明                   | 預設值           | 範例                 |
| --------- | ---- | ---- | ---------------------- | ---------------- | -------------------- |
| `timeout` | 整數 | ❌   | 編譯超時（秒）         | 10               | `15`                 |
| `flags`   | 字串 | ❌   | 傳給 g++ 的編譯參數    | `-std=c++17 -O2` | `-std=c++20 -O3 -Wall` |

**範例**：
```yaml
compiler:
  timeout: 15  # 編譯時間較長的專案
  flags: "-std=c++20 -O2 -Wall -Wextra"  # 啟用更多警告
```

**常用編譯參數**：
- `-std=c++17` / `-std=c++20` - C++ 標準版本
- `-O2` / `-O3` - 最佳化等級
- `-Wall` - 啟用所有警告
- `-Wextra` - 啟用額外警告
- `-g` - 產生除錯資訊（通常不用於評分）

### runner - 執行器設定

控制程式執行行為。

| 選項           | 類型 | 必填 | 說明                         | 預設值 | 範例 |
| -------------- | ---- | ---- | ---------------------------- | ------ | ---- |
| `timeout`      | 整數 | ❌   | 預設執行超時（秒）           | 5      | `10` |
| `memory_limit` | 整數 | ❌   | 記憶體限制 MB（目前未實作）  | 256    | `512` |

**範例**：
```yaml
runner:
  timeout: 10      # 允許程式執行較長時間
  memory_limit: 512  # 較大的記憶體限制（未實作）
```

> **💡 提示**：個別題目可以覆蓋全域的 `timeout` 設定

### test - 測試設定

控制測試執行行為。

| 選項                 | 類型 | 必填 | 說明                       | 預設值 | 範例    |
| -------------------- | ---- | ---- | -------------------------- | ------ | ------- |
| `stop_on_first_fail` | 布林 | ❌   | 是否在第一個失敗時停止測試 | false  | `true` |

**範例**：
```yaml
test:
  stop_on_first_fail: false  # 執行所有測試，即使某些失敗
```

---

## 題目設定

每個題目在 `problems` 下有自己的配置區塊。

### 必填欄位

| 選項     | 類型 | 說明     | 範例           |
| -------- | ---- | -------- | -------------- |
| `name`   | 字串 | 題目名稱 | `"Sum Sum"`    |
| `points` | 整數 | 題目總分 | `25`           |

### 可選欄位

| 選項        | 類型     | 說明                                       | 範例                          |
| ----------- | -------- | ------------------------------------------ | ----------------------------- |
| `timeout`   | 整數     | 執行超時（秒），覆蓋全域設定               | `3`                           |
| `forbidden` | 字串列表 | 禁止使用的關鍵字                           | `["for", "while", "do"]`      |
| `required`  | 字串列表 | 程式碼中必須包含的函數名稱                 | `["factorial", "recursion"]`  |
| `cases`     | 字典     | 個別測資配分，key 為測資檔名（去掉副檔名） | `{"01": 10, "02": 15}`        |

### 欄位詳解

#### timeout - 執行超時

指定該題目的執行時間限制（秒）。

**使用時機**：
- 演算法複雜度較高的題目
- 需要處理大量資料的題目
- 遞迴深度較深的題目

**範例**：
```yaml
problems:
  p5:
    name: "大數計算"
    points: 30
    timeout: 5  # 允許 5 秒執行時間
```

#### forbidden - 禁止關鍵字

列出不允許在程式碼中出現的關鍵字。

**使用時機**：
- 要求學生使用特定方法（如遞迴而非迴圈）
- 禁止使用內建函數（如 `sort`）
- 教學特定演算法實作

**範例**：
```yaml
problems:
  p3:
    name: "遞迴練習"
    points: 25
    forbidden:
      - "for"      # 禁止 for 迴圈
      - "while"    # 禁止 while 迴圈
      - "do"       # 禁止 do-while 迴圈
```

#### required - 必須函數

列出程式碼中必須包含的函數名稱。

**使用時機**：
- 要求使用特定函數名稱
- 檢查是否實作必要的函數
- 確保學生遵循指定的程式架構

**範例**：
```yaml
problems:
  p4:
    name: "階乘計算"
    points: 25
    required:
      - "factorial"  # 必須有 factorial 函數
      - "main"       # 必須有 main 函數
```

> **⚠️ 注意**：系統只檢查函數名稱是否出現，不檢查函數簽章或實作細節

#### cases - 個別測資配分

為每個測資指定不同的分數（部分計分制）。

**預設行為**（未設定 cases）：
- 題目總分平均分配到所有測資
- 必須**全部通過**才得分（全有全無制）

**設定 cases 後**：
- 每個測資獨立計分
- 通過幾個測資就得幾分（部分計分制）

**範例**：
```yaml
problems:
  p6:
    name: "複雜問題"
    points: 50
    cases:
      "01": 5   # 簡單案例，5 分
      "02": 10  # 中等案例，10 分
      "03": 15  # 困難案例，15 分
      "04": 20  # 極限案例，20 分
    # 總計：5 + 10 + 15 + 20 = 50 分
```

> **💡 提示**：`cases` 的總和應該等於 `points`

---

## 配置範例

### 範例 1：基本題目

最簡單的配置，只有名稱和分數：

```yaml
problems:
  p1:
    name: "Hello World"
    points: 25
```

### 範例 2：有時間限制的題目

允許較長的執行時間：

```yaml
problems:
  p2:
    name: "大數據處理"
    points: 30
    timeout: 5  # 允許 5 秒
```

### 範例 3：禁止迴圈，強制遞迴

要求學生使用遞迴而非迴圈：

```yaml
problems:
  p3:
    name: "遞迴練習"
    points: 25
    forbidden:
      - "for"
      - "while"
      - "do"
    required:
      - "factorial"
```

### 範例 4：禁用內建排序

要求學生自行實作排序演算法：

```yaml
problems:
  p4:
    name: "排序演算法"
    points: 30
    timeout: 2
    forbidden:
      - "sort"           # 禁止 std::sort
      - "stable_sort"    # 禁止 std::stable_sort
      - "partial_sort"   # 禁止 std::partial_sort
    required:
      - "bubbleSort"     # 必須實作 bubbleSort
```

### 範例 5：個別測資配分

不同難度的測資給予不同分數：

```yaml
problems:
  p5:
    name: "進階題目"
    points: 100
    timeout: 3
    cases:
      "01": 10   # 基本案例
      "02": 10   # 基本案例
      "03": 20   # 邊界案例
      "04": 20   # 邊界案例
      "05": 20   # 特殊案例
      "06": 20   # 壓力測試
```

### 範例 6：完整配置檔案

包含多個題目的完整配置：

```yaml
app:
  title: "資料結構作業測試系統"
  description: "2024 秋季班"

compiler:
  timeout: 10
  flags: "-std=c++17 -O2 -Wall"

runner:
  timeout: 5
  memory_limit: 256

test:
  stop_on_first_fail: false

problems:
  # 基本題目
  p1:
    name: "陣列加總"
    points: 25

  # 遞迴題目
  p2:
    name: "階乘計算"
    points: 25
    forbidden:
      - "for"
      - "while"
    required:
      - "factorial"

  # 排序題目
  p3:
    name: "氣泡排序"
    points: 30
    timeout: 2
    forbidden:
      - "sort"
    required:
      - "bubbleSort"

  # 複雜題目（個別計分）
  p4:
    name: "進階演算法"
    points: 50
    timeout: 3
    cases:
      "01": 10
      "02": 10
      "03": 15
      "04": 15
```

---

## 常見問題

### Q1: 修改 config.yaml 後需要重啟什麼嗎？

**答**：不需要。每次執行 `python3 run_tests.py` 時，系統都會重新讀取配置檔案。

### Q2: forbidden 可以禁止哪些東西？

**答**：任何在程式碼中以文字形式出現的內容，包括：
- 關鍵字：`for`, `while`, `if`, etc.
- 函數名稱：`sort`, `printf`, etc.
- 標頭檔：`algorithm`, `vector`, etc.
- 註解也會被檢查

**注意**：系統使用簡單的字串搜尋，所以 `for` 會匹配到 `for`, `before`, `information` 等。

### Q3: required 檢查函數簽章嗎？

**答**：不會。系統只檢查函數名稱是否出現在程式碼中，不檢查參數、回傳值或實作細節。

### Q4: cases 的分數總和可以不等於 points 嗎？

**答**：技術上可以，但不建議。如果總和小於 points，學生無法獲得滿分；如果總和大於 points，學生可能得分超過題目分數。

### Q5: 如何為某個題目設定不同的編譯參數？

**答**：目前系統不支援個別題目的編譯參數。所有題目使用相同的 `compiler.flags`。

### Q6: memory_limit 為什麼標註「未實作」？

**答**：記憶體限制功能尚未實作。配置該選項不會產生任何效果。

### Q7: 如何禁止使用某個標頭檔？

**答**：使用 `forbidden` 列出標頭檔名稱：
```yaml
forbidden:
  - "#include <algorithm>"
  - "algorithm"  # 更寬鬆的檢查
```

### Q8: 配置檔案格式錯誤會怎樣？

**答**：系統會在啟動時顯示錯誤訊息並停止執行。常見錯誤：
- YAML 縮排錯誤
- 缺少必填欄位（name, points）
- 資料型態錯誤（如 points 填入字串）

**驗證配置**：
```bash
python3 run_tests.py  # 會自動驗證配置檔案
```

---

## 修改配置的工作流程

1. **備份配置檔案**
   ```bash
   cp config/config.yaml config/config.yaml.backup
   ```

2. **編輯配置**
   ```bash
   # 使用任何文字編輯器
   vim config/config.yaml
   # 或
   code config/config.yaml
   ```

3. **驗證配置**
   ```bash
   python3 run_tests.py
   ```

4. **測試變更**
   ```bash
   python3 run_tests.py p1  # 測試單一題目
   ```

---

## 相關文件

- **[README.md](README.md)** - 系統維護指南
- **[README_STUDENT.md](README_STUDENT.md)** - 學生使用指南

---

**最後更新**: 2024 年 11 月
