# C++ Lab 測試系統 - 學生/TA 使用指南

歡迎使用 C++ Lab 測試系統！本指南將幫助您了解如何使用系統、哪些檔案可以修改。

**如果您是 AI 或維護者**，請改看：[`README.md`](README.md)

---

## ⚠️ 重要：檔案權限說明

在開始之前，請務必了解哪些檔案可以動、哪些不能動：

### ✅ 您可以修改的檔案（學生）

```
src/
├── p1.cpp    ← ✅ 您的程式碼，隨意修改
├── p2.cpp    ← ✅ 您的程式碼，隨意修改
├── p3.cpp    ← ✅ 您的程式碼，隨意修改
└── ...       ← ✅ 所有 src/ 下的 .cpp 檔案都可以修改
```

**這是唯一您應該修改的目錄！**

### 👁️ 您可以查看的檔案（學生/TA）

```
problems/
├── p1.md     ← 👁️ 題目說明，可以看，不要改
├── p2.md     ← 👁️ 題目說明，可以看，不要改
└── ...

tests/
├── p1/
│   ├── inputs/
│   │   ├── 01.in    ← 👁️ 測試輸入，可以看，不要改
│   │   └── ...
│   └── outputs/
│       ├── 01.out   ← 👁️ 正確答案，可以看，不要改
│       └── ...
└── ...

build/
├── p1.score         ← 👁️ 您的分數
├── p1.compile.log   ← 👁️ 編譯記錄
├── p1.run.log       ← 👁️ 執行記錄
└── ...
```

**可以查看這些檔案來：**

- 了解題目要求（`problems/`）
- 查看測試資料（`tests/`）
- 檢查測試結果（`build/`）

### ❌ 您不應該修改的檔案

```
config/           ← ❌ 系統配置，不要改
app/              ← ❌ 系統核心，不要改
templates/        ← ❌ 網頁介面，不要改
static/           ← ❌ 網頁資源，不要改
scripts/          ← ❌ 系統腳本，不要改
run_tests.py      ← ❌ 主程式，不要改
add_problem.py    ← ❌ 工具腳本，不要改
*.md              ← ❌ 說明文件，不要改
requirements.txt  ← ❌ 依賴清單，不要改
.gitignore        ← ❌ Git 設定，不要改
```

**修改這些檔案可能導致：**

- ❌ 系統無法正常運作
- ❌ 測試結果不正確
- ❌ 無法獲得正確評分
- ❌ 其他學生的環境也受影響

### 📌 給 TA 的說明

如果您是助教，需要管理題目和測資，請：

1. **閱讀完整的維護文件**：[`README.md`](README.md)
2. **這些檔案您可以修改**：
   - `tests/` - 新增/修改測試案例
   - `problems/` - 編輯題目說明
   - `config/config.yaml` - 調整題目配置
3. **使用工具腳本**：
   - `python3 add_problem.py` - 新增題目
   - 參考 README.md 的完整操作指南

---

## 📚 還沒設定環境嗎？

如果這是您第一次使用，請先參考：

- **[安裝指南 (INSTALLATION.md)](INSTALLATION.md)** - 完整的環境設定步驟

**大約需要 15-30 分鐘**完成環境設定，之後就可以一直使用了！

---

## 🚀 快速開始（三步驟）

### 第 1 步：啟動虛擬環境

每次**開啟新的終端機視窗**時，都需要啟動虛擬環境。

> **💡 說明**：如果終端機一直開著，虛擬環境會保持啟動狀態，不需要重複執行。只有在關閉終端機後重新開啟、或開啟新的終端機視窗時，才需要再次啟動。

#### Windows 用戶

**方法 1：使用命令提示字元 (cmd) - 推薦**

1. 開啟命令提示字元
   - 按 `Windows鍵 + R`，輸入 `cmd`，按 Enter
   - 或在專案資料夾的網址列輸入 `cmd`

2. 切換到專案目錄並啟動環境
   ```cmd
   cd C:\路徑\到\專案\Course_Lab_Example_Template
   venv\Scripts\activate
   ```

**方法 2：使用 PowerShell**

1. 開啟 PowerShell（在專案資料夾按住 `Shift` + 右鍵）

2. 啟動環境
   ```powershell
   venv\Scripts\Activate.ps1
   ```

> 💡 **推薦使用命令提示字元 (cmd)**，可避免 PowerShell 權限問題

#### macOS / Linux 用戶

1. 開啟終端機

2. 切換到專案目錄並啟動環境
   ```bash
   cd ~/路徑/到/專案/Course_Lab_Example_Template
   source venv/bin/activate
   ```

#### ✅ 啟動成功

命令列開頭會出現 `(venv)` 標示：
```
(venv) C:\...\Course_Lab_Example_Template>    # Windows
(venv) username@MacBook Course_Lab_Example_Template %  # macOS
```

### 第 2 步：寫程式

用您習慣的文字編輯器（記事本、VS Code、Dev-C++ 等）開啟並編輯：

```
src/p1.cpp  ← 題目 1 的程式碼（✅ 可以改）
src/p2.cpp  ← 題目 2 的程式碼（✅ 可以改）
...
```

⚠️ **只修改 `src/` 目錄下的 `.cpp` 檔案！**

寫完程式後，記得**儲存檔案**！

### 第 3 步：執行測試

在終端機/命令提示字元中執行：

```bash
# 測試所有題目
python3 run_tests.py

# 只測試某一題（例如題目 1）
python3 run_tests.py p1
```

> **Windows 用戶注意**：將 `python3` 改成 `python`

系統會自動：

1. ✅ 編譯您的程式
2. ✅ 用測試資料執行程式
3. ✅ 比對輸出結果
4. ✅ 顯示測試結果和分數

---

## 🌐 使用網頁介面（推薦）

網頁介面更友善，可以看到更多細節！

### 啟動網頁介面

```bash
python3 run_tests.py --gui
```

瀏覽器會自動開啟 `http://localhost:8080`，顯示測試介面。

### 使用方式

1. **點擊「執行測試」按鈕** - 開始測試所有題目
2. **查看結果** - 題目卡片會顯示：
   - 🟢 綠色：全部通過
   - 🔴 紅色：有錯誤
3. **點擊題目卡片** - 查看詳細資訊：
   - 題目說明
   - 每個測試案例的結果
   - 您的輸出 vs 正確輸出
   - 編譯或執行錯誤訊息
4. **點擊「Push to GitHub」按鈕** - 一鍵推送程式碼到 GitHub
   - 系統會彈出確認視窗，說明即將執行的操作
   - 確認後自動執行：
     - 檢查是否有程式碼變更
     - `git add src/*.cpp`
     - `git commit -m "GUI 自動提交"`
     - `git push`
   - ⚠️ 如果沒有修改任何 `.cpp` 檔案，系統會拒絕提交

### 關閉伺服器

按 `Ctrl+C` 停止網頁伺服器。

---

## 📖 測試結果說明

### 成功的測試

```
✅ PASS: p1 - Test case 01.in (0.12s)
```

恭喜！這個測試案例通過了。

### 失敗的測試

```
❌ FAIL: p1 - Test case 01.in

預期輸出:
Hello, World!

實際輸出:
hello world

差異:
- Hello, World!
+ hello world
```

說明：

- **預期輸出**: 正確答案應該是什麼
- **實際輸出**: 您的程式輸出了什麼
- **差異**: 標示出不同的地方
  - `-` 開頭：應該要有但沒有
  - `+` 開頭：多出來的內容

### 編譯錯誤

```
❌ COMPILE ERROR: p1

錯誤訊息:
p1.cpp:5:10: error: expected ';' before 'return'
```

說明：您的程式有語法錯誤，無法編譯。請檢查錯誤訊息並修正程式碼。

### 執行逾時

```
⏱️ TLE: p1 - Test case 01.in (5.00s)
```

說明：程式執行時間超過限制（通常是 1-5 秒）。可能的原因：

- 無窮迴圈
- 演算法效率太低
- 等待輸入但沒有輸入資料

---

## 💯 評分系統

### 如何計分？

- 每個題目有固定分數（通常是 25 分或 100 分）
- **必須通過所有測試案例**才能拿到分數
- 只通過部分測試案例 = 0 分

### 範例

假設題目 p1 有 5 個測試案例：

| 通過測試 | 得分    |
| -------- | ------- |
| 5/5 通過 | 滿分 ✅ |
| 4/5 通過 | 0 分 ❌ |
| 0/5 通過 | 0 分 ❌ |

**小提示**：確保您的程式能處理所有情況！

---

## 🔍 常見問題

### Q1: 測試失敗，但我覺得我的答案是對的？

**檢查清單**：

- [ ] 輸出格式是否**完全一致**？（大小寫、標點符號、空格）
- [ ] 每行末尾有沒有多餘的空格？
- [ ] 最後一行有沒有換行？
- [ ] 是否處理了所有邊界情況？

**建議**：使用網頁介面查看「預期輸出」和「實際輸出」的差異。

### Q2: 編譯錯誤訊息看不懂？

常見錯誤：

- `expected ';'` → 少了分號
- `undeclared identifier` → 變數名稱打錯或沒有宣告
- `cannot convert` → 資料型態不符

**建議**：複製錯誤訊息，Google 搜尋或詢問助教。

### Q3: 程式在我的電腦上可以執行，但測試失敗？

可能原因：

- 您的程式依賴特定環境（例如 Windows 特有功能）
- 輸出格式在不同系統上不一致
- 使用了不標準的 C++ 語法

**建議**：使用標準 C++ 語法，避免使用系統特定功能。

### Q4: 忘記啟動虛擬環境了怎麼辦？

會看到錯誤訊息：`command not found` 或找不到模組。

**解決方法**：

```bash
# 啟動虛擬環境
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

看到 `(venv)` 就表示成功了。

### Q5: 測試很慢，要等很久？

可能原因：

- 程式效率太低（巢狀迴圈過多）
- 測試案例很大
- 您的電腦效能較慢

**建議**：

- 先測試單一題目：`python3 run_tests.py p1`
- 優化您的演算法
- 檢查是否有無窮迴圈

### Q6: 我可以看測試案例的內容嗎？

當然可以！測試案例都是公開的：

```
tests/
  └── p1/
      ├── inputs/      ← 輸入檔案（可以看）
      │   ├── 01.in
      │   ├── 02.in
      │   └── ...
      └── outputs/     ← 正確輸出（可以看）
          ├── 01.out
          ├── 02.out
          └── ...
```

可以用記事本或任何文字編輯器開啟這些檔案。

⚠️ **但是不要修改這些檔案！**

### Q7: 我不小心修改了系統檔案怎麼辦？

如果您修改了不該修改的檔案：

1. **立即告訴助教或老師**
2. 如果使用 Git，可以還原：
   ```bash
   git restore <檔案名稱>
   ```
3. 重新下載完整的專案檔案

---

## 💡 使用技巧

### 技巧 1：逐個測試案例除錯

```bash
# 只測試一題
python3 run_tests.py p1

# 如果失敗，查看輸入檔案
cat tests/p1/inputs/01.in  # macOS/Linux
type tests\p1\inputs\01.in  # Windows

# 查看正確答案
cat tests/p1/outputs/01.out  # macOS/Linux
type tests\p1\outputs\01.out  # Windows
```

### 技巧 2：使用網頁介面查看差異

網頁介面會清楚標示：

- ✅ 哪些字元是正確的
- ❌ 哪些字元是錯誤的
- 逐字元比對

### 技巧 3：檢查您的分數和日誌

```bash
# 查看分數
cat build/p1.score

# 查看編譯記錄
cat build/p1.compile.log

# 查看執行記錄
cat build/p1.run.log
```

### 技巧 4：在自己的電腦上測試

在提交前，可以手動測試：

```bash
# macOS/Linux
g++ -std=c++17 -o my_test src/p1.cpp
./my_test < tests/p1/inputs/01.in

# Windows
g++ -std=c++17 -o my_test.exe src/p1.cpp
my_test.exe < tests/p1/inputs/01.in
```

---

## 🗂️ 檔案位置速查

| 檔案       | 位置                      | 您能做什麼 |
| ---------- | ------------------------- | ---------- |
| 您的程式碼 | `src/pX.cpp`              | ✅ 修改    |
| 題目說明   | `problems/pX.md`          | 👁️ 查看    |
| 測試輸入   | `tests/pX/inputs/XX.in`   | 👁️ 查看    |
| 正確輸出   | `tests/pX/outputs/XX.out` | 👁️ 查看    |
| 您的分數   | `build/pX.score`          | 👁️ 查看    |
| 編譯記錄   | `build/pX.compile.log`    | 👁️ 查看    |
| 執行記錄   | `build/pX.run.log`        | 👁️ 查看    |

---

## 📋 每次使用的流程

```
1. 開啟終端機/命令提示字元
   ↓
2. 切換到專案目錄 (cd ...)
   ↓
3. 啟動虛擬環境 (activate)
   ↓
4. 用編輯器開啟 src/pX.cpp
   ↓
5. 寫/修改程式碼
   ↓
6. 儲存檔案
   ↓
7. 執行測試 (python3 run_tests.py)
   ↓
8. 查看結果
   ↓
9. 如果失敗，回到步驟 5
   ↓
10. 全部通過！🎉
```

---

## 🎯 記住這些指令就夠了

### Windows (命令提示字元 cmd)
```cmd
:: 啟動環境
venv\Scripts\activate

:: 測試所有題目
python run_tests.py

:: 測試單一題目
python run_tests.py p1

:: 網頁介面（推薦）
python run_tests.py --gui

:: 關閉虛擬環境
deactivate
```

### Windows (PowerShell)
```powershell
# 啟動環境
venv\Scripts\Activate.ps1

# 其他指令同上（使用 python 而非 python3）
```

### macOS / Linux
```bash
# 啟動環境
source venv/bin/activate

# 測試所有題目
python3 run_tests.py

# 測試單一題目
python3 run_tests.py p1

# 網頁介面（推薦）
python3 run_tests.py --gui

# 關閉虛擬環境
deactivate
```

---

## ✅ 提交作業前的檢查清單

在提交作業前，確認：

- [ ] 所有測試案例都通過（顯示全部 ✅）
- [ ] 得分是滿分
- [ ] 程式碼有適當的註解
- [ ] 沒有使用不允許的函式庫或語法
- [ ] 程式碼符合老師的要求（如命名規則、程式風格等）
- [ ] **確認沒有修改 `src/` 以外的檔案**

---

## 📤 作業繳交流程（GitHub）

本課程使用 **GitHub Classroom** 管理作業繳交和自動評分。

### 第一次使用 Git（初次設定）

如果您從未使用過 Git，請先進行設定：

```bash
# 設定您的姓名和Email（只需要做一次）
git config --global user.name "您的姓名"
git config --global user.email "您的Email"
```

### 作業繳交步驟

#### 方法一：使用網頁介面（最簡單！）

1. **啟動網頁介面**：

   ```bash
   python3 run_tests.py --gui
   ```

2. **執行測試**：點擊「執行所有測試」按鈕，確認全部通過

3. **推送到 GitHub**：

   - 點擊「Push to GitHub」按鈕
   - 閱讀確認視窗的說明
   - 點擊「確認推送」按鈕
   - 等待推送完成
   - 看到「✅ 成功」訊息就完成了！

4. **檢查自動評分**：前往 GitHub repository 查看 Actions 結果

#### 方法二：使用命令列

##### 步驟 1：完成程式碼

確保您的程式通過所有測試：

```bash
# 在本地測試
python3 run_tests.py

# 或使用網頁介面
python3 run_tests.py --gui
```

##### 步驟 2：查看修改的檔案

```bash
# 查看哪些檔案被修改了
git status
```

您應該只會看到 `src/` 目錄下的 `.cpp` 檔案被修改。

⚠️ **如果看到其他檔案被修改，請不要提交它們！**

##### 步驟 3：加入要提交的檔案

```bash
# 加入所有 src/ 目錄下的 .cpp 檔案
git add src/*.cpp

# 或逐一加入特定檔案
git add src/p1.cpp
git add src/p2.cpp
```

**不要使用 `git add .` 或 `git add -A`**，因為可能會加入不該提交的檔案！

##### 步驟 4：提交變更

```bash
# 提交並附上說明訊息
git commit -m "完成 p1 和 p2"

# 或更詳細的說明
git commit -m "修正 p1 的邊界條件處理"
```

##### 步驟 5：推送到 GitHub

```bash
# 推送到您的 GitHub repository
git push origin main
```

如果您的分支名稱是 `master` 而不是 `main`：

```bash
git push origin master
```

##### 步驟 6：檢查自動評分結果

1. 前往您的 GitHub repository 頁面
2. 點擊上方的 **"Actions"** 標籤
3. 查看最新的 workflow 執行結果
4. 綠色 ✅ = 全部通過
5. 紅色 ❌ = 有測試失敗

### 查看詳細測試結果

在 GitHub Actions 頁面：

1. 點擊最新的 workflow run
2. 點擊 "test" job
3. 展開各個步驟查看詳細輸出
4. 捲動到底部查看 **"測試結果"** 和 **"分數統計"**

### 修正錯誤並重新提交

如果測試失敗：

```bash
# 1. 在本地修正程式碼
# 2. 本地測試確認通過
python3 run_tests.py

# 3. 再次提交
git add src/*.cpp
git commit -m "修正測試錯誤"
git push origin main
```

每次 push 都會自動觸發測試，直到全部通過為止。

### 常見 Git 問題

#### Q: 忘記提交訊息怎麼辦？

如果執行 `git commit` 後進入編輯器：

1. 輸入提交訊息
2. 按 `Esc`，然後輸入 `:wq` 並按 Enter（Vim 編輯器）
3. 或按 `Ctrl+X`，然後 `Y`，再按 Enter（Nano 編輯器）

#### Q: Push 被拒絕（rejected）？

```bash
# 先拉取最新的變更
git pull origin main

# 解決衝突（如果有）

# 再次推送
git push origin main
```

#### Q: 不小心加入了不該提交的檔案？

```bash
# 從 staging area 移除
git reset HEAD 檔案名稱

# 重新選擇要提交的檔案
git add src/*.cpp
git commit -m "訊息"
```

#### Q: 想要撤銷上一次的 commit？

```bash
# 撤銷 commit 但保留修改
git reset --soft HEAD~1

# 或完全撤銷（危險！會遺失修改）
git reset --hard HEAD~1
```

### Git 指令速查

```bash
# 查看狀態
git status

# 查看修改內容
git diff

# 查看提交歷史
git log --oneline

# 加入檔案
git add src/*.cpp

# 提交
git commit -m "訊息"

# 推送
git push origin main

# 拉取
git pull origin main
```

### 📋 完整繳交流程總結

```
1. 寫程式 (src/pX.cpp)
   ↓
2. 本地測試 (python3 run_tests.py)
   ↓
3. 確認通過
   ↓
4. git add src/*.cpp
   ↓
5. git commit -m "完成 pX"
   ↓
6. git push origin main
   ↓
7. 到 GitHub 查看 Actions 結果
   ↓
8. 全部通過 ✅ → 完成！
   或 有錯誤 ❌ → 回到步驟 1 修正
```

### ⚠️ 重要注意事項

1. **只提交 src/ 下的 .cpp 檔案**
2. **不要使用 `git add .` 或 `git add -A`**
3. **每次修改都要先在本地測試**
4. **提交訊息要清楚說明做了什麼**
5. **截止日期前確保 GitHub 上的版本是正確的**
6. **不要等到最後一刻才 push**（GitHub 可能會塞車）

### 🎯 截止日期提醒

- GitHub 的提交時間戳記是您 **push 的時間**，不是 commit 的時間
- 如果在截止日期後才 push，會被視為遲交
- 建議在截止日期前幾個小時就完成並 push

---

## 🔗 更多資源

### 詳細文件

- **[INSTALLATION.md](INSTALLATION.md)** - 環境安裝指南（第一次使用必讀）
- **[README.md](README.md)** - 系統維護文件（給 TA/AI 看的）

### 尋求協助

1. **查看本文件的「常見問題」章節**
2. **使用網頁介面查看詳細錯誤訊息**
3. **查看測試案例的輸入和輸出**
4. **詢問同學或助教**
5. **Google 搜尋錯誤訊息**

### 學習 C++

- [C++ Reference](https://cppreference.com/)
- [LeetCode](https://leetcode.com/) - 練習程式題
- [Codeforces](https://codeforces.com/) - 程式競賽

---

## ⚠️ 重要提醒

### 千萬不要做的事

1. ❌ **不要修改 `src/` 以外的任何檔案**
2. ❌ **不要刪除或重新命名測試檔案**
3. ❌ **不要修改 `config/config.yaml`**
4. ❌ **不要抄襲其他同學的程式碼**
5. ❌ **不要在最後一刻才開始寫作業**

### 建議做的事

1. ✅ **早點開始寫作業**
2. ✅ **頻繁測試您的程式**
3. ✅ **仔細閱讀題目說明**
4. ✅ **檢查所有邊界情況**
5. ✅ **寫清楚的註解**
6. ✅ **保持程式碼整潔**

---

祝您寫程式順利！有問題隨時參考文件或詢問助教。💪

**提醒**：早點開始寫作業，不要拖到最後一刻！😊
