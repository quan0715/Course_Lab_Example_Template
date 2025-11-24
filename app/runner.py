import os
import time
import glob
import subprocess
from app.utils import Colors, get_prefixes, print_diff, BUILD_DIR, TESTS_DIR
from app.config import get_config_val, get_problem_points, get_timeout
from app.compiler import find_source, compile_problem_with_log

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
    import tempfile
    
    # Create temp files for stdout and stderr
    # Open in text mode ('w+') to match Popen text=True
    with tempfile.TemporaryFile(mode='w+') as f_out, tempfile.TemporaryFile(mode='w+') as f_err:
        try:
            with open(input_file, 'r') as fin:
                # Use Popen instead of run to have better control
                proc = subprocess.Popen(
                    [bin_path],
                    stdin=fin,
                    stdout=f_out,
                    stderr=f_err,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
            try:
                proc.wait(timeout=timeout_sec)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait() # Ensure it's dead
                return "TLE", None
            
            if proc.returncode != 0:
                f_err.seek(0)
                content = f_err.read()
                err_output = content.decode('utf-8', errors='replace') if isinstance(content, bytes) else content
                return "Runtime Error", err_output
                
            # Compare output
            f_out.seek(0)
            # Read with limit to avoid memory issues if output is huge (though TLE should catch infinite loops)
            # But if it finished within time but produced 1GB of data, we don't want to crash.
            got = f_out.read(1024 * 1024) # Limit to 1MB
            if f_out.read(1): # Check if there's more
                got += "\n... (output truncated)"
            
            # Normalize line endings
            got = got.replace('\r\n', '\n')
            
            with open(expected_file, 'r') as fexp:
                expected = fexp.read().replace('\r\n', '\n')
            
            if got.strip() == expected.strip(): # Use strip to be lenient on trailing newlines
                return "PASS", None
            else:
                return "FAIL", (expected, got)
                    
        except Exception as e:
            return "Error", str(e)

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
        if not capture_logs:
            print(f"{prefixes['FAIL']} Compilation failed:")
            print(compile_log)
            
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
