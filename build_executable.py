import os
import subprocess
import sys
import platform

def install_pyinstaller():
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    system = platform.system()
    print(f"Building for {system}...")
    
    # Define the main script
    main_script = "run_tests.py"
    
    # Define the name of the executable
    app_name = f"CppLabTestSystem_{system}"
    
    # Determine the separator for --add-data based on the OS
    sep = ";" if system == "Windows" else ":"
    
    # PyInstaller arguments
    args = [
        "pyinstaller",
        "--name", app_name,
        "--onefile",  # Create a single executable file
        "--add-data", f"templates{sep}templates",  # Include templates directory
        "--add-data", f"config{sep}config",        # Include config directory
        "--add-data", f"static{sep}static",        # Include static directory
        "--hidden-import", "flask",
        "--hidden-import", "yaml",
        main_script
    ]
    
    print("Running PyInstaller with arguments:", " ".join(args))
    
    try:
        subprocess.check_call(args)
        print(f"\nBuild successful! The executable is located in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")

if __name__ == "__main__":
    install_pyinstaller()
    build_executable()
