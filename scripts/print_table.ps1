param(
  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$Problems
)

if (-not $Problems -or $Problems.Count -eq 0) {
  exit 0
}

$rows = @()
foreach ($p in $Problems) {
  $pass = 0; $total = 0; $g = 0; $t = 0
  if (Test-Path ("build/" + $p + ".cases")) {
    $ct = Get-Content -Raw ("build/" + $p + ".cases")
    $parts = $ct -split '\s+'
    if ($parts.Length -ge 2) { $pass = [int]$parts[0]; $total = [int]$parts[1] }
  }
  if (Test-Path ("build/" + $p + ".score")) {
    $st = Get-Content -Raw ("build/" + $p + ".score")
    $sp = $st -split '\s+'
    if ($sp.Length -ge 2) { $g = [int]$sp[0]; $t = [int]$sp[1] }
  }
  $fail = $total - $pass
  $rows += [pscustomobject]@{ Problem=$p; Pass=$pass; Fail=$fail; Score=('{0}/{1}' -f $g,$t) }
}

$sum_pass = ($rows | Measure-Object -Property Pass -Sum).Sum; if (-not $sum_pass) { $sum_pass = 0 }
$sum_fail = ($rows | Measure-Object -Property Fail -Sum).Sum; if (-not $sum_fail) { $sum_fail = 0 }
$sum_g = 0; $sum_t = 0
foreach ($p in $Problems) {
  if (Test-Path ("build/" + $p + ".score")) {
    $st = Get-Content -Raw ("build/" + $p + ".score")
    $sp = $st -split '\s+'
    if ($sp.Length -ge 2) { $sum_g += [int]$sp[0]; $sum_t += [int]$sp[1] }
  }
}

$rows += [pscustomobject]@{ Problem='total'; Pass=$sum_pass; Fail=$sum_fail; Score=('{0}/{1}' -f $sum_g,$sum_t) }

$w1 = [Math]::Max(8, (('Problem').Length, ($rows | ForEach-Object { ($_.Problem).ToString().Length }) | Measure-Object -Maximum).Maximum)
$w2 = [Math]::Max(10, (('pass_test').Length, ($rows | ForEach-Object { ($_.Pass).ToString().Length }) | Measure-Object -Maximum).Maximum)
$w3 = [Math]::Max(10, (('fail_test').Length, ($rows | ForEach-Object { ($_.Fail).ToString().Length }) | Measure-Object -Maximum).Maximum)
$w4 = [Math]::Max(12, (('score').Length, ($rows | ForEach-Object { ($_.Score).ToString().Length }) | Measure-Object -Maximum).Maximum)

function Rep([int]$n, [string]$ch) { return [string]::new($ch[0], $n) }
$top = '+' + (Rep ($w1+2) '-') + '+' + (Rep ($w2+2) '-') + '+' + (Rep ($w3+2) '-') + '+' + (Rep ($w4+2) '-') + '+'
$sep = $top

$h1='Problem'.PadRight($w1)
$h2='pass_test'.PadLeft($w2)
$h3='fail_test'.PadLeft($w3)
$h4='score'.PadLeft($w4)
Write-Host $top
Write-Host ('| ' + $h1 + ' | ' + $h2 + ' | ' + $h3 + ' | ' + $h4 + ' |')
Write-Host $sep
foreach ($r in $rows) {
  $c1=($r.Problem).ToString().PadRight($w1)
  $c2=($r.Pass).ToString().PadLeft($w2)
  $c3=($r.Fail).ToString().PadLeft($w3)
  $c4=($r.Score).ToString().PadLeft($w4)
  Write-Host ('| ' + $c1 + ' | ' + $c2 + ' | ' + $c3 + ' | ' + $c4 + ' |')
}
Write-Host $top

