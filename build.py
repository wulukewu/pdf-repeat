#!/usr/bin/env python3
"""
Build script for PDF Repeat application
"""

import os
import sys
import subprocess
import platform

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("Building PDF Repeat application...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        if run_command("pip install pyinstaller") is None:
            print("Failed to install PyInstaller")
            return 1
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for path in ['build', 'dist']:
        if os.path.exists(path):
            run_command(f"rm -rf {path}")
    
    # Build the application
    print("Building with PyInstaller...")
    if run_command("pyinstaller pdf-repeat.spec") is None:
        print("Build failed")
        return 1
    
    # Check if build was successful
    exe_name = "pdf-repeat.exe" if platform.system() == "Windows" else "pdf-repeat"
    exe_path = os.path.join("dist", exe_name)
    
    if os.path.exists(exe_path):
        print(f"Build successful! Executable created at: {exe_path}")
        print(f"File size: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
        return 0
    else:
        print("Build failed - executable not found")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 