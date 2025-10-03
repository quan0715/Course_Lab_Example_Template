#!/usr/bin/env bash

set -u

SEP="========================================================"
CONFIG_FILE="config/points.conf"

# Color handling: --color/--no-color flags and NO_COLOR/FORCE_COLOR env
color_mode="never"
while [ $# -gt 0 ]; do
  case "$1" in
    --color) color_mode="always"; shift ;;
    --no-color) color_mode="never"; shift ;;
    --) shift; break ;;
    --*) echo "Unknown option: $1" >&2; exit 2 ;;
    *) break ;;
  esac
done

# ANSI colors (enabled only when supported)
enable_colors=false
if [ "$color_mode" = "always" ] || [ -n "${FORCE_COLOR:-}" ]; then
  enable_colors=true
elif [ "$color_mode" = "never" ] || [ -n "${NO_COLOR:-}" ]; then
  enable_colors=false
else
  if [ -t 1 ] && [ "${TERM:-}" != "dumb" ]; then
    if command -v tput >/dev/null 2>&1; then
      if [ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]; then
        enable_colors=true
      fi
    else
      enable_colors=true
    fi
  fi
fi

if $enable_colors; then
  RED="\033[31m"; GREEN="\033[32m"; YELLOW="\033[33m"; BLUE="\033[34m"; CYAN="\033[36m"; BOLD="\033[1m"; RESET="\033[0m"
else
  RED=""; GREEN=""; YELLOW=""; BLUE=""; CYAN=""; BOLD=""; RESET=""
fi

# Friendly, high-contrast prefixes with emojis
PASS_PREFIX="${GREEN}✅ PASS${RESET}"
FAIL_PREFIX="${RED}❌ FAIL${RESET}"
BUILD_PREFIX="${BLUE}🔧 BUILD${RESET}"
RESULT_PREFIX="${BOLD}📄 RESULT${RESET}"
TOTAL_PREFIX="${BOLD}📊 TOTAL${RESET}"
CONFIG_FILE="config/points.conf"

# --- Helpers for scoring and diffs ---
is_integer() {
  case "$1" in
    '' ) return 1 ;;
    *[!0-9]* ) return 1 ;;
    * ) return 0 ;;
  esac
}

cfg_get() {
  local key="$1"
  if [ -f "$CONFIG_FILE" ]; then
    awk -F= -v k="$key" 'BEGIN{IGNORECASE=0} $1==k {print $2; exit}' "$CONFIG_FILE"
  fi
}

get_problem_points() {
  local prob="$1"
  local v
  v=$(cfg_get "problem.${prob}")
  if is_integer "$v"; then echo "$v"; else echo 100; fi
}

get_case_points() {
  local prob="$1" base="$2"
  local v
  v=$(cfg_get "case.${prob}.${base}")
  if is_integer "$v"; then echo "$v"; fi
}

override_points() {
  local base="$1" list="$2"
  for tok in $list; do
    local k=${tok%%:*}
    local val=${tok#*:}
    if [ "$k" = "$base" ]; then echo "$val"; return 0; fi
  done
  return 1
}

eol_state() {
  local f="$1"
  if [ ! -e "$f" ]; then echo "n/a"; return; fi
  if [ ! -s "$f" ]; then echo "empty"; return; fi
  local last
  last=$(tail -c1 "$f")
  if [ "$last" = $'\n' ]; then echo "yes"; else echo "no"; fi
}

preview5() {
  local f="$1"
  if [ -e "$f" ]; then
    awk 'NR<=5{print $0 " $"} NR==6{exit}' "$f"
  else
    echo "(missing)"
  fi
}

# Colorize unified diff when colors are enabled
colorize_diff() {
  if $enable_colors; then
    awk -v red="$RED" -v green="$GREEN" -v yellow="$YELLOW" -v blue="$BLUE" -v bold="$BOLD" -v reset="$RESET" '
      /^@@/ { print bold blue $0 reset; next }
      /^\+\+\+|^---/ { print yellow $0 reset; next }
      /^\+/ && !/^\+\+\+/ { print green $0 reset; next }
      /^-/ && !/^---/ { print red $0 reset; next }
      { print }
    '
  else
    cat
  fi
}

if ! command -v g++ >/dev/null 2>&1; then
  printf '%b\n' "${FAIL_PREFIX} g++ not found. Please install a C++ compiler (g++)."
  exit 1
fi

mkdir -p build

# Header banner (non-intrusive, no behavior change)
printf '%b\n' "${BLUE}${BOLD}────────────────────────────────────────────────────────${RESET}"
printf '%b\n' "${BOLD}🧪 Lab Test Runner${RESET}"
printf '%b\n' "📁 Root   : ${CYAN}$(pwd)${RESET}"
printf '%b\n' "📦 Results: ${CYAN}build${RESET}"
printf '%b\n' "${BLUE}${BOLD}────────────────────────────────────────────────────────${RESET}"

problem="${1:-}"

find_source() {
  local prob="$1"
  local src=""
  if [ -f "src/${prob}.cpp" ]; then
    src="src/${prob}.cpp"
  else
    # match first src/${prob}_*.cpp if exactly one
    shopt -s nullglob
    local matches=(src/${prob}_*.cpp)
    shopt -u nullglob
    if [ ${#matches[@]} -eq 1 ]; then
      src="${matches[0]}"
    elif [ ${#matches[@]} -gt 1 ]; then
      echo "❌ Multiple sources found for ${prob}: ${matches[*]}" >&2
      return 2
    fi
  fi
  if [ -z "$src" ]; then
    echo "" # empty means not found
  else
    echo "$src"
  fi
}

run_problem() {
  local prob="$1"
  local src
  src="$(find_source "$prob")"

  if [ -z "$src" ]; then
    echo "$SEP"
    echo "❌ No source for ${prob}. Expected src/${prob}.cpp or src/${prob}_*.cpp"
    return 1
  fi

  local bin="build/${prob}"
  echo "$SEP"
  printf '%b\n' "${BUILD_PREFIX} Compiling ${src}..."
  if ! g++ -std=c++17 -O2 "$src" -o "$bin" 2> "build/${prob}.compile.log"; then
    printf '%b\n' "${FAIL_PREFIX} Compilation failed for ${prob}. See build/${prob}.compile.log"
    # On compile failure, if tests exist, record them as failed so summary aligns
    local base_dir_cf="tests/${prob}"
    local cf_cases=0
    if [ -d "${base_dir_cf}/inputs" ]; then
      shopt -s nullglob
      for f in "${base_dir_cf}/inputs"/*.in; do [ -e "$f" ] || continue; cf_cases=$((cf_cases+1)); done
      shopt -u nullglob
    fi
    echo "0 ${cf_cases}" > "build/${prob}.cases"
    local total_points_cf
    total_points_cf=$(get_problem_points "$prob")
    echo "0 ${total_points_cf}" > "build/${prob}.score"
    return 1
  fi
  printf '%b\n' "${PASS_PREFIX} Compilation successful"
  echo "$SEP"

  local base_dir="tests/${prob}"
  if [ ! -d "${base_dir}/inputs" ] || [ ! -d "${base_dir}/outputs" ]; then
    printf '%b\n' "${FAIL_PREFIX} No tests found for ${prob}. Expected tests/${prob}/inputs and tests/${prob}/outputs"
    return 1
  fi

  # Build input list and case names (stable order)
  shopt -s nullglob
  local inputs_list=""
  local cases=""
  local count=0
  for f in "${base_dir}/inputs"/*.in; do
    [ -e "$f" ] || continue
    inputs_list+="$f
"
    local base
    base="$(basename "$f" .in)"
    cases+="$base
"
    count=$((count+1))
  done
  shopt -u nullglob

  if [ $count -eq 0 ]; then
    printf '%b\n' "${FAIL_PREFIX} No input tests found for ${prob} in ${base_dir}/inputs/*.in"
    return 1
  fi

  # Scoring: full points only if all cases pass
  local total_points
  total_points=$(get_problem_points "$prob")
  local total=0
  local passed=0

  # Iterate again in order to run tests
  while IFS= read -r infile; do
    [ -n "$infile" ] || continue
    total=$((total + 1))
    local base expected
    base="$(basename "$infile" .in)"
    expected="${base_dir}/outputs/${base}.out"

    if [ ! -f "$expected" ]; then
      printf '%b\n' "${FAIL_PREFIX} ${prob}:${base}.in (missing expected ${base}.out)"
      continue
    fi

    if "$bin" < "$infile" > build/tmp.out 2> "build/${prob}.run.log"; then :; else
      echo "${FAIL_PREFIX} ${prob}:${base}.in (program exited with error)"
      echo "-- stderr (first 5 lines) --"
      head -n 5 "build/${prob}.run.log" || true
      continue
    fi

    if diff -q "$expected" build/tmp.out >/dev/null 2>&1; then
      printf '%b\n' "${PASS_PREFIX} ${prob}:${base}.in"
      passed=$((passed + 1))
    else
      printf '%b\n' "${FAIL_PREFIX} ${prob}:${base}.in"
      printf '%b\n' "${YELLOW}----- Expected -----${RESET}"
      cat "$expected"
      printf '%b\n' "${YELLOW}----- Got -----${RESET}"
      cat build/tmp.out
      printf '%b\n' "${BLUE}${BOLD}EOL:${RESET} expected=$(eol_state "$expected"), got=$(eol_state build/tmp.out)"
      printf '%b\n' "${YELLOW}----- Diff -----${RESET}"
      diff -u --label expected --label got "$expected" build/tmp.out | colorize_diff
    fi
  done <<EOF
${inputs_list}
EOF

  echo
  local gained=0
  if [ $passed -eq $total ]; then gained=$total_points; fi
  printf '%b\n' "${RESULT_PREFIX} ${prob} Result: ${passed}/${total} tests passed | Score: ${gained}/${total_points}"
  echo "${gained} ${total_points}" > "build/${prob}.score"
  echo "${passed} ${total}" > "build/${prob}.cases"
  echo "$SEP"

  return $(( total - passed ))
}

if [ -n "$problem" ]; then
  # Run a specific problem
  run_problem "$problem"; rc=$?
  # Single-problem summary table (dynamic widths + proper borders)
  printf '%b\n' "${BOLD}Summary Table${RESET}"
  # Compute widths based on header and data
  h1="Problem"; h2="pass_test"; h3="fail_test"; h4="score"
  name_w=${#h1}; pass_w=${#h2}; fail_w=${#h3}; score_w=${#h4}
  # Defaults/min widths
  [ $name_w  -lt 8 ] && name_w=8
  [ $pass_w  -lt 10 ] && pass_w=10
  [ $fail_w  -lt 10 ] && fail_w=10
  [ $score_w -lt 12 ] && score_w=12

  pass=0; total=0; g=0; t=0
  if [ -f "build/${problem}.cases" ]; then read -r pass total < "build/${problem}.cases" || true; fi
  if [ -f "build/${problem}.score" ]; then read -r g t < "build/${problem}.score" || true; fi
  if ! is_integer "$pass"; then pass=0; fi
  if ! is_integer "$total"; then total=0; fi
  if ! is_integer "$g"; then g=0; fi
  if ! is_integer "$t"; then t=0; fi
  fail=$(( total - pass ))
  score_str="$g/$t"
  # Adjust score width if necessary
  [ ${#score_str} -gt $score_w ] && score_w=${#score_str}

  # Helper to repeat a character N times
  rep() { local n=$1 ch=$2; local s=""; while [ $n -gt 0 ]; do s="$s$ch"; n=$((n-1)); done; printf '%s' "$s"; }

  # Build borders with +2 padding per column (spaces inside cell)
  top="┌$(rep $((name_w+2)) '─')┬$(rep $((pass_w+2)) '─')┬$(rep $((fail_w+2)) '─')┬$(rep $((score_w+2)) '─')┐"
  sep="├$(rep $((name_w+2)) '─')┼$(rep $((pass_w+2)) '─')┼$(rep $((fail_w+2)) '─')┼$(rep $((score_w+2)) '─')┤"
  bot="└$(rep $((name_w+2)) '─')┴$(rep $((pass_w+2)) '─')┴$(rep $((fail_w+2)) '─')┴$(rep $((score_w+2)) '─')┘"

  printf '%s\n' "$top"
  printf '│ %-*s │ %*s │ %*s │ %*s │\n' "$name_w" "$h1" "$pass_w" "$h2" "$fail_w" "$h3" "$score_w" "$h4"
  printf '%s\n' "$sep"
  printf '│ %-*s │ %*d │ %*d │ %*s │\n' "$name_w" "$problem" "$pass_w" "$pass" "$fail_w" "$fail" "$score_w" "$score_str"
  printf '%s\n' "$sep"
  printf '│ %-*s │ %*d │ %*d │ %*s │\n' "$name_w" "total" "$pass_w" "$pass" "$fail_w" "$fail" "$score_w" "$score_str"
  printf '%s\n' "$bot"
  echo "$SEP"
  printf '%b\n' "${BLUE}${BOLD}────────────────────────────────────────────────────────${RESET}"
  exit $rc
else
  # Discover problems by scanning src for p*.cpp or p*_* .cpp (robust w/ set -u)
  shopt -s nullglob
  problems=""
  any=0
  for f in src/p*.cpp; do
    any=1
    name="$(basename "$f" .cpp)"
    base="${name%%_*}"
    case " $problems " in
      *" $base "*) : ;; # already in list
      *) problems+=" $base" ;;
    esac
  done
  shopt -u nullglob

  if [ $any -eq 0 ]; then
    echo "❌ No problems discovered in src/. Expect files like src/p1.cpp or src/p1_name.cpp"
    exit 1
  fi

  overall_fail=0
  overall_scored=0
  overall_total=0
  for prob in $problems; do
    run_problem "$prob"; rc=$?
    if [ $rc -ne 0 ]; then
      overall_fail=$((overall_fail + rc))
    fi
    if [ -f "build/${prob}.score" ]; then
      read -r g t < "build/${prob}.score" || true
      if is_integer "$g"; then overall_scored=$((overall_scored + g)); fi
      if is_integer "$t"; then overall_total=$((overall_total + t)); fi
    fi
  done
  if [ $overall_total -gt 0 ]; then
    printf '%b\n' "${TOTAL_PREFIX} Total Score: ${overall_scored}/${overall_total}"
    echo "$SEP"
  fi
  # Final table summary per problem and totals (dynamic widths + proper borders)
  printf '%b\n' "${BOLD}Summary Table${RESET}"
  h1="Problem"; h2="pass_test"; h3="fail_test"; h4="score"
  name_w=${#h1}; pass_w=${#h2}; fail_w=${#h3}; score_w=${#h4}
  [ $name_w  -lt 8 ] && name_w=8
  [ $pass_w  -lt 10 ] && pass_w=10
  [ $fail_w  -lt 10 ] && fail_w=10
  [ $score_w -lt 12 ] && score_w=12
  sum_pass=0
  sum_fail=0
  sum_g=0
  sum_t=0
  # First pass to compute max widths across data
  for prob in $problems; do
    pass=0; total=0; g=0; t=0
    [ -f "build/${prob}.cases" ] && read -r pass total < "build/${prob}.cases" || true
    [ -f "build/${prob}.score" ] && read -r g t < "build/${prob}.score" || true
    # Normalize to integers for safe arithmetic
    if ! is_integer "$pass"; then pass=0; fi
    if ! is_integer "$total"; then total=0; fi
    fail=$(( total - pass ))
    # Update widths
    [ ${#prob} -gt $name_w ] && name_w=${#prob}
    sp="${g}/${t}"; [ ${#sp} -gt $score_w ] && score_w=${#sp}
  done
  # Compute total row widths impact
  sp_total="${overall_scored}/${overall_total}"; [ ${#sp_total} -gt $score_w ] && score_w=${#sp_total}

  # Helper to repeat a character N times
  rep() { local n=$1 ch=$2; local s=""; while [ $n -gt 0 ]; do s="$s$ch"; n=$((n-1)); done; printf '%s' "$s"; }

  # Build borders with +2 padding per column
  top="┌$(rep $((name_w+2)) '─')┬$(rep $((pass_w+2)) '─')┬$(rep $((fail_w+2)) '─')┬$(rep $((score_w+2)) '─')┐"
  sep="├$(rep $((name_w+2)) '─')┼$(rep $((pass_w+2)) '─')┼$(rep $((fail_w+2)) '─')┼$(rep $((score_w+2)) '─')┤"
  bot="└$(rep $((name_w+2)) '─')┴$(rep $((pass_w+2)) '─')┴$(rep $((fail_w+2)) '─')┴$(rep $((score_w+2)) '─')┘"

  printf '%s\n' "$top"
  printf '│ %-*s │ %*s │ %*s │ %*s │\n' "$name_w" "$h1" "$pass_w" "$h2" "$fail_w" "$h3" "$score_w" "$h4"
  printf '%s\n' "$sep"
  for prob in $problems; do
    pass=0; total=0; g=0; t=0
    if [ -f "build/${prob}.cases" ]; then
      read -r pass total < "build/${prob}.cases" || true
    fi
    if [ -f "build/${prob}.score" ]; then
      read -r g t < "build/${prob}.score" || true
    fi
    if ! is_integer "$pass"; then pass=0; fi
    if ! is_integer "$total"; then total=0; fi
    if ! is_integer "$g"; then g=0; fi
    if ! is_integer "$t"; then t=0; fi
    fail=$(( total - pass ))
    printf '│ %-*s │ %*d │ %*d │ %*s │\n' "$name_w" "$prob" "$pass_w" "$pass" "$fail_w" "$fail" "$score_w" "$g/$t"
    sum_pass=$(( sum_pass + pass ))
    sum_fail=$(( sum_fail + fail ))
    sum_g=$(( sum_g + g ))
    sum_t=$(( sum_t + t ))
  done
  printf '%s\n' "$sep"
  printf '│ %-*s │ %*d │ %*d │ %*s │\n' "$name_w" "total" "$pass_w" "$sum_pass" "$fail_w" "$sum_fail" "$score_w" "$sum_g/$sum_t"
  printf '%s\n' "$bot"
  echo "$SEP"
  printf '%b\n' "${BLUE}${BOLD}────────────────────────────────────────────────────────${RESET}"
  exit $overall_fail
fi
