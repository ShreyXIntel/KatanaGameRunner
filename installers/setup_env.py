#!/usr/bin/env python3
"""
One-click script to:
1. Create a Python virtual environment in the root directory
2. Activate it and install dependencies from requirements.txt
3. Open a new command prompt in the root directory
4. Close the current window

This script is intended to be placed in /installers/setup_env.py
but will create the virtual environment in the root folder (/)
"""

import os
import platform
import subprocess
import sys
import shutil
from pathlib import Path

# ANSI colors for better readability
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    """Print a formatted step message"""
    print(f"{Colors.BLUE}{Colors.BOLD}[STEP]{Colors.ENDC} {message}")

def print_success(message):
    """Print a formatted success message"""
    print(f"{Colors.GREEN}{Colors.BOLD}[SUCCESS]{Colors.ENDC} {message}")

def print_error(message):
    """Print a formatted error message"""
    print(f"{Colors.RED}{Colors.BOLD}[ERROR]{Colors.ENDC} {message}")

def detect_root_directory():
    """Try to detect the project root directory"""
    # Start with the script directory
    script_dir = Path(__file__).parent.absolute()
    
    # Look for the project root - it's typically the parent of the installers directory
    # or where main.py exists, or where there's a git repository
    potential_root = script_dir.parent
    
    # Check if the potential root has a main.py file or a .git directory
    if (potential_root / "main.py").exists() or (potential_root / ".git").exists():
        return potential_root
    
    # If we can't detect it automatically, fall back to the actual root directory
    return Path("/")

def open_new_command_prompt(directory, venv_path):
    """Open a new command prompt in the specified directory with venv activated"""
    try:
        if platform.system() == "Windows":
            # For Windows, use start cmd with venv activation
            activate_cmd = str(venv_path / "Scripts" / "activate.bat")
            # Create a command that: 
            # 1. Changes to the root directory
            # 2. Activates the virtual environment
            # 3. Shows a success message
            cmd = f'start cmd /K "cd /d "{directory}" && call "{activate_cmd}" && echo Environment setup complete! && echo Virtual environment activated: {venv_path} && echo."'
            subprocess.Popen(cmd, shell=True)
        else:
            # For Unix-like systems, try to determine the default terminal
            terminal = None
            for term in ["gnome-terminal", "xterm", "konsole", "terminal"]:
                if shutil.which(term):
                    terminal = term
                    break
            
            if terminal:
                activate_cmd = str(venv_path / "bin" / "activate")
                if terminal == "gnome-terminal":
                    subprocess.Popen([terminal, "--", "bash", "-c", f"cd {directory} && source {activate_cmd} && echo 'Environment setup complete!' && echo 'Virtual environment activated: {venv_path}' && bash"])
                else:
                    subprocess.Popen([terminal, "-e", f"cd {directory} && source {activate_cmd} && echo 'Environment setup complete!' && echo 'Virtual environment activated: {venv_path}' && bash"], start_new_session=True)
            else:
                print_error("Couldn't detect a terminal emulator. Please open a new terminal manually.")
                print(f"Navigate to: {directory}")
                print(f"And activate the environment: source {venv_path}/bin/activate")
                return False
        return True
    except Exception as e:
        print_error(f"Failed to open a new command prompt: {e}")
        return False

def main():
    # Detect root directory
    script_dir = Path(__file__).parent.absolute()
    root_dir = detect_root_directory()
    
    print_step(f"Detected root directory: {root_dir}")
    
    # Define venv path in root directory
    venv_path = root_dir / ".venv"
    
    # Check if requirements.txt exists in the installers directory
    req_file = script_dir / "requirements.txt"
    if not req_file.exists():
        print_error(f"requirements.txt not found in {script_dir}")
        sys.exit(1)
    
    # Check if venv already exists
    if venv_path.exists():
        print(f"{Colors.YELLOW}Virtual environment already exists at {venv_path}{Colors.ENDC}")
        response = input("Do you want to remove it and create a new one? (y/n): ")
        if response.lower() == 'y':
            print_step(f"Removing existing virtual environment...")
            try:
                shutil.rmtree(venv_path)
            except Exception as e:
                print_error(f"Failed to remove existing environment: {e}")
                sys.exit(1)
        else:
            print("Using existing virtual environment.")
    
    # Create venv if it doesn't exist
    if not venv_path.exists():
        print_step("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            print_success(f"Virtual environment created at {venv_path}")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to create virtual environment: {e}")
            sys.exit(1)
    
    # Determine activation script path based on OS
    if platform.system() == "Windows":
        activate_script = venv_path / "Scripts" / "activate.bat"
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:  # Unix-like systems (Linux, macOS)
        activate_script = venv_path / "bin" / "activate"
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    if not activate_script.exists():
        print_error(f"Activation script not found at {activate_script}")
        sys.exit(1)
    
    print_step("Installing dependencies into the virtual environment...")
    print(f"{Colors.BLUE}Using pip from: {pip_exe}{Colors.ENDC}")
    try:
        if platform.system() == "Windows":
            # For Windows, use the pip.exe from the virtual environment
            print(f"{Colors.BLUE}Running: {pip_exe} install -r {req_file}{Colors.ENDC}")
            subprocess.run([str(pip_exe), "install", "-r", str(req_file)], check=True)
        else:
            # For Unix systems, we need to use a subshell with source
            cmd = f"source {activate_script} && pip install -r {req_file}"
            print(f"{Colors.BLUE}Running: {cmd}{Colors.ENDC}")
            subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)
        
        # Verify installation by checking pip list
        print_step("Verifying package installation...")
        if platform.system() == "Windows":
            subprocess.run([str(pip_exe), "list"], check=True)
        else:
            subprocess.run(f"source {activate_script} && pip list", shell=True, executable="/bin/bash", check=True)
            
        print_success("Dependencies installed successfully in the virtual environment!")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        sys.exit(1)
    
    # Print activation instructions
    print(f"\n{Colors.GREEN}{Colors.BOLD}Setup complete!{Colors.ENDC}")
    print(f"\nVirtual environment created at: {venv_path}")
    print("\nTo activate the virtual environment:")
    
    if platform.system() == "Windows":
        print(f"    {Colors.YELLOW}> {venv_path}\\Scripts\\activate{Colors.ENDC}")
    else:
        print(f"    {Colors.YELLOW}$ source {venv_path}/bin/activate{Colors.ENDC}")
    
    print("\nAfter activation, you can run the benchmark script from the project directory:")
    print(f"    {Colors.YELLOW}$ python main.py{Colors.ENDC}")
    
    # Open a new command prompt in the root directory
    print_step("Opening a new command prompt in the root directory...")
    if open_new_command_prompt(root_dir, venv_path):
        print_success("New command prompt opened with virtual environment activated.")
        
        # On Windows, close this window
        if platform.system() == "Windows":
            print(f"{Colors.YELLOW}This window will close in 3 seconds...{Colors.ENDC}")
            # Use a more reliable way to exit after delay
            subprocess.Popen('ping 127.0.0.1 -n 4 > nul && exit', shell=True)
        else:
            print("Setup complete. You can close this window.")
            # Just exit the script normally
            sys.exit(0)
    else:
        print("You can manually open a new command prompt in the root directory.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    print(f"{Colors.HEADER}{Colors.BOLD}FC6 Benchmark Environment Setup{Colors.ENDC}")
    print(f"{Colors.HEADER}Creating environment in root directory{Colors.ENDC}")
    main()