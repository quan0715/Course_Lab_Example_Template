# C++ Lab 測試系統（模板專案）

## 專案簡介

這是一個簡單易用的 C++ 程式作業測試系統，專為教學環境設計。系統會自動編譯、執行並測試學生的 C++ 程式碼，並提供詳細的測試結果和評分。

**主要特色**：
- ✅ 跨平台支援（Linux、Windows、macOS）
- ✅ 自動編譯與測試
- ✅ 詳細的錯誤報告與差異比對
- ✅ 可自訂評分配置
- ✅ 網頁介面（GUI）模式
- ✅ 獨立執行檔，無需安裝 Python

## 專案結構

```
.
├── src/                    # 學生程式碼目錄
│   ├── p1.cpp             # 問題 1 的解答
│   ├── p2.cpp             # 問題 2 的解答
│   └── ...
├── tests/                  # 測試資料目錄
│   ├── p1/
│   │   ├── inputs/        # 輸入檔案 (*.in)
│   │   └── outputs/       # 預期輸出 (*.out)
│   └── ...
├── config/                 # 配置檔案
│   ├── points.conf        # 評分配置
│   └── config.yaml        # 系統配置
├── scripts/                # 執行腳本
│   ├── run_tests.sh       # Linux/macOS 測試腳本
│   ├── run_tests.bat      # Windows 測試腳本
│   └── build_executables.sh  # 建置執行檔腳本
├── build/                  # 編譯產物與測試結果
├── dist/                   # 打包後的執行檔
├── templates/              # 網頁介面模板
├── run_tests.py           # Python 測試程式
└── README.md              # 本說明文件
```

## 使用方式

### 方法一：使用打包後的執行檔（推薦）

打包後的執行檔已包含所有必要的依賴，無需安裝 Python 即可使用。

#### 1. 取得執行檔

執行檔位於 `dist/` 目錄：
- **Linux**: `dist/run_tests_linux`
- **Windows**: `dist/run_tests.exe`
- **macOS**: `dist/run_tests_mac`

#### 2. 執行測試

**Linux / macOS**:
```bash
# 給予執行權限（首次使用）
chmod +x dist/run_tests_linux  # 或 run_tests_mac

# 執行所有測試
./dist/run_tests_linux

# 執行特定問題的測試
./dist/run_tests_linux p1

# 使用網頁介面
./dist/run_tests_linux --gui
```

**Windows**:
```cmd
# 執行所有測試
dist\run_tests.exe

# 執行特定問題的測試
dist\run_tests.exe p1

# 使用網頁介面
dist\run_tests.exe --gui
```

#### 3. 網頁介面說明

使用 `--gui` 參數啟動網頁介面後：
1. 系統會自動在瀏覽器開啟測試介面（預設：http://localhost:5000）
2. 點擊「執行測試」按鈕開始測試
3. 點擊各個問題卡片可查看詳細的測試結果
4. 可以查看每個測試案例的輸入、預期輸出和實際輸出

---

### 方法二：使用 Python 直接執行

如果您已安裝 Python 3.7+，可以直接執行 Python 腳本。

```bash
# 執行所有測試
python3 run_tests.py

# 執行特定問題
python3 run_tests.py p1

# 強制顯示顏色
python3 run_tests.py --color

# 使用網頁介面
python3 run_tests.py --gui
```

---

### 方法三：使用 Shell 腳本

**Linux / macOS**:
```bash
bash scripts/run_tests.sh
```

**Windows**:
```cmd
scripts\run_tests.bat
```

## 評分系統

### 預設評分規則

- 每個問題預設 100 分
- **全部通過才給分**：只有當問題的所有測試案例都通過時，才會獲得該問題的分數
- 最終分數為所有問題的總分

### 自訂評分配置

編輯 `config/points.conf` 檔案來自訂每個問題的分數：

```ini
# 設定問題 p1 為 50 分
problem.p1=50

# 設定問題 p2 為 30 分
problem.p2=30

# 未設定的問題預設為 100 分
```

### 測試結果檔案

測試完成後，系統會在 `build/` 目錄產生以下檔案：

- `build/pX.cases`: 記錄通過/總共的測試案例數（格式：`通過數 總數`）
- `build/pX.score`: 記錄獲得/總共的分數（格式：`獲得分數 總分`）
- `build/pX.compile.log`: 編譯日誌
- `build/pX.run.log`: 執行日誌

## 輸出說明

測試執行時會顯示：

1. **編譯狀態**：顯示每個問題的編譯結果
2. **測試結果**：
   - ✅ PASS：測試通過
   - ❌ FAIL：測試失敗
   - ⏱️ TLE：執行逾時
3. **失敗詳情**（當測試失敗時）：
   - 預期輸出（Expected）
   - 實際輸出（Got）
   - 差異比對（Diff）
   - 行尾資訊（EOL）
4. **總結表格**：顯示每個問題的通過/失敗測試數和得分

## 建置執行檔

如果您想要自行建置執行檔：

### 1. 安裝 PyInstaller

```bash
pip install pyinstaller
```

### 2. 執行建置腳本

```bash
bash scripts/build_executables.sh
```

### 3. 取得執行檔

建置完成後，執行檔會出現在 `dist/` 目錄：
- `dist/run_tests_linux`（Linux）
- `dist/run_tests.exe`（Windows）
- `dist/run_tests_mac`（macOS）

**注意**：PyInstaller 只能為當前平台建置執行檔。若要建置所有平台的執行檔，需要在各個平台上分別執行建置腳本。

## Windows 注意事項

- Windows 批次腳本會自動處理 CRLF 與 LF 的換行符號差異
- 如果編譯失敗，該問題的所有測試案例都會被標記為失敗，分數為 0

## 範例

```bash
# 使用執行檔測試所有問題
./dist/run_tests_linux

# 使用執行檔測試單一問題
./dist/run_tests_linux p1

# 使用網頁介面
./dist/run_tests_linux --gui

# 使用 Python 直接執行
python3 run_tests.py --gui
```

## 常見問題

### Q: 執行檔無法執行怎麼辦？

**Linux/macOS**: 確保已給予執行權限
```bash
chmod +x dist/run_tests_linux
```

**macOS**: 如果出現安全性警告，請到「系統偏好設定 > 安全性與隱私權」允許執行

### Q: 如何新增測試案例？

1. 在 `tests/pX/inputs/` 目錄新增 `.in` 檔案（輸入）
2. 在 `tests/pX/outputs/` 目錄新增對應的 `.out` 檔案（預期輸出）
3. 檔名必須相同（例如：`01.in` 對應 `01.out`）

### Q: 如何修改網頁介面的標題？

編輯 `config/config.yaml` 檔案：
```yaml
app:
  title: "您的標題"
  description: "您的描述"
```

## 授權

本專案為教學用途的模板專案。
