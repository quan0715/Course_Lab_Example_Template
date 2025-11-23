# 安裝指南

本指南將引導您從零開始，在電腦上設定 C++ Lab 測試系統的執行環境。

**目標讀者**: 完全沒有 Python 經驗的新手

**預計時間**: 15-30 分鐘

---

## 📋 安裝步驟總覽

1. 安裝 Python
2. 驗證 Python 安裝
3. 下載/取得專案檔案
4. 建立虛擬環境
5. 安裝必要套件
6. 驗證環境設定

---

## Windows 用戶安裝步驟

### 步驟 1: 安裝 Python

#### 1.1 下載 Python

1. 前往 Python 官方網站: https://www.python.org/downloads/
2. 點擊黃色的「Download Python 3.x.x」按鈕（x 代表版本號）
3. 建議下載 **Python 3.11** 或更新版本

#### 1.2 執行安裝程式

1. 找到下載的檔案（通常在「下載」資料夾），檔名類似 `python-3.11.x.exe`
2. 雙擊執行安裝程式
3. **重要**: 在安裝視窗最下方，勾選「Add Python to PATH」
4. 點擊「Install Now」
5. 等待安裝完成（約 2-5 分鐘）
6. 看到「Setup was successful」後，點擊「Close」

### 步驟 2: 驗證 Python 安裝

#### 2.1 開啟命令提示字元

方法一：
- 按下鍵盤上的 `Windows鍵 + R`
- 輸入 `cmd` 後按 Enter

方法二：
- 點擊開始選單
- 搜尋「命令提示字元」或「cmd」
- 點擊開啟

#### 2.2 檢查 Python 版本

在命令提示字元視窗中，輸入以下指令後按 Enter：

```cmd
python --version
```

應該會看到類似以下的輸出：
```
Python 3.11.x
```

如果看到「'python' 不是內部或外部命令」，請參考本文件最後的「常見問題」章節。

#### 2.3 檢查 pip（Python 套件管理工具）

在命令提示字元中輸入：

```cmd
pip --version
```

應該會看到類似以下的輸出：
```
pip 23.x.x from ...
```

### 步驟 3: 取得專案檔案

1. 將老師提供的專案資料夾複製到您的電腦
2. 建議放在容易找到的位置，例如：`C:\Users\您的使用者名稱\Desktop\cpp_lab`
3. 記住這個路徑，等等會用到

### 步驟 4: 建立虛擬環境

#### 4.1 切換到專案目錄

在命令提示字元中，使用 `cd` 指令切換到專案資料夾。

假設專案在桌面上，輸入（請替換成您的實際路徑）：

```cmd
cd C:\Users\您的使用者名稱\Desktop\cpp_lab\input-output-test-module
```

小技巧：可以直接在檔案總管中開啟專案資料夾，在資料夾空白處按住 Shift 後點滑鼠右鍵，選擇「在此處開啟 PowerShell 視窗」或「在終端機中開啟」。

#### 4.2 建立虛擬環境

輸入以下指令：

```cmd
python -m venv venv
```

說明：
- 這個指令會建立一個名為 `venv` 的資料夾
- 資料夾裡包含這個專案專用的 Python 環境
- 需要等待約 10-30 秒

#### 4.3 啟動虛擬環境

輸入以下指令：

```cmd
venv\Scripts\activate
```

成功後，命令提示字元的開頭會出現 `(venv)`，例如：
```
(venv) C:\Users\您的使用者名稱\Desktop\cpp_lab\input-output-test-module>
```

這表示您現在在虛擬環境中了！

### 步驟 5: 安裝必要套件

確認您在虛擬環境中（看到 `(venv)` 開頭），然後輸入：

```cmd
pip install -r requirements.txt
```

這個指令會自動安裝所有需要的套件，包括：
- Flask（網頁介面）
- PyYAML（讀取設定檔）
- Markdown（顯示題目說明）

等待安裝完成（約 30-60 秒）。

### 步驟 6: 驗證環境設定

執行驗證腳本：

```cmd
python scripts\verify_python_setup.py
```

如果一切正常，會看到綠色的成功訊息：
```
🎉 環境設定完成！您可以開始使用測試系統了
```

### 完成！

現在您可以開始使用測試系統了。請參考 `README_STUDENT.md` 了解如何使用。

---

## macOS 用戶安裝步驟

### 步驟 1: 檢查並安裝 Python

#### 1.1 檢查是否已安裝 Python 3

1. 開啟「終端機」應用程式
   - 方法一：按 `Command + 空白鍵`，輸入「終端機」或「Terminal」
   - 方法二：在「應用程式」→「工具程式」中找到「終端機」

2. 在終端機中輸入：

```bash
python3 --version
```

如果看到 `Python 3.7` 或更新的版本，可以跳到步驟 2。

#### 1.2 安裝 Python（如果尚未安裝）

**方法一：使用官方安裝程式（推薦給新手）**

1. 前往 Python 官方網站: https://www.python.org/downloads/
2. 點擊黃色的「Download Python 3.x.x」按鈕
3. 下載完成後，開啟 `.pkg` 檔案
4. 跟隨安裝精靈的指示完成安裝

**方法二：使用 Homebrew（適合進階使用者）**

如果您已經安裝 Homebrew：

```bash
brew install python3
```

### 步驟 2: 驗證 Python 安裝

在終端機中輸入：

```bash
python3 --version
pip3 --version
```

應該會看到 Python 和 pip 的版本資訊。

### 步驟 3: 取得專案檔案

1. 將老師提供的專案資料夾複製到您的電腦
2. 建議放在容易找到的位置，例如：`~/Desktop/cpp_lab`
3. 記住這個路徑

### 步驟 4: 建立虛擬環境

#### 4.1 切換到專案目錄

在終端機中，使用 `cd` 指令切換到專案資料夾：

```bash
cd ~/Desktop/cpp_lab/input-output-test-module
```

小技巧：可以將資料夾直接拖曳到終端機視窗中，會自動填入路徑。

#### 4.2 建立虛擬環境

輸入以下指令：

```bash
python3 -m venv venv
```

說明：
- 這個指令會建立一個名為 `venv` 的資料夾
- 資料夾裡包含這個專案專用的 Python 環境
- 需要等待約 10-30 秒

#### 4.3 啟動虛擬環境

輸入以下指令：

```bash
source venv/bin/activate
```

成功後，終端機的開頭會出現 `(venv)`，例如：
```
(venv) username@MacBook cpp_lab %
```

這表示您現在在虛擬環境中了！

### 步驟 5: 安裝必要套件

確認您在虛擬環境中（看到 `(venv)` 開頭），然後輸入：

```bash
pip install -r requirements.txt
```

這個指令會自動安裝所有需要的套件。等待安裝完成（約 30-60 秒）。

### 步驟 6: 驗證環境設定

執行驗證腳本：

```bash
python3 scripts/verify_python_setup.py
```

如果一切正常，會看到綠色的成功訊息：
```
🎉 環境設定完成！您可以開始使用測試系統了
```

### 完成！

現在您可以開始使用測試系統了。請參考 `README_STUDENT.md` 了解如何使用。

---

## 常見問題

### Q1: Windows 說找不到 'python' 指令

**原因**: Python 沒有加入到系統 PATH 中。

**解決方法**:
1. 重新執行 Python 安裝程式
2. 選擇「Modify」
3. 在「Advanced Options」中勾選「Add Python to environment variables」
4. 完成後重新開啟命令提示字元

或者，嘗試使用 `py` 指令代替 `python`：
```cmd
py --version
py -m venv venv
```

### Q2: pip 安裝套件時出現權限錯誤

**Windows**:
- 以系統管理員身分執行命令提示字元
- 或確認您在虛擬環境中執行

**macOS**:
- 確認您在虛擬環境中執行
- 避免使用 `sudo pip`（這會安裝到系統層級）

### Q3: 虛擬環境啟動失敗

**Windows PowerShell 權限問題**:

如果出現「無法載入檔案，因為這個系統上已停用指令碼執行」的錯誤：

1. 以系統管理員身分開啟 PowerShell
2. 執行：`Set-ExecutionPolicy RemoteSigned`
3. 輸入 `Y` 確認

或改用命令提示字元（cmd）而非 PowerShell。

**macOS 權限問題**:

如果出現權限錯誤，執行：
```bash
chmod +x venv/bin/activate
```

### Q4: 我關閉終端機/命令提示字元後要重新開始嗎？

是的，每次開啟新的終端機視窗時，都需要：
1. 切換到專案目錄（`cd` 指令）
2. 重新啟動虛擬環境（`activate` 指令）

這是正常的！請參考 `QUICK_START.md` 了解每次使用的快速流程。

### Q5: 安裝套件時很慢或失敗

**可能原因**:
- 網路連線問題
- 防火牆封鎖

**解決方法**:
1. 檢查網路連線
2. 嘗試使用其他網路（如手機熱點）
3. 稍後再試

### Q6: 驗證腳本說某些目錄不存在

**可能原因**:
- 不在正確的專案目錄中
- 專案檔案不完整

**解決方法**:
1. 確認您在專案根目錄（應該看到 `run_tests.py` 檔案）
2. 使用 `ls`（macOS）或 `dir`（Windows）列出檔案確認
3. 重新下載完整的專案檔案

### Q7: macOS 說無法執行腳本（安全性問題）

**macOS Catalina 或更新版本的安全性限制**:

1. 前往「系統偏好設定」→「安全性與隱私權」
2. 在「一般」分頁中，點擊「強制允許」
3. 或在終端機中給予執行權限：
   ```bash
   chmod +x scripts/*.py
   chmod +x scripts/*.sh
   ```

---

## 需要更多協助？

- 查看 `README_STUDENT.md` - 學生使用指南
- 查看 `QUICK_START.md` - 快速參考卡
- 詢問老師或助教
- 檢查是否有更新的文件

---

## 下一步

環境設定完成後，請前往：
- **`README_STUDENT.md`** - 了解如何使用測試系統
- **`QUICK_START.md`** - 快速指令參考

