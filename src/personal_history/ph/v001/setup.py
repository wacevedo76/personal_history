#!/usr/bin/env python3
"""
NOTE: Install from the personal_history root directory, not from here!

Correct installation:
cd /path/to/personal_history  # Go UP two directories
pip install -e .

This setup.py exists only to help with development tools.
"""

import sys
import os

print("=" * 60)
print("ERROR: Don't install from this directory!")
print("=" * 60)
print("\nInstall from the personal_history root directory:")
print("\n  cd /path/to/personal_history")
print("  pip install -e .")
print("\nOr use the development script:")
print("\n  python3 dev_setup.py")
print("\n" + "=" * 60)

# Try to find the root
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))

if os.path.exists(os.path.join(root_dir, "setup.py")):
    print(f"\nRoot directory appears to be: {root_dir}")
    print(f"Try: cd {root_dir} && pip install -e .")

sys.exit(1)