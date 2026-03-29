#!/usr/bin/env python3
"""
Development setup script for Personal History
Run this from ANY directory within the project
"""

import os
import sys
import subprocess

def find_root():
    """Find the personal_history root directory"""
    # Start from current directory and go up
    current = os.path.abspath(".")
    
    while current != "/":
        if os.path.exists(os.path.join(current, "setup.py")):
            # Check if this looks like our root
            with open(os.path.join(current, "setup.py"), "r") as f:
                content = f.read()
                if "personal-history" in content:
                    return current
        current = os.path.dirname(current)
    
    # Try common locations
    for path in [
        os.path.dirname(os.path.abspath(__file__)),
        os.path.join(os.path.expanduser("~"), "code", "Testing", "personal_history"),
        os.path.join(os.path.expanduser("~"), "personal_history"),
        "/home/wacevedo/code/Testing/personal_history",
    ]:
        if os.path.exists(os.path.join(path, "setup.py")):
            return path
    
    return None

def main():
    print("Personal History Development Setup")
    print("=" * 60)
    
    # Find root directory
    root = find_root()
    if not root:
        print("❌ Could not find personal_history root directory")
        print("\nPlease navigate to the personal_history directory manually:")
        print("  cd /path/to/personal_history")
        print("  pip install -e .")
        return 1
    
    print(f"✓ Found root directory: {root}")
    
    # Check if we're already in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        print("\n⚠️  Not in a virtual environment")
        print("Recommended: Create and activate virtual environment first:")
        print(f"  cd {root}")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate  # Linux/Mac")
        print("  venv\\Scripts\\activate   # Windows")
        print("\nContinue without virtual environment? (y/N): ", end="")
        if input().lower() != 'y':
            return 0
    
    # Change to root directory
    os.chdir(root)
    print(f"\n✓ Changed to: {os.getcwd()}")
    
    # Install the package
    print("\nInstalling personal-history package...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Installation successful!")
            print("\n" + "=" * 60)
            print("Quick test commands:")
            print("  ph --help           # Show all commands")
            print("  ph demo             # Run demonstration")
            print("  ph init --name \"Test\"  # Create identity")
            print("\nDevelopment commands:")
            print("  # Edit files in personal_history/ph/v001/")
            print("  # Changes are immediately available!")
            print("  # No need to reinstall")
        else:
            print("❌ Installation failed:")
            print(result.stderr)
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())