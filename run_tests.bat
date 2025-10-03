@echo off
setlocal enabledelayedexpansion

rem Minimal test runner for p1 only (CI diagnosis)

echo [LOG] Checking for g++...
where g++ >NUL 2>&1
if errorlevel 1 (
  echo [FAIL] g++ not found.
  exit /b 1
)

if not exist build mkdir build >NUL 2>&1

echo [LOG] Compiling src/p1.cpp...
g++ -std=c++17 -O2 src/p1.cpp -o build/p1.exe 2> build/p1.compile.log
if errorlevel 1 (
  echo [FAIL] Compilation failed. See build/p1.compile.log
  exit /b 1
)
echo [LOG] Compilation successful.

echo [LOG] Running build/p1.exe with tests/p1/inputs/01.in...
build\p1.exe < tests\p1\inputs\01.in > build\tmp.out 2>&1
if errorlevel 1 (
  echo [FAIL] Program exited with error.
  exit /b 1
)
echo [LOG] Program ran successfully.

echo [LOG] Comparing output with tests/p1/outputs/01.out...
fc /N /W build\tmp.out tests\p1\outputs\01.out >NUL 2>&1
if errorlevel 1 (
  echo [FAIL] Output mismatch.
  echo ----- Expected -----
  type tests\p1\outputs\01.out
  echo ----- Got -----
  type build\tmp.out
  exit /b 1
)
echo [PASS] Test passed.
exit /b 0
