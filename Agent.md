Agent.md
🎯 目標

提供一組 C++ 多題目（p1, p2, …）的自動測試腳本，讓學生在本地端驗證各題正確性；同時支援題目檔名規則「pX.cpp」與「pX_題目名稱.cpp」皆視為題目 pX。

📂 專案結構（多題目）
assignment-X/
├─ src/
│  ├─ p1.cpp              # 或 p1_problem_name.cpp（兩者其一即可）
│  ├─ p2_sum.cpp          # 範例：p2_* 視為 p2
│  └─ ...
├─ tests/
│  ├─ p1/
│  │  ├─ inputs/
│  │  │  ├─ 01.in
│  │  │  └─ 02.in
│  │  └─ outputs/
│  │     ├─ 01.out
│  │     └─ 02.out
│  ├─ p2/
│  │  ├─ inputs/
│  │  └─ outputs/
│  └─ ...
├─ run_tests.sh           # 測試腳本 (macOS/Linux)
└─ run_tests.bat          # 測試腳本 (Windows)

🧭 題目檔名規則（重要）
- pX.cpp 與 pX_*.cpp 均視為題目 pX。若兩者同時存在，優先使用 pX.cpp。
- 若存在多個 pX_*.cpp（不含 pX.cpp），會視為歧義並報錯，請保留唯一檔案。

🛠️ 腳本行為
run_tests.sh（macOS/Linux）與 run_tests.bat（Windows）：
- `run_tests.sh p1`：只編譯執行題目 p1，測試 `tests/p1/inputs/*.in` 與 `tests/p1/outputs/*.out`。
- 無參數時：自動偵測 `tests/*/inputs` 作為多題目根目錄，依序測試所有題目並彙總退出碼（等於所有題目失敗用例數）。
- 編譯：`g++ -std=c++17 -O2`，成功/失敗皆會顯示清楚訊息與 log 位置。
- 比對：逐一執行 `.in`，與對應 `.out` 精準比對；失敗時列出 Expected/Got 各前 5 行、EOL 狀態（是否以換行結尾）、以及 unified diff（前 20 行）。

🧭 題目偵測與測資資料夾
- 題目以 `src` 目錄下檔名為準：`pX.cpp` 或 `pX_*.cpp` → 題目代號為 `pX`。
- 測資放在 `tests/pX/inputs/*.in` 與 `tests/pX/outputs/*.out`。
- 不再支援舊版單一題目結構 `tests/inputs`、`tests/outputs`。

📈 配分設定（config）
- 檔案：`config/points.conf`
- 格式：
  - `problem.p1=50` 表示題目 p1 總分 50 分。
  - `case.p1.01=20` 表示 p1 的測資 `01` 配 20 分（覆蓋同題目下的平均分配）。
- 分配邏輯：
  - 每題總分 = 各測資分數總和。
  - 未設定覆蓋的測資，平均分配剩餘分數；若有餘數，依測資名稱排序，前幾個各+1。

🎨 範例輸出（節錄）
===============================
🔧 Compiling src/p1.cpp...
✅ Compilation successful!
===============================
✅ [PASS] p1:01.in (+20/20)
❌ [FAIL] p1:02.in (+0/20)
----- Expected (first 5 lines) -----
...
----- Got (first 5 lines) -----
...
EOL: expected=yes, got=no
----- Diff (first 20 lines) -----
...
📊 p1 Result: 1/2 tests passed | Score: 20/50
===============================

📦 使用方式
- mac/Linux：
  - 全部題目：`./run_tests.sh`
  - 指定題目：`./run_tests.sh p1`
- Windows：
  - 全部題目：`run_tests.bat`
  - 指定題目：`run_tests.bat p1`
