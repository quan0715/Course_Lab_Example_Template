import os
import sys
import glob
import markdown
from flask import Flask, jsonify, render_template, send_from_directory, request
from app.utils import SRC_DIR, BUILD_DIR, TESTS_DIR
from app.config import load_config, get_problem_points, get_problem_name, get_app_title, get_app_description, get_timeout
from app.compiler import find_source
from app.runner import run_problem

def start_server():
    # Determine template folder path (works for source and PyInstaller)
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')
    else:
        template_folder = os.path.abspath('templates')
        static_folder = os.path.abspath('static')

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    @app.route('/api/code/<prob>', methods=['GET', 'POST'])
    def handle_code(prob):
        src_file = find_source(prob)
        if not src_file:
            # If file doesn't exist, try to create it from template or just empty
            src_file = os.path.join(SRC_DIR, f"{prob}.cpp")
            if not os.path.exists(src_file):
                with open(src_file, 'w') as f:
                    f.write(f"// Source for {prob}\n#include <iostream>\n\nint main() {{\n    return 0;\n}}\n")

        if request.method == 'GET':
            try:
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                return jsonify({'content': content})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        elif request.method == 'POST':
            try:
                data = request.get_json()
                content = data.get('content')
                if content is None:
                    return jsonify({'error': 'No content provided'}), 400
                
                # Backup
                bak_file = src_file + ".bak"
                if os.path.exists(src_file):
                    import shutil
                    shutil.copy2(src_file, bak_file)
                
                with open(src_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/problems')
    def api_problems():
        config = load_config()
        print(f"DEBUG: Config loaded keys: {list(config.keys())}")
        
        files = glob.glob(os.path.join(SRC_DIR, "p*.cpp"))
        seen = set()
        
        # First discover all problems
        prob_names = []
        
        # Add from config
        if 'problems' in config:
            print(f"DEBUG: Problems in config: {list(config['problems'].keys())}")
            for p in config['problems']:
                if p not in seen:
                    prob_names.append(p)
                    seen.add(p)
        else:
            print("DEBUG: 'problems' key not found in config")

        # Add from files
        for f in files:
            name = os.path.basename(f).replace(".cpp", "")
            base = name.split('_')[0]
            if base not in seen:
                prob_names.append(base)
                seen.add(base)
        prob_names.sort()
        
        print(f"DEBUG: Final problem list: {prob_names}")
        
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
            
            # Get details if run
            details = []
            # Note: We don't store full details in files currently, only summary.
            # If we want details on load, we might need to store them or just show summary.
            # For now, let's just return summary data.
            
            data.append({
                "name": p,
                "display_name": get_problem_name(config, p),
                "score": score,
                "total_points": total_points,
                "passed": passed,
                "total_tests": total_tests,
                "has_run": has_run,
                "details": [] # Empty initially
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
        
        fail_count = total_count - pass_count
        
        return jsonify({
            "score": score,
            "total_points": max_score,
            "passed_count": pass_count,
            "total_count": total_count,
            "fail_count": fail_count,
            "details": details
        })

    @app.route('/api/problem/<prob>/info')
    def api_problem_info(prob):
        config = load_config()
        
        # Get description from markdown file
        desc_file = os.path.join('problems', f"{prob}.md")
        desc_content = ""
        if os.path.exists(desc_file):
            with open(desc_file, 'r', encoding='utf-8') as f:
                desc_content = f.read()
        else:
            desc_content = f"# {prob}\nNo description available."
        
        # Get forbidden and required keywords
        forbidden = []
        required = []
        if 'problems' in config and isinstance(config['problems'], dict):
            if prob in config['problems'] and isinstance(config['problems'][prob], dict):
                forbidden_val = config['problems'][prob].get('forbidden', [])
                required_val = config['problems'][prob].get('required', [])
                if isinstance(forbidden_val, list):
                    forbidden = forbidden_val
                if isinstance(required_val, list):
                    required = required_val
            
        return jsonify({
            "name": prob,
            "display_name": get_problem_name(config, prob),
            "description_md": desc_content,
            "points": get_problem_points(config, prob),
            "timeout": get_timeout(config, prob),
            "forbidden": forbidden,
            "required": required
        })

    @app.route('/api/git_push', methods=['POST'])
    def git_push():
        """處理 Git Push 請求"""
        import subprocess
        
        data = request.get_json()
        commit_message = data.get('commit_message', '更新程式碼')
        
        try:
            # 檢查是否在 git repository 中
            result = subprocess.run(
                ['git', 'rev-parse', '--is-inside-work-tree'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return jsonify({
                    'success': False,
                    'error': '這不是一個 Git repository',
                    'details': '請確認專案目錄已經初始化 Git'
                })
            
            # 檢查 git remote
            result = subprocess.run(
                ['git', 'remote', '-v'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if not result.stdout.strip():
                return jsonify({
                    'success': False,
                    'error': '沒有設定 Git remote',
                    'details': '請先設定遠端 repository:\ngit remote add origin <URL>'
                })
            
            # 先檢查 src/*.cpp 是否有變更
            import glob
            cpp_files = glob.glob('src/*.cpp')
            
            if not cpp_files:
                return jsonify({
                    'success': False,
                    'error': '沒有找到 .cpp 檔案',
                    'details': 'src/ 目錄中沒有 .cpp 檔案'
                })
            
            # 檢查這些檔案是否有變更（包括 modified 和 untracked）
            result = subprocess.run(
                ['git', 'status', '--porcelain'] + cpp_files,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # 如果沒有任何變更，不允許 commit
            if not result.stdout.strip():
                return jsonify({
                    'success': False,
                    'error': '沒有需要提交的變更',
                    'details': 'src/ 目錄中的 .cpp 檔案沒有任何修改'
                })
            
            # git add src/*.cpp（加入所有 src 目錄下的 .cpp 檔案）
            result = subprocess.run(
                ['git', 'add'] + cpp_files,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return jsonify({
                    'success': False,
                    'error': 'git add 失敗',
                    'details': result.stderr or result.stdout
                })
            
            # git commit
            result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                # 可能沒有變更或其他錯誤
                if 'nothing to commit' in result.stdout:
                    return jsonify({
                        'success': True,
                        'message': '沒有需要提交的變更',
                        'details': result.stdout
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Commit 失敗',
                        'details': result.stderr or result.stdout
                    })
            
            commit_info = result.stdout
            
            # git push
            result = subprocess.run(
                ['git', 'push'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return jsonify({
                    'success': False,
                    'error': 'Push 失敗',
                    'details': result.stderr or result.stdout
                })
            
            return jsonify({
                'success': True,
                'message': '成功推送到 GitHub！',
                'details': f"Commit: {commit_info}\n\nPush: {result.stderr or result.stdout}"
            })
            
        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'error': 'Git 操作逾時',
                'details': '請檢查網路連線或手動執行 git push'
            })
        except FileNotFoundError:
            return jsonify({
                'success': False,
                'error': '找不到 Git',
                'details': '請確認已安裝 Git: https://git-scm.com/'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': '未知錯誤',
                'details': str(e)
            })

    app.run(host='0.0.0.0', port=8080, debug=True)
