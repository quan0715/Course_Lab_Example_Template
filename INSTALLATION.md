# 安裝指南

本指南將引導您從零開始，設定 C++ Lab 測試系統的執行環境。

> **💡 提示**: 我們提供了自動安裝腳本，可以快速完成設定！  
> 如果您想直接使用自動安裝，請跳到「[快速安裝](#-快速安裝-推薦)」章節。

---

## 🚀 快速安裝（推薦）

### Windows 用戶

1. **確認已安裝 Python 3.7+**（如果沒有，請先看[手動安裝](#windows-手動安裝步驟)的步驟 1-2）

2. **開啟命令提示字元或 PowerShell**
   - 在專案資料夾空白處，按住 `Shift` 後點滑鼠右鍵
   - 選擇「在此處開啟 PowerShell 視窗」或「在終端機中開啟」

3. **執行自動安裝腳本**

   **使用命令提示字元 (cmd)：**
   ```cmd
   scripts\setup_env.bat
   ```

   **使用 PowerShell：**
   ```powershell
   scripts\setup_env.bat
   ```
   
   > **⚠️ PowerShell 權限問題？**  
   > 如果 PowerShell 出現「無法載入檔案」錯誤，請：
   > - **方法 1（推薦）**：改用命令提示字元 (cmd)
   > - **方法 2**：以系統管理員身分開啟 PowerShell，執行 `Set-ExecutionPolicy RemoteSigned`，輸入 `Y` 確認

4. **完成！** 腳本會自動：
   - ✅ 建立虛擬環境
   - ✅ 安裝所有必要套件
   - ✅ 驗證環境設定

### macOS/Linux 用戶

1. **確認已安裝 Python 3.7+**（如果沒有，請先看[手動安裝](#macos-手動安裝步驟)的步驟 1）

2. **開啟終端機**，切換到專案目錄：
   ```bash
   cd ~/Desktop/cpp_lab/Course_Lab_Example_Template
   ```

3. **執行自動安裝腳本**：
   ```bash
   bash scripts/setup_env.sh
   ```

4. **完成！** 腳本會自動完成所有設定

---

## 📖 使用測試系統

安裝完成後，每次使用時：

### Windows

**使用命令提示字元 (cmd)：**
```cmd
:: 1. 啟動虛擬環境
venv\Scripts\activate

:: 2. 執行測試
python run_tests.py
```

**使用 PowerShell：**
```powershell
# 1. 啟動虛擬環境
venv\Scripts\Activate.ps1

# 2. 執行測試
python run_tests.py
```

> **💡 推薦使用命令提示字元 (cmd)**，可以避免 PowerShell 權限問題

### macOS/Linux

```bash
# 1. 啟動虛擬環境
source venv/bin/activate

# 2. 執行測試
python3 run_tests.py
```

啟動成功後，命令列前面會出現 `(venv)` 標示。

---

## Windows 手動安裝步驟

> **💡 提示**: 如果自動安裝失敗，才需要手動安裝

### 步驟 1: 安裝 Python

1. **下載 Python**
   - 前往 https://www.python.org/downloads/
   - 點擊黃色的「Download Python 3.11.x」按鈕（建議 3.11 或更新版本）
   - 瀏覽器會開始下載，檔案名稱類似 `python-3.11.x.exe`
   - 等待下載完成（通常在「下載」資料夾）

2. **執行安裝程式**
   - 在「下載」資料夾中，找到 `python-3.11.x.exe`
   - 雙擊執行安裝程式
   - ⚠️ **非常重要**: 在安裝視窗**最下方**，勾選 ✅ **「Add Python to PATH」**
   - 點擊「Install Now」
   - 等待安裝進度條完成（約 2-5 分鐘）
   - 看到「Setup was successful」後，點擊「Close」

### 步驟 2: 驗證 Python 安裝

1. **開啟命令提示字元**
   - 按 `Windows鍵 + R`，輸入 `cmd`，按 Enter

2. **檢查 Python 版本**
   ```cmd
   python --version
   ```
   應會顯示：`Python 3.11.x`

   > **找不到 python？** 嘗試 `py --version`

### 步驟 3: 切換到專案目錄

```cmd
cd C:\Users\您的使用者名稱\Desktop\cpp_lab\Course_Lab_Example_Template
```

> **💡 小技巧**: 在檔案總管的專案資料夾中，於網址列輸入 `cmd` 可快速開啟命令提示字元

### 步驟 4: 建立虛擬環境

```cmd
python -m venv venv
```

等待 10-30 秒，會建立 `venv` 資料夾。

### 步驟 5: 啟動虛擬環境

**命令提示字元 (cmd)：**
```cmd
venv\Scripts\activate
```

**PowerShell：**
```powershell
venv\Scripts\Activate.ps1
```

成功後會看到 `(venv)` 開頭：
```
(venv) C:\Users\...\Course_Lab_Example_Template>
```

### 步驟 6: 安裝必要套件

```cmd
pip install -r requirements.txt
```

等待 30-60 秒。

### 步驟 7: 驗證環境

```cmd
python scripts\verify_python_setup.py
```

看到綠色的「🎉 環境設定完成」即成功！

---

## macOS 手動安裝步驟

> **💡 提示**: 如果自動安裝失敗，才需要手動安裝

### 步驟 1: 安裝 Python

1. **檢查是否已安裝**
   ```bash
   python3 --version
   ```
   如果顯示 `Python 3.7` 或更新版本，跳到步驟 2

2. **下載並安裝 Python**
   - 前往 https://www.python.org/downloads/
   - 點擊黃色的「Download Python 3.11.x」按鈕
   - 瀏覽器會開始下載，檔案名稱類似 `python-3.11.x-macos11.pkg`
   - 等待下載完成
   
3. **執行安裝程式**
   - 在「下載」資料夾中，雙擊 `.pkg` 檔案
   - 會開啟 Python 安裝程式視窗
   - 點擊「繼續」
   - 閱讀授權條款後，點擊「繼續」，然後點擊「同意」
   - 點擊「安裝」（可能需要輸入您的 macOS 密碼）
   - 等待安裝完成（約 2-5 分鐘）
   - 看到「安裝成功」後，點擊「關閉」

### 步驟 2: 切換到專案目錄

```bash
cd ~/Desktop/cpp_lab/Course_Lab_Example_Template
```

> **💡 小技巧**: 可將資料夾拖曳到終端機自動填入路徑

### 步驟 3: 建立虛擬環境

```bash
python3 -m venv venv
```

### 步驟 4: 啟動虛擬環境

```bash
source venv/bin/activate
```

成功後會看到 `(venv)` 開頭。

### 步驟 5: 安裝必要套件

```bash
pip install -r requirements.txt
```

### 步驟 6: 驗證環境

```bash
python3 scripts/verify_python_setup.py
```

---

## ❓ 常見問題

### Windows：找不到 'python' 指令

**解決方法**:
- 嘗試使用 `py` 代替 `python`
- 或重新安裝 Python，確認勾選「Add Python to PATH」

### Windows：PowerShell 無法執行腳本

**錯誤訊息**: 「無法載入檔案，因為這個系統上已停用指令碼執行」

**解決方法（擇一）**:
1. **改用命令提示字元 (cmd)**（推薦）
2. 以系統管理員身分開啟 PowerShell，執行：
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```
   輸入 `Y` 確認

### 每次都要啟動虛擬環境嗎？

**是的**，每次開啟新的終端機視窗，都需要重新啟動虛擬環境：

**Windows (cmd):**
```cmd
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

這是 Python 虛擬環境的正常運作方式。

### 安裝套件時很慢或失敗

**解決方法**:
- 檢查網路連線
- 嘗試其他網路（如手機熱點）
- 稍後再試

---

## 🎓 下一步

環境設定完成後：
- 📖 查看 **`README_STUDENT.md`** - 了解如何使用測試系統

需要更多協助？請詢問老師或助教。
