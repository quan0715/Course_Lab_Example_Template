@echo off
setlocal enabledelayedexpansion

rem Multi-problem test runner (Windows)
rem Usage:
rem   run_tests.bat           -> auto-discover problems from src\p*.cpp
rem   run_tests.bat p1        -> run only p1

where g++ >NUL 2>&1
if errorlevel 1 (
  echo [FAIL] g++ not found. Please install MinGW-w64 or similar.
  exit /b 1
)

if not exist build mkdir build >NUL 2>&1

set "problem=%~1"

call :maybe_run_one "%problem%"
if not "%problem%"=="" exit /b %errorlevel%

set overall=0
set "PROBLEMS="
for %%F in (src\p*.cpp) do (
  set "name=%%~nF"
  for /f "tokens=1 delims=_" %%A in ("!name!") do set "base=%%A"
  call :add_problem "!base!"
)

if "%PROBLEMS%"=="" (
  echo [FAIL] No problems discovered in src\. Expect files like src\p1.cpp or src\p1_name.cpp
  exit /b 1
)

for %%P in (%PROBLEMS%) do (
  call :run_problem "%%P"
  set /a overall+=!errorlevel!
)

rem Aggregate total score across problems if any .score files exist
set /a overall_g=0
set /a overall_t=0
for %%P in (%PROBLEMS%) do (
  if exist "build\%%P.score" (
    for /f "tokens=1,2" %%a in (build\%%P.score) do (
      for /f %%x in ("%%a") do set /a overall_g+=%%x
      for /f %%y in ("%%b") do set /a overall_t+=%%y
    )
  )
)
if %overall_t% gtr 0 (
  echo [TOTAL] Total Score: %overall_g%/%overall_t%
)

rem Print summary table using PowerShell for alignment
call :print_summary_table "%PROBLEMS%"
exit /b %overall%

goto :eof

:maybe_run_one
set "prob=%~1"
if "%prob%"=="" goto :eof
call :run_problem "%prob%"
exit /b %errorlevel%

:find_source
set "prob=%~1"
set "src="
if exist "src\%prob%.cpp" set "src=src\%prob%.cpp"& goto :found
for %%F in (src\%prob%_*.cpp) do (
  if not defined src (
    set "src=%%F"
  ) else (
    echo ^❌ Multiple sources found for %prob% & echo !src! %%F
    set "src="
    exit /b 2
  )
)
:found
if not defined src exit /b 1
echo !src!
exit /b 0

:run_problem
setlocal enabledelayedexpansion
set "prob=%~1"
for /f "usebackq delims=" %%S in (`call "%~f0" find_source "%prob%"`) do set "src=%%S"
if not defined src (
  echo ===============================
  echo ^❌ No source for %prob%. Expected src\%prob%.cpp or src\%prob%_*.cpp
  endlocal & exit /b 1
)

set "bin=build\%prob%.exe"
echo ===============================
echo [BUILD] Compiling !src!... 
g++ -std=c++17 -O2 "!src!" -o "!bin!" 2> "build\%prob%.compile.log"
if errorlevel 1 (
  echo [FAIL] Compilation failed for %prob%. See build\%prob%.compile.log
  rem On compile failure, record all tests as failed for summary/score
  call :count_inputs "%prob%" cases
  call :get_problem_points "%prob%" points
  >"build\%prob%.cases" echo 0 !cases!
  >"build\%prob%.score" echo 0 !points!
  endlocal & exit /b 1
)
echo [PASS] Compilation successful
echo ===============================

set "base_dir=tests\%prob%"
if not exist "%base_dir%\inputs" goto notests
if not exist "%base_dir%\outputs" goto notests

set total=0
set passed=0
for %%f in ("%base_dir%\inputs\*.in") do (
  set /a total+=1
  for %%~nf in ("%%f") do set "base=%%~nf"
  set "expected=%base_dir%\outputs\!base!.out"
  if not exist "!expected!" (
    echo [FAIL] %prob%:!base!.in ^(missing expected !base!.out^)
    goto :continue_case
  )
  cmd /c ""%bin%" < "%%f" > build\tmp.raw" 1> build\%prob%.run.log 2>&1
  if errorlevel 1 (
    echo [FAIL] %prob%:!base!.in ^(program exited with error^)
    echo -- stderr/stdout (first 5 lines) --
    powershell -NoProfile -Command "Get-Content -LiteralPath 'build/%prob%.run.log' -TotalCount 5" 2>NUL
    goto :continue_case
  )
  rem Normalize CRLF in both expected and actual
  powershell -NoProfile -Command "(Get-Content -Raw '!expected!').Replace('`r','') | Set-Content -NoNewline 'build/expect.norm'"
  powershell -NoProfile -Command "(Get-Content -Raw 'build/tmp.raw').Replace('`r','') | Set-Content -NoNewline 'build/actual.norm'"
  fc /N /W "build\expect.norm" "build\actual.norm" >NUL 2>&1
  if errorlevel 1 (
    echo [FAIL] %prob%:!base!.in
    echo ----- Expected -----
    type "!expected!"
    echo ----- Got -----
    type build\tmp.raw
    echo ----- Diff -----
    fc /N /W "build\expect.norm" "build\actual.norm"
  ) else (
    echo [PASS] %prob%:!base!.in
    set /a passed+=1
  )
  :continue_case
)

echo.
rem Scoring and records
call :get_problem_points "%prob%" points
set /a gained=0
if %passed%==%total% set /a gained=%points%
>"build\%prob%.score" echo %gained% %points%
>"build\%prob%.cases" echo %passed% %total%
echo [RESULT] %prob% Result: !passed!/!total! tests passed ^| Score: %gained%/%points%
echo ===============================

set /a rc=total-passed
endlocal & exit /b %rc%

:add_problem
set "cand=%~1"
if "%cand%"=="" exit /b 0
for %%X in (%PROBLEMS%) do if /i "%%X"=="%cand%" exit /b 0
if "%PROBLEMS%"=="" (
  set "PROBLEMS=%cand%"
) else (
  set "PROBLEMS=%PROBLEMS% %cand%"
)
exit /b 0

:notests
echo ^❌ No tests found for %prob%. Expected tests\%prob%\inputs and tests\%prob%\outputs
endlocal & exit /b 1

:get_problem_points
setlocal
set "prob=%~1"
set "points="
for /f "usebackq tokens=1,2 delims==" %%A in (`findstr /b /c:"problem.%prob%=" config\points.conf 2^>NUL`) do (
  if "%%A"=="problem.%prob%" set "points=%%B"
)
if not defined points set "points=100"
endlocal & set "%~2=%points%" & exit /b 0

:count_inputs
setlocal
set "prob=%~1"
set /a cnt=0
for %%f in ("tests\%prob%\inputs\*.in") do set /a cnt+=1
endlocal & set "%~2=%cnt%" & exit /b 0

:print_summary_table
setlocal
set "LIST=%~1"
set "top=+--------+------------+------------+--------------+"
echo Summary Table
echo %top%
powershell -NoProfile -Command "$fmt='| {0,-8} | {1,10} | {2,10} | {3,12} |'; Write-Host ($fmt -f 'Problem','pass_test','fail_test','score')"
echo +--------+------------+------------+--------------+
set /a sum_pass=0
set /a sum_fail=0
set /a sum_g=0
set /a sum_t=0
for %%P in (%LIST%) do (
  set pass=0
  set total=0
  set g=0
  set t=0
  if exist "build\%%P.cases" for /f "tokens=1,2" %%a in (build\%%P.cases) do (set pass=%%a & set total=%%b)
  if exist "build\%%P.score" for /f "tokens=1,2" %%a in (build\%%P.score) do (set g=%%a & set t=%%b)
  set /a fail=total-pass
  set "score=%g%/%t%"
  powershell -NoProfile -Command "$fmt='| {0,-8} | {1,10} | {2,10} | {3,12} |'; Write-Host ($fmt -f '%P',%pass%,%fail%,'%g%/%t%')"
  set /a sum_pass+=pass
  set /a sum_fail+=fail
  set /a sum_g+=g
  set /a sum_t+=t
)
echo +--------+------------+------------+--------------+
powershell -NoProfile -Command "$fmt='| {0,-8} | {1,10} | {2,10} | {3,12} |'; Write-Host ($fmt -f 'total',%sum_pass%,%sum_fail%,'%sum_g%/%sum_t%')"
echo %top%
endlocal & exit /b 0
