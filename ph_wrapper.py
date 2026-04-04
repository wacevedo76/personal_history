#!/usr/bin/env python3
"""
Wrapper script for Personal History CLI
Use this if the 'ph' entry point isn't created in editable mode.
"""

import sys
from personal_history.ph.v001.views.cli_view import main

if __name__ == "__main__":
    sys.exit(main())