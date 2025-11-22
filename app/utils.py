import os
import difflib

# --- Configuration ---
CONFIG_DIR = "config"
CONFIG_FILE = "config/points.conf"
BUILD_DIR = "build"
SRC_DIR = "src"
TESTS_DIR = "tests"

# ANSI Colors
class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def disable():
        Colors.RED = ""
        Colors.GREEN = ""
        Colors.YELLOW = ""
        Colors.BLUE = ""
        Colors.CYAN = ""
        Colors.BOLD = ""
        Colors.RESET = ""

# Prefixes
def get_prefixes():
    return {
        "PASS": f"{Colors.GREEN}✅ PASS{Colors.RESET}",
        "FAIL": f"{Colors.RED}❌ FAIL{Colors.RESET}",
        "TLE": f"{Colors.YELLOW}⏱️ TLE{Colors.RESET}",
        "BUILD": f"{Colors.BLUE}🔧 BUILD{Colors.RESET}",
        "RESULT": f"{Colors.BOLD}📄 RESULT{Colors.RESET}",
        "TOTAL": f"{Colors.BOLD}📊 TOTAL{Colors.RESET}",
    }

def print_diff(expected, got):
    # Simple unified diff
    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        got.splitlines(keepends=True),
        fromfile='expected',
        tofile='got',
    )
    
    # Colorize diff
    for line in diff:
        if line.startswith('+'):
            print(f"{Colors.GREEN}{line.rstrip()}{Colors.RESET}")
        elif line.startswith('-'):
            print(f"{Colors.RED}{line.rstrip()}{Colors.RESET}")
        elif line.startswith('@'):
            print(f"{Colors.BLUE}{Colors.BOLD}{line.rstrip()}{Colors.RESET}")
        else:
            print(line.rstrip())
