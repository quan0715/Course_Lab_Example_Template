import os
from app.utils import CONFIG_DIR

def parse_simple_yaml(path):
    """Simple YAML parser for basic config structure"""
    config = {}
    current_section = None
    current_sub = None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip()
                if not line or line.strip().startswith('#'):
                    continue
                
                indent = len(line) - len(line.lstrip())
                content = line.strip()
                
                if ':' in content:
                    key, val = content.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    
                    # Remove quotes if present
                    if val.startswith("'") and val.endswith("'"): val = val[1:-1]
                    if val.startswith('"') and val.endswith('"'): val = val[1:-1]
                    
                    if indent == 0:
                        current_section = key
                        config[current_section] = {}
                        current_sub = None
                    elif indent == 2:
                        if current_section == 'problems':
                            current_sub = key
                            config[current_section][current_sub] = {}
                        elif current_section:
                            config[current_section][key] = val
                    elif indent == 4:
                        if current_section == 'problems' and current_sub:
                            config[current_section][current_sub][key] = val
    except Exception as e:
        print(f"Error parsing YAML manually: {e}")
    return config

def load_config():
    """Load configuration from YAML or legacy conf file"""
    yaml_path = os.path.join(CONFIG_DIR, "config.yaml")
    conf_path = os.path.join(CONFIG_DIR, "points.conf")
    
    # Try YAML first
    if os.path.exists(yaml_path):
        try:
            import yaml
            with open(yaml_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            print("PyYAML not installed. Using fallback parser.")
            return parse_simple_yaml(yaml_path)
        except Exception as e:
            print(f"Warning: Failed to load YAML config: {e}")
            return parse_simple_yaml(yaml_path)
    
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
