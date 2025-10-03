@echo off
setlocal enabledelayedexpansion
rem Flat for-loop test runner for p1 (all testcases, no functions)

echo [LOG] Checking for g++...
where g++ >NUL 2>&1
if errorlevel 1 (
  echo [FAIL] g++ not found.
  exit /b 1
)

echo [LOG] Creating build directory...
if not exist build mkdir build >NUL 2>&1

echo [LOG] Compiling src/p1.cpp...
g++ -std=c++17 -O2 src/p1.cpp -o build/p1.exe 2> build/p1.compile.log
if errorlevel 1 (
  echo [FAIL] Compilation failed. See build/p1.compile.log
  exit /b 1
)
echo [LOG] Compilation successful.

echo [LOG] Running tests for p1...
set passed=0
set total=0

for %%f in (tests\p1\inputs\*.in) do (
  echo [LOG] Processing test: %%~nf
  set /a total+=1
  set "infile=%%f"
  set "basename=%%~nf"
  set "outfile=tests\p1\outputs\!basename!.out"
  set "tmpfile=build\tmp_!basename!.out"
  
  echo [LOG] Running build/p1.exe ^< !infile! ^> !tmpfile!
  build\p1.exe < "!infile!" > "!tmpfile!" 2>&1
  if errorlevel 1 (
    echo [FAIL] p1:!basename!.in ^(program exited with error^)
  ) else (
    echo [LOG] Comparing !tmpfile! with !outfile!...
    fc /N /W "!tmpfile!" "!outfile!" >NUL 2>&1
    if errorlevel 1 (
      echo [FAIL] p1:!basename!.in ^(output mismatch^)
      echo ----- Expected -----
      type "!outfile!"
      echo ----- Got -----
      type "!tmpfile!"
    ) else (
      echo [PASS] p1:!basename!.in
      set /a passed+=1
    )
  )
)

echo [LOG] Tests completed: !passed!/!total! passed
if !passed! equ !total! (
  echo [RESULT] All tests passed!
  exit /b 0
) else (
  echo [RESULT] Some tests failed.
  exit /b 1
)
