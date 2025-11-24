import os
import glob
import platform
import subprocess
from app.utils import SRC_DIR, get_prefixes
from app.config import load_config

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
    config = load_config()
    compiler = config.get("compiler_path", "g++")
    
    bin_path = os.path.join(build_dir, prob)
    if platform.system() == "Windows":
        bin_path += ".exe"
    
    print(f"{prefixes['BUILD']} Compiling {src}...")
    log_path = os.path.join(build_dir, f"{prob}.compile.log")
    
    cmd = [compiler, "-std=c++17", "-O2", src, "-o", bin_path]
    
    try:
        with open(log_path, "w") as log:
            subprocess.check_call(cmd, stdout=log, stderr=log)
        print(f"{prefixes['PASS']} Compilation successful")
        return bin_path
    except subprocess.CalledProcessError:
        print(f"{prefixes['FAIL']} Compilation failed for {prob}. See {log_path}")
        return None
    except FileNotFoundError:
        print(f"{prefixes['FAIL']} Compiler not found: '{compiler}'")
        print(f"  Please check your PATH or update 'compiler_path' in config/config.yaml")
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

    config = load_config()
    compiler = config.get("compiler_path", "g++")
    cmd = [compiler, "-std=c++17", "-O2", src, "-o", bin_path]
    
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
    except FileNotFoundError:
        return None, f"Compiler not found: '{compiler}'. Please check your PATH or update 'compiler_path' in config/config.yaml"
