import os
import yaml
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
SRC_DIR = os.path.join(BASE_DIR, "src")

def load_config():
    yaml_path = os.path.join(CONFIG_DIR, "config.yaml")
    print(f"Checking config at: {yaml_path}")
    if os.path.exists(yaml_path):
        try:
            with open(yaml_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading yaml: {e}")
            return {}
    return {}

def test_discovery():
    config = load_config()
    print(f"Config loaded keys: {config.keys()}")
    if 'problems' in config:
        print(f"Problems in config: {list(config['problems'].keys())}")
    
    files = glob.glob(os.path.join(SRC_DIR, "p*.cpp"))
    seen = set()
    prob_names = []
    
    # Add from config
    if 'problems' in config:
        for p in config['problems']:
            if p not in seen:
                prob_names.append(p)
                seen.add(p)

    # Add from files
    for f in files:
        name = os.path.basename(f).replace(".cpp", "")
        base = name.split('_')[0]
        if base not in seen:
            prob_names.append(base)
            seen.add(base)
    prob_names.sort()
    
    print(f"Discovered problems: {prob_names}")

if __name__ == "__main__":
    test_discovery()
