#!/usr/bin/env python3
import sys
import os
import glob
import argparse
from app.utils import Colors, SRC_DIR, BUILD_DIR
from app.config import load_config
from app.runner import run_problem, print_diff # print_diff might be needed if I moved it to utils? Yes I did.
from app.server import start_server

# Need to re-implement print_summary or move it to utils/runner?
# It was in run_tests.py. Let's put it here or in utils.
# It's better in utils or runner. I'll put it in utils for now or just keep it here since it's CLI specific display.
# Actually, let's keep CLI logic here to keep it simple as an entry point, but use the core logic from app.

def print_summary(results):
    print(f"{Colors.BOLD}Summary Table{Colors.RESET}")
    
    # Headers
    headers = ["Problem", "pass_test", "fail_test", "score"]
    
    # Calculate widths
    widths = [len(h) for h in headers]
    
    # Data rows
    rows = []
    total_pass = 0
    total_fail = 0
    total_score = 0
    total_max_score = 0
    
    for prob, (fail_count, score, max_score, pass_count, case_total) in results.items():
        score_str = f"{score}/{max_score}"
        rows.append([prob, str(pass_count), str(fail_count), score_str])
        
        widths[0] = max(widths[0], len(prob))
        widths[1] = max(widths[1], len(str(pass_count)))
        widths[2] = max(widths[2], len(str(fail_count)))
        widths[3] = max(widths[3], len(score_str))
        
        total_pass += pass_count
        total_fail += fail_count
        total_score += score
        total_max_score += max_score

    # Total row
    total_score_str = f"{total_score}/{total_max_score}"
    rows.append(["total", str(total_pass), str(total_fail), total_score_str])
    
    widths[0] = max(widths[0], len("total"))
    widths[1] = max(widths[1], len(str(total_pass)))
    widths[2] = max(widths[2], len(str(total_fail)))
    widths[3] = max(widths[3], len(total_score_str))
    
    # Print table
    def print_sep(chars):
        line = chars[0] + chars[1].join([chars[2] * (w + 2) for w in widths]) + chars[3]
        print(line)
        
    print_sep("┌┬─┐")
    
    # Header
    print("│ " + " │ ".join(f"{h:<{w}}" for h, w in zip(headers, widths)) + " │")
    print_sep("├┼─┤")
    
    # Rows
    for i, row in enumerate(rows):
        if i == len(rows) - 1: # Separator before total
             print_sep("├┼─┤")
        print("│ " + " │ ".join(f"{d:<{w}}" for d, w in zip(row, widths)) + " │")
        
    print_sep("└┴─┘")
    print("========================================================")

def main():
    parser = argparse.ArgumentParser(description="Lab Test Runner")
    parser.add_argument("problem", nargs="?", help="Specific problem to run (e.g. p1)")
    parser.add_argument("--color", action="store_true", help="Force color output")
    parser.add_argument("--no-color", action="store_true", help="Disable color output")
    parser.add_argument("--gui", action="store_true", help="Launch Web UI")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (for developers)")
    
    args = parser.parse_args()
    
    # Handle Color
    if args.no_color:
        Colors.disable()
    elif args.color or os.environ.get("FORCE_COLOR"):
        pass # Colors enabled by default class
    elif not sys.stdout.isatty():
        Colors.disable()

    config = load_config()
    
    # Banner
    print(f"{Colors.BLUE}{Colors.BOLD}────────────────────────────────────────────────────────{Colors.RESET}")
    print(f"{Colors.BOLD}🧪 Lab Test Runner (Python){Colors.RESET}")
    print(f"📁 Root   : {Colors.CYAN}{os.getcwd()}{Colors.RESET}")
    print(f"📦 Results: {Colors.CYAN}{BUILD_DIR}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}────────────────────────────────────────────────────────{Colors.RESET}")

    if args.gui:
        start_server(debug=args.debug)
    else:
        # CLI Mode
        problems = []
        if args.problem:
            problems = [args.problem]
        else:
            # Discover all
            files = glob.glob(os.path.join(SRC_DIR, "p*.cpp"))
            seen = set()
            
            # Add from config
            if 'problems' in config:
                for p in config['problems']:
                    if p not in seen:
                        problems.append(p)
                        seen.add(p)

            for f in files:
                name = os.path.basename(f).replace(".cpp", "")
                base = name.split('_')[0]
                if base not in seen:
                    problems.append(base)
                    seen.add(base)
            problems.sort()
            
            if not problems:
                print("❌ No problems discovered in src/ or config")
                sys.exit(1)

        results = {} # prob -> (fail, score, max, pass, total)
        overall_fail = 0
        
        for prob in problems:
            fail_count, score, max_score, _ = run_problem(prob, config)
            
            pass_count = 0
            case_total = 0
            if os.path.exists(os.path.join(BUILD_DIR, f"{prob}.cases")):
                with open(os.path.join(BUILD_DIR, f"{prob}.cases"), 'r') as f:
                    parts = f.read().split()
                    if len(parts) >= 2:
                        pass_count = int(parts[0])
                        case_total = int(parts[1])
            
            results[prob] = (fail_count, score, max_score, pass_count, case_total)
            overall_fail += fail_count

        if len(problems) > 1 or not args.problem:
            # Calculate total score
            total_score = sum(r[1] for r in results.values())
            total_max = sum(r[2] for r in results.values())
            if total_max > 0:
                 print(f"{Colors.BOLD}📊 TOTAL Total Score: {total_score}/{total_max}{Colors.RESET}")
                 print("========================================================")
            
            print_summary(results)
            
        print(f"{Colors.BLUE}{Colors.BOLD}────────────────────────────────────────────────────────{Colors.RESET}")
        sys.exit(overall_fail)

if __name__ == "__main__":
    main()
