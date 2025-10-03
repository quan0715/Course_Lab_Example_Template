@echo off
setlocal enabledelayedexpansion
rem Multi-problem, multi-case test runner (flat for-loops, no functions/call, Windows batch)
rem Auto-discover all p*.cpp in src/, compile each, run all test cases per problem, display summary
echo [LOG] Checking for g++...
where g++ >NUL 2>&1
if errorlevel 1 (
  echo ❌ FAIL g++ not found. Please install MinGW-w64 or similar.
  exit /b 1
)
echo [LOG] Creating build directory...
if not exist build mkdir build >NUL 2>&1
rem ===== Phase 1: Discover all problems from src\p*.cpp =====
echo [LOG] Discovering problems from src\p*.cpp...
set "PROBLEMS="
for %%F in (src\p*.cpp) do (
  set "name=%%~nF"
  rem Extract base name (before underscore if exists)
  for /f "tokens=1 delims=_" %%A in ("!name!") do set "base=%%A"
  rem Add to PROBLEMS list (avoid duplicates)
  set "found=0"
  for %%P in (!PROBLEMS!) do if "%%P"=="!base!" set "found=1"
  if "!found!"=="0" (
    if "!PROBLEMS!"=="" (
      set "PROBLEMS=!base!"
    ) else (
      set "PROBLEMS=!PROBLEMS! !base!"
    )
  )
)
if "!PROBLEMS!"=="" (
  echo ❌ FAIL No problems discovered in src\. Expect files like src\p1.cpp or src\p1_name.cpp
  exit /b 1
)
echo [LOG] Discovered problems: !PROBLEMS!
echo.
rem ===== Phase 2: For each problem, compile and run all test cases =====
for %%P in (!PROBLEMS!) do (
  echo ===============================
  echo 🔧 BUILD Problem: %%P
  
  set "skip_this=0"
  
  rem Find source file for %%P
  set "src="
  if exist "src\%%P.cpp" set "src=src\%%P.cpp"
  if "!src!"=="" (
    rem Try src\%%P_*.cpp pattern
    for %%S in (src\%%P_*.cpp) do (
      if "!src!"=="" (
        set "src=%%S"
      ) else (
        echo ❌ FAIL Multiple sources found for %%P: !src! and %%S
        set "src="
        set "skip_this=1"
      )
    )
  )
  
  if "!src!"=="" (
    echo ❌ FAIL No source for %%P. Expected src\%%P.cpp or src\%%P_*.cpp
    echo 0 0 > "build\%%P.cases"
    echo 0 100 > "build\%%P.score"
    set "skip_this=1"
  )
  
  if "!skip_this!"=="0" (
    echo [LOG] Compiling !src!...
    g++ -std=c++17 -O2 "!src!" -o "build\%%P.exe" 2> "build\%%P.compile.log"
    if errorlevel 1 (
      echo ⚠️  Compilation failed for %%P. See build\%%P.compile.log
      rem Count test cases for failure record
      set /a cases_count=0
      if exist "tests\%%P\inputs" (
        for %%T in (tests\%%P\inputs\*.in) do set /a cases_count+=1
      )
      echo 0 !cases_count! > "build\%%P.cases"
      rem Get points from config (default 100)
      set "points=100"
      if exist "config\points.conf" (
        for /f "tokens=1,2 delims==" %%A in ('findstr /b /c:"problem.%%P=" config\points.conf 2^>NUL') do (
          if "%%A"=="problem.%%P" set "points=%%B"
        )
      )
      echo 0 !points! > "build\%%P.score"
      set "skip_this=1"
    )
  )
  
  if "!skip_this!"=="0" (
    echo ✅ PASS Compilation successful
    echo ===============================
    
    rem Check test directories exist
    if not exist "tests\%%P\inputs" (
      echo ❌ FAIL No tests found for %%P. Expected tests\%%P\inputs and tests\%%P\outputs
      echo 0 0 > "build\%%P.cases"
      set "points=100"
      if exist "config\points.conf" (
        for /f "tokens=1,2 delims==" %%A in ('findstr /b /c:"problem.%%P=" config\points.conf 2^>NUL') do (
          if "%%A"=="problem.%%P" set "points=%%B"
        )
      )
      echo 0 !points! > "build\%%P.score"
      set "skip_this=1"
    )
    
    if "!skip_this!"=="0" (
      if not exist "tests\%%P\outputs" (
        echo ❌ FAIL No tests found for %%P. Expected tests\%%P\inputs and tests\%%P\outputs
        echo 0 0 > "build\%%P.cases"
        set "points=100"
        if exist "config\points.conf" (
          for /f "tokens=1,2 delims==" %%A in ('findstr /b /c:"problem.%%P=" config\points.conf 2^>NUL') do (
            if "%%A"=="problem.%%P" set "points=%%B"
          )
        )
        echo 0 !points! > "build\%%P.score"
        set "skip_this=1"
      )
    )
    
    if "!skip_this!"=="0" (
      rem Run all test cases for %%P
      set /a total=0
      set /a passed=0
      
      for %%f in (tests\%%P\inputs\*.in) do (
        set /a total+=1
        set "basename=%%~nf"
        set "infile=%%f"
        set "expected=tests\%%P\outputs\!basename!.out"
        set "tmpfile=build\tmp_!basename!.out"
        
        if not exist "!expected!" (
          echo ❌ FAIL %%P:!basename!.in ^(missing expected !basename!.out^)
        ) else (
          cmd /c ""build\%%P.exe" < "%%f" > "!tmpfile!"" 1> "build\%%P.run.log" 2>&1
          if errorlevel 1 (
            echo ❌ FAIL %%P:!basename!.in ^(program exited with error^)
          ) else (
            rem Normalize line endings and compare
            powershell -NoProfile -Command "(Get-Content -Raw '!expected!').Replace('`r','') | Set-Content -NoNewline 'build\expect.norm'" 2>NUL
            powershell -NoProfile -Command "(Get-Content -Raw '!tmpfile!').Replace('`r','') | Set-Content -NoNewline 'build\actual.norm'" 2>NUL
            fc /N /W "build\expect.norm" "build\actual.norm" >NUL 2>&1
            if errorlevel 1 (
              echo ❌ FAIL %%P:!basename!.in
            ) else (
              echo ✅ PASS %%P:!basename!.in
              set /a passed+=1
            )
          )
        )
      )
      
      rem Get problem points from config
      set "points=100"
      if exist "config\points.conf" (
        for /f "tokens=1,2 delims==" %%A in ('findstr /b /c:"problem.%%P=" config\points.conf 2^>NUL') do (
          if "%%A"=="problem.%%P" set "points=%%B"
        )
      )
      
      rem Calculate score (all-or-nothing: full points if all tests pass)
      set /a gained=0
      if !passed! equ !total! set /a gained=!points!
      
      echo.
      echo 📄 RESULT %%P Result: !passed!/!total! tests passed ^| Score: !gained!/!points!
      echo ===============================
      echo.
      
      rem Save results
      echo !passed! !total! > "build\%%P.cases"
      echo !gained! !points! > "build\%%P.score"
    )
  )
)
rem ===== Phase 3: Calculate and display summary =====
set /a overall_g=0
set /a overall_t=0
set /a sum_pass=0
set /a sum_fail=0
for %%P in (!PROBLEMS!) do (
  if exist "build\%%P.score" (
    for /f "tokens=1,2" %%a in (build\%%P.score) do (
      set /a overall_g+=%%a
      set /a overall_t+=%%b
    )
  )
  if exist "build\%%P.cases" (
    for /f "tokens=1,2" %%a in (build\%%P.cases) do (
      set /a sum_pass+=%%a
      set /a sum_fail+=%%b
    )
  )
)
set /a sum_fail=!sum_fail!-!sum_pass!
if !overall_t! gtr 0 (
  echo 📊 TOTAL Total Score: !overall_g!/!overall_t!
  echo.
)
rem Print summary table using PowerShell with dynamic widths (ASCII borders)
echo Summary Table
powershell -NoProfile -Command "$list='!PROBLEMS!'.Split(' ',[StringSplitOptions]::RemoveEmptyEntries); $rows=@(); foreach($p in $list){ $pass=0;$total=0;$g=0;$t=0; if(Test-Path "build/$p.cases"){ $ct=(Get-Content -Raw "build/$p.cases"); $parts=$ct -split '\s+'; if($parts.Length -ge 2){ $pass=[int]$parts[0]; $total=[int]$parts[1] } } if(Test-Path "build/$p.score"){ $st=(Get-Content -Raw "build/$p.score"); $sp=$st -split '\s+'; if($sp.Length -ge 2){ $g=[int]$sp[0]; $t=[int]$sp[1] } } $fail=$total-$pass; $rows += [pscustomobject]@{ Problem=$p; Pass=$pass; Fail=$fail; Score=(''{0}/{1}'' -f $g,$t) } } $sum_pass=($rows|Measure-Object Pass -Sum).Sum; if(-not $sum_pass){$sum_pass=0}; $sum_fail=($rows|Measure-Object Fail -Sum).Sum; if(-not $sum_fail){$sum_fail=0}; $sum_g=0;$sum_t=0; foreach($p in $list){ if(Test-Path "build/$p.score"){ $st=(Get-Content -Raw "build/$p.score"); $sp=$st -split '\s+'; if($sp.Length -ge 2){ $sum_g += [int]$sp[0]; $sum_t += [int]$sp[1] } } } $rows += [pscustomobject]@{ Problem='total'; Pass=$sum_pass; Fail=$sum_fail; Score=(''{0}/{1}'' -f $sum_g,$sum_t) }; $w1=[Math]::Max(8, ((''Problem'').Length, ($rows|%{($_.Problem).ToString().Length}) | Measure-Object -Maximum).Maximum); $w2=[Math]::Max(10, ((''pass_test'').Length, ($rows|%{($_.Pass).ToString().Length}) | Measure-Object -Maximum).Maximum); $w3=[Math]::Max(10, ((''fail_test'').Length, ($rows|%{($_.Fail).ToString().Length}) | Measure-Object -Maximum).Maximum); $w4=[Math]::Max(12, ((''score'').Length, ($rows|%{($_.Score).ToString().Length}) | Measure-Object -Maximum).Maximum); function Rep($n,$ch){return ($ch * $n)} $top='+'+(Rep ($w1+2) '-')+'+'+(Rep ($w2+2) '-')+'+'+(Rep ($w3+2) '-')+'+'+(Rep ($w4+2) '-')+'+'; $sep=$top; $h1='Problem'.PadRight($w1); $h2='pass_test'.PadLeft($w2); $h3='fail_test'.PadLeft($w3); $h4='score'.PadLeft($w4); Write-Host $top; Write-Host ('| '+$h1+' | '+$h2+' | '+$h3+' | '+$h4+' |'); Write-Host $sep; foreach($r in $rows){ $c1=($r.Problem).ToString().PadRight($w1); $c2=($r.Pass).ToString().PadLeft($w2); $c3=($r.Fail).ToString().PadLeft($w3); $c4=($r.Score).ToString().PadLeft($w4); Write-Host ('| '+$c1+' | '+$c2+' | '+$c3+' | '+$c4+' |') }; Write-Host $top"
rem Exit with failure count
set /a exit_code=!sum_fail!
if !exit_code! gtr 0 (
  exit /b !exit_code!
) else (
  exit /b 0
)
