#!/usr/bin/env python3
import sys
import os
import subprocess
import glob
import time
import argparse
import platform
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

# --- Helpers ---

def load_config():
    """Load configuration from YAML or legacy conf file"""
    yaml_path = os.path.join(CONFIG_DIR, "config.yaml")
    conf_path = os.path.join(CONFIG_DIR, "points.conf")
    
    # Try YAML first
    if os.path.exists(yaml_path):
        try:
            import yaml
            with open(yaml_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            print("Warning: PyYAML not installed. Install with: pip install pyyaml")
            print("Falling back to legacy conf format...")
        except Exception as e:
            print(f"Warning: Failed to load YAML config: {e}")
            print("Falling back to legacy conf format...")
    
    # Fallback to legacy conf format
    config = {}
    if os.path.exists(conf_path):
        with open(conf_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    config[key.strip()] = val.strip()
    return config

def get_config_val(config, key, default=None):
    """Get config value supporting both YAML nested structure and flat key format"""
    # For YAML nested structure
    if isinstance(config, dict) and '.' in key:
        parts = key.split('.')
        current = config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current if current is not None else default
    
    # For flat key format (legacy)
    return config.get(key, default)

def get_problem_points(config, prob):
    # Try YAML nested structure first
    if 'problems' in config and isinstance(config['problems'], dict):
        if prob in config['problems'] and isinstance(config['problems'][prob], dict):
            points = config['problems'][prob].get('points')
            if points is not None:
                return int(points)
    
    # Fallback to flat key
    val = get_config_val(config, f"problem.{prob}")
    if val and str(val).isdigit():
        return int(val)
    return 0

def get_case_points(config, prob, case_base):
    val = get_config_val(config, f"case.{prob}.{case_base}")
    if val and val.isdigit():
        return int(val)
    return None

def get_timeout(config, prob):
    # Try YAML nested structure first
    if 'problems' in config and isinstance(config['problems'], dict):
        if prob in config['problems'] and isinstance(config['problems'][prob], dict):
            timeout = config['problems'][prob].get('timeout')
            if timeout is not None:
                return int(timeout)
    
    # Try flat key problem specific
    val = get_config_val(config, f"timeout.{prob}")
    if val and str(val).isdigit():
        return int(val)
    
    # Try YAML defaults
    if 'defaults' in config and isinstance(config['defaults'], dict):
        timeout = config['defaults'].get('timeout')
        if timeout is not None:
            return int(timeout)
    
    # Try flat key default
    val = get_config_val(config, "timeout.default")
    if val and str(val).isdigit():
        return int(val)
    return 1

def get_app_title(config):
    # Try YAML nested
    if 'app' in config and isinstance(config['app'], dict):
        title = config['app'].get('title')
        if title:
            return title
    # Fallback to flat key
    return get_config_val(config, "app.title", "Lab Test Runner")

def get_app_description(config):
    # Try YAML nested
    if 'app' in config and isinstance(config['app'], dict):
        desc = config['app'].get('description')
        if desc:
            return desc
    # Fallback to flat key
    return get_config_val(config, "app.description", "C++ Programming Lab Test System")

def get_problem_name(config, prob):
    """Get display name for a problem, fallback to problem ID"""
    # Try YAML nested
    if 'problems' in config and isinstance(config['problems'], dict):
        if prob in config['problems'] and isinstance(config['problems'][prob], dict):
            name = config['problems'][prob].get('name')
            if name:
                return name
    # Fallback to flat key
    return get_config_val(config, f"name.{prob}", prob)

def check_keywords(config, prob, src_file):
    with open(src_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    prefixes = get_prefixes()
    
    # Forbidden
    forbidden = get_config_val(config, f"forbidden.{prob}")
    if forbidden:
        for keyword in forbidden.split(','):
            keyword = keyword.strip()
            if not keyword: continue
            # Simple check: exact word match using split is tricky, 
            # but for now let's do a simple substring check or use regex if needed.
            # The shell script used grep -w. Let's try to emulate that roughly or just simple 'in'.
            # To be robust like grep -w, we should use regex.
            import re
            if re.search(r'\b' + re.escape(keyword) + r'\b', content):
                print(f"{prefixes['FAIL']} Forbidden keyword found: '{keyword}'")
                return False

    # Required
    required = get_config_val(config, f"required.{prob}")
    if required:
        for keyword in required.split(','):
            keyword = keyword.strip()
            if not keyword: continue
            import re
            if not re.search(r'\b' + re.escape(keyword) + r'\b', content):
                print(f"{prefixes['FAIL']} Required keyword missing: '{keyword}'")
                return False
                
    return True

def find_source(prob):
    # Exact match
    p = os.path.join(SRC_DIR, f"{prob}.cpp")
    if os.path.exists(p):
        return p
    # Prefix match
    matches = glob.glob(os.path.join(SRC_DIR, f"{prob}_*.cpp"))
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"❌ Multiple sources found for {prob}: {matches}")
        return None
    return None

def compile_problem(prob, src, build_dir):
    prefixes = get_prefixes()
    bin_path = os.path.join(build_dir, prob)
    if platform.system() == "Windows":
        bin_path += ".exe"
    
    print(f"{prefixes['BUILD']} Compiling {src}...")
    log_path = os.path.join(build_dir, f"{prob}.compile.log")
    
    cmd = ["g++", "-std=c++17", "-O2", src, "-o", bin_path]
    
    try:
        with open(log_path, "w") as log:
            subprocess.check_call(cmd, stdout=log, stderr=log)
        print(f"{prefixes['PASS']} Compilation successful")
        return bin_path
    except subprocess.CalledProcessError:
        print(f"{prefixes['FAIL']} Compilation failed for {prob}. See {log_path}")
        return None

def compile_problem_with_log(prob, src, build_dir):
    """Compile and return both bin_path and log content"""
    bin_path = os.path.join(build_dir, prob)
    if platform.system() == "Windows":
        bin_path += ".exe"
    
    log_path = os.path.join(build_dir, f"{prob}.compile.log")
    
    # Check if we need to recompile
    needs_compile = True
    if os.path.exists(bin_path):
        src_mtime = os.path.getmtime(src)
        bin_mtime = os.path.getmtime(bin_path)
        if bin_mtime > src_mtime:
            needs_compile = False
            
    if not needs_compile:
        return bin_path, ""

    cmd = ["g++", "-std=c++17", "-O2", src, "-o", bin_path]
    
    try:
        with open(log_path, "w") as log:
            subprocess.check_call(cmd, stdout=log, stderr=log)
        return bin_path, ""
    except subprocess.CalledProcessError:
        # Read log content
        log_content = ""
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                log_content = f.read()
        return None, log_content

def check_keywords_detailed(config, prob, src_file):
    """Check keywords and return detailed result"""
    with open(src_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    result = {
        'passed': True,
        'message': '',
        'forbidden': [],
        'required': [],
        'violations': []
    }
    
    # Get forbidden keywords
    forbidden = None
    if 'problems' in config and isinstance(config['problems'], dict):
        if prob in config['problems'] and isinstance(config['problems'][prob], dict):
            forbidden = config['problems'][prob].get('forbidden')
    if forbidden is None:
        forbidden_str = get_config_val(config, f"forbidden.{prob}")
        if forbidden_str:
            forbidden = [k.strip() for k in forbidden_str.split(',') if k.strip()]
    
    if forbidden:
        if isinstance(forbidden, str):
            forbidden = [k.strip() for k in forbidden.split(',') if k.strip()]
        result['forbidden'] = forbidden
        
        for keyword in forbidden:
            import re
            if re.search(r'\b' + re.escape(keyword) + r'\b', content):
                result['passed'] = False
                result['violations'].append(f"Forbidden keyword found: '{keyword}'")
    
    # Get required keywords
    required = None
    if 'problems' in config and isinstance(config['problems'], dict):
        if prob in config['problems'] and isinstance(config['problems'][prob], dict):
            required = config['problems'][prob].get('required')
    if required is None:
        required_str = get_config_val(config, f"required.{prob}")
        if required_str:
            required = [k.strip() for k in required_str.split(',') if k.strip()]
    
    if required:
        if isinstance(required, str):
            required = [k.strip() for k in required.split(',') if k.strip()]
        result['required'] = required
        
        for keyword in required:
            import re
            if not re.search(r'\b' + re.escape(keyword) + r'\b', content):
                result['passed'] = False
                result['violations'].append(f"Required keyword missing: '{keyword}'")
    
    if not result['passed']:
        result['message'] = '; '.join(result['violations'])
    
    return result

def run_test_case(bin_path, input_file, expected_file, timeout_sec):
    prefixes = get_prefixes()
    
    try:
        with open(input_file, 'r') as fin:
            input_data = fin.read()
            
        start_time = time.time()
        # Run process
        proc = subprocess.run(
            [bin_path],
            input=input_data,
            capture_output=True,
            timeout=timeout_sec,
            text=True # Expect text output
        )
        
        if proc.returncode != 0:
            return "Runtime Error", proc.stderr
            
        # Compare output
        got = proc.stdout
        # Normalize line endings for comparison
        got = got.replace('\r\n', '\n')
        
        with open(expected_file, 'r') as fexp:
            expected = fexp.read().replace('\r\n', '\n')
        
        if got == expected:
            return "PASS", None
        else:
            return "FAIL", (expected, got)
                
    except subprocess.TimeoutExpired:
        return "TLE", None
    except Exception as e:
        return "Error", str(e)

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

def run_problem(prob, config, capture_logs=False):
    prefixes = get_prefixes()
    if not capture_logs:
        print("========================================================")
    
    src = find_source(prob)
    if not src:
        if not capture_logs: print(f"❌ No source for {prob}")
        return 0, 0, 0, [] # fail, score, total_score, details

    # Keyword Check
    keyword_check_result = check_keywords_detailed(config, prob, src)
    if not keyword_check_result['passed']:
        total_points = get_problem_points(config, prob)
        return 1, 0, total_points, [{
            "case": "Keyword Check", 
            "status": "FAIL", 
            "msg": keyword_check_result['message'],
            "forbidden": keyword_check_result.get('forbidden', []),
            "required": keyword_check_result.get('required', []),
            "violations": keyword_check_result.get('violations', [])
        }]

    # Compile
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)
        
    bin_path, compile_log = compile_problem_with_log(prob, src, BUILD_DIR)
    if not bin_path:
        total_points = get_problem_points(config, prob)
        return 1, 0, total_points, [{
            "case": "Compilation", 
            "status": "FAIL", 
            "msg": "Compilation failed",
            "log": compile_log
        }]

    # Discover tests
    prob_tests_dir = os.path.join(TESTS_DIR, prob)
    inputs_dir = os.path.join(prob_tests_dir, "inputs")
    outputs_dir = os.path.join(prob_tests_dir, "outputs")
    
    if not os.path.exists(inputs_dir) or not os.path.exists(outputs_dir):
        if not capture_logs: print(f"{prefixes['FAIL']} No tests found for {prob}")
        return 1, 0, 0, []

    input_files = sorted(glob.glob(os.path.join(inputs_dir, "*.in")))
    if not input_files:
        if not capture_logs: print(f"{prefixes['FAIL']} No input files found")
        return 1, 0, 0, []

    total_points = get_problem_points(config, prob)
    timeout = get_timeout(config, prob)
    
    passed_count = 0
    total_count = 0
    
    details = []

    for infile in input_files:
        total_count += 1
        base = os.path.basename(infile)
        case_name = os.path.splitext(base)[0]
        outfile = os.path.join(outputs_dir, f"{case_name}.out")
        
        if not os.path.exists(outfile):
            if not capture_logs: print(f"{prefixes['FAIL']} {prob}:{base} (missing output)")
            details.append({"case": base, "status": "ERROR", "msg": "Missing expected output file"})
            continue
            
        result, data = run_test_case(bin_path, infile, outfile, timeout)
        
        # Read input content for display
        with open(infile, 'r') as f:
            input_content = f.read()

        if result == "PASS":
            if not capture_logs: print(f"{prefixes['PASS']} {prob}:{base}")
            passed_count += 1
            # Read output for display
            with open(outfile, 'r') as f:
                output_content = f.read()
            details.append({
                "case": base, 
                "status": "PASS",
                "input": input_content,
                "output": output_content
            })
        elif result == "TLE":
            if not capture_logs: print(f"{prefixes['TLE']} {prob}:{base} (Time Limit Exceeded: {timeout}s)")
            details.append({
                "case": base, 
                "status": "TLE", 
                "timeout": timeout,
                "input": input_content
            })
        elif result == "FAIL":
            expected, got = data
            if not capture_logs:
                print(f"{prefixes['FAIL']} {prob}:{base}")
                print(f"{Colors.YELLOW}----- Expected -----{Colors.RESET}")
                print(expected.rstrip())
                print(f"{Colors.YELLOW}----- Got -----{Colors.RESET}")
                print(got.rstrip())
                print(f"{Colors.YELLOW}----- Diff -----{Colors.RESET}")
                print_diff(expected, got)
            
            details.append({
                "case": base, 
                "status": "FAIL", 
                "input": input_content,
                "expected": expected,
                "got": got
            })
        else:
            if not capture_logs:
                print(f"{prefixes['FAIL']} {prob}:{base} ({result})")
                if data: print(f"-- stderr --\n{data}")
            
            details.append({
                "case": base, 
                "status": "ERROR", 
                "msg": result,
                "stderr": data if data else ""
            })

    if not capture_logs:
        print()
    
    score = 0
    if passed_count == total_count:
        score = total_points
    
    if not capture_logs:
        print(f"{prefixes['RESULT']} {prob} Result: {passed_count}/{total_count} tests passed | Score: {score}/{total_points}")
        print("========================================================")
    
    # Write artifacts for summary (optional, but good for consistency)
    with open(os.path.join(BUILD_DIR, f"{prob}.score"), "w") as f:
        f.write(f"{score} {total_points}")
    with open(os.path.join(BUILD_DIR, f"{prob}.cases"), "w") as f:
        f.write(f"{passed_count} {total_count}")

    return (total_count - passed_count), score, total_points, details

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
        start_gui()
    else:
        # CLI Mode
        problems = []
        if args.problem:
            problems = [args.problem]
        else:
            # Discover all
            files = glob.glob(os.path.join(SRC_DIR, "p*.cpp"))
            seen = set()
            for f in files:
                name = os.path.basename(f).replace(".cpp", "")
                base = name.split('_')[0]
                if base not in seen:
                    problems.append(base)
                    seen.add(base)
            problems.sort()
            
            if not problems:
                print("❌ No problems discovered in src/")
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

# --- GUI / Flask ---
def start_gui():
    try:
        from flask import Flask, render_template, jsonify
        import webbrowser
        from threading import Timer
    except ImportError:
        print("Flask is not installed. Please run: pip install flask")
        sys.exit(1)

    # Determine template folder path (works for source and PyInstaller)
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
    else:
        template_folder = 'templates'

    app = Flask(__name__, template_folder=template_folder)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/problems')
    def api_problems():
        config = load_config()
        files = glob.glob(os.path.join(SRC_DIR, "p*.cpp"))
        seen = set()
        problems = []
        
        # First discover all problems
        prob_names = []
        for f in files:
            name = os.path.basename(f).replace(".cpp", "")
            base = name.split('_')[0]
            if base not in seen:
                prob_names.append(base)
                seen.add(base)
        prob_names.sort()
        
        # Then gather data for each
        data = []
        for p in prob_names:
            # Default values
            score = 0
            total_points = get_problem_points(config, p)
            passed = 0
            total_tests = 0
            has_run = False
            
            # Try to read artifacts
            score_file = os.path.join(BUILD_DIR, f"{p}.score")
            cases_file = os.path.join(BUILD_DIR, f"{p}.cases")
            
            if os.path.exists(score_file):
                try:
                    with open(score_file, 'r') as f:
                        parts = f.read().split()
                        if len(parts) >= 2:
                            score = int(parts[0])
                            has_run = True
                except: pass
                
            if os.path.exists(cases_file):
                try:
                    with open(cases_file, 'r') as f:
                        parts = f.read().split()
                        if len(parts) >= 2:
                            passed = int(parts[0])
                            total_tests = int(parts[1])
                            has_run = True
                except: pass
            
            data.append({
                "name": p,
                "display_name": get_problem_name(config, p),
                "score": score,
                "total_points": total_points,
                "passed": passed,
                "total_tests": total_tests,
                "has_run": has_run
            })
        
        # Return app metadata along with problems
        return jsonify({
            "app_title": get_app_title(config),
            "app_description": get_app_description(config),
            "problems": data
        })

    @app.route('/api/run/<prob>', methods=['POST'])
    def api_run(prob):
        config = load_config()
        
        # Run with capture_logs=True to suppress stdout
        fail_count, score, max_score, details = run_problem(prob, config, capture_logs=True)
            
        # Read stats
        pass_count = 0
        total_count = 0
        if os.path.exists(os.path.join(BUILD_DIR, f"{prob}.cases")):
            with open(os.path.join(BUILD_DIR, f"{prob}.cases"), 'r') as cf:
                parts = cf.read().split()
                if len(parts) >= 2:
                    pass_count = int(parts[0])
                    total_count = int(parts[1])

        return jsonify({
            'prob': prob,
            'fail_count': fail_count,
            'score': score,
            'total_points': max_score,
            'passed_count': pass_count,
            'total_count': total_count,
            'details': details
        })

    @app.route('/api/problem/<prob>/info')
    def api_problem_info(prob):
        """Get problem metadata including description"""
        config = load_config()
        
        # Read markdown description if exists
        md_path = os.path.join("problems", f"{prob}.md")
        description_md = ""
        if os.path.exists(md_path):
            with open(md_path, 'r', encoding='utf-8') as f:
                description_md = f.read()
        
        # Get problem configuration
        info = {
            "name": prob,
            "display_name": get_problem_name(config, prob),
            "points": get_problem_points(config, prob),
            "timeout": get_timeout(config, prob),
            "description_md": description_md
        }
        
        # Get forbidden keywords
        forbidden = None
        if 'problems' in config and isinstance(config['problems'], dict):
            if prob in config['problems'] and isinstance(config['problems'][prob], dict):
                forbidden = config['problems'][prob].get('forbidden')
        if forbidden is None:
            forbidden_str = get_config_val(config, f"forbidden.{prob}")
            if forbidden_str:
                forbidden = [k.strip() for k in forbidden_str.split(',') if k.strip()]
        
        if forbidden:
            if isinstance(forbidden, str):
                forbidden = [k.strip() for k in forbidden.split(',') if k.strip()]
            info['forbidden'] = forbidden
        else:
            info['forbidden'] = []
        
        # Get required keywords
        required = None
        if 'problems' in config and isinstance(config['problems'], dict):
            if prob in config['problems'] and isinstance(config['problems'][prob], dict):
                required = config['problems'][prob].get('required')
        if required is None:
            required_str = get_config_val(config, f"required.{prob}")
            if required_str:
                required = [k.strip() for k in required_str.split(',') if k.strip()]
        
        if required:
            if isinstance(required, str):
                required = [k.strip() for k in required.split(',') if k.strip()]
            info['required'] = required
        else:
            info['required'] = []
        
        return jsonify(info)

    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')

    print("Starting Web UI at http://127.0.0.1:5000/")
    Timer(1, open_browser).start()
    app.run(port=5000)

if __name__ == "__main__":
    main()
