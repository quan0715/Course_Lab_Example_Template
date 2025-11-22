#!/usr/bin/env bash
CONFIG_FILE="config/points.conf"

# Colors
BLUE="\033[34m"
BOLD="\033[1m"
RESET="\033[0m"
GREEN="\033[32m"
RED="\033[31m"
YELLOW="\033[33m"

cfg_get() {
  local key="$1"
  if [ -f "$CONFIG_FILE" ]; then
    awk -F= -v k="$key" 'BEGIN{IGNORECASE=0} $1==k {print $2; exit}' "$CONFIG_FILE"
  fi
}

echo -e "${BLUE}${BOLD}========================================================${RESET}"
echo -e "${BOLD}🔧 Configuration Verification${RESET}"
echo -e "${BLUE}${BOLD}========================================================${RESET}"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: Configuration file $CONFIG_FILE not found.${RESET}"
    exit 1
fi

# Global
def_timeout=$(cfg_get "timeout.default")
[ -z "$def_timeout" ] && def_timeout="1"
echo -e "Global Settings:"
echo -e "  Default Timeout: ${BOLD}${def_timeout}s${RESET}"
echo ""

# Find all problems
# grep keys that look like problem.X, timeout.X, forbidden.X, required.X
# and extract the problem name, excluding 'default'
problems=$(grep -E "^(problem|timeout|forbidden|required)\." "$CONFIG_FILE" | cut -d. -f2 | cut -d= -f1 | grep -v "^default$" | sort | uniq)

echo -e "Problem Settings:"

for prob in $problems; do
    echo -e "${BLUE}--------------------------------------------------------${RESET}"
    echo -e "Problem: ${GREEN}${BOLD}${prob}${RESET}"
    
    # Points
    pts=$(cfg_get "problem.${prob}")
    echo -e "  Points: ${pts}"
    
    # Timeout
    t=$(cfg_get "timeout.${prob}")
    if [ -n "$t" ]; then
        echo -e "  Timeout: ${t}s (override)"
    else
        echo -e "  Timeout: ${def_timeout}s (default)"
    fi
    
    # Forbidden
    forbidden=$(cfg_get "forbidden.${prob}")
    if [ -n "$forbidden" ]; then
        echo -e "  Forbidden: ${RED}${forbidden}${RESET}"
    else
        echo -e "  Forbidden: (none)"
    fi
    
    # Required
    required=$(cfg_get "required.${prob}")
    if [ -n "$required" ]; then
        echo -e "  Required: ${GREEN}${required}${RESET}"
    else
        echo -e "  Required: (none)"
    fi
    
    # Case overrides
    # grep for case.prob.
    case_overrides=$(grep "^case\.${prob}\." "$CONFIG_FILE" | cut -d. -f3 | cut -d= -f1 | sort)
    if [ -n "$case_overrides" ]; then
        echo -e "  Case Overrides:"
        for c in $case_overrides; do
            val=$(cfg_get "case.${prob}.${c}")
            echo -e "    ${c}: ${val}"
        done
    fi
done
echo -e "${BLUE}${BOLD}========================================================${RESET}"
