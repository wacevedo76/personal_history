#!/usr/bin/env python3
"""
Simple test runner for Personal History using pytest.
"""

import sys
import subprocess
from pathlib import Path


def run_pytest(args=None):
    """Run pytest with given arguments."""
    if args is None:
        args = []
    
    cmd = [sys.executable, "-m", "pytest"] + args
    
    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    print("=" * 60)
    return result.returncode


def main():
    """Main test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Personal History tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--cov", action="store_true", help="Run with coverage")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("test_path", nargs="?", help="Specific test file or directory")
    
    args = parser.parse_args()
    
    pytest_args = []
    
    if args.unit:
        pytest_args.append("tests/unit")
    elif args.integration:
        pytest_args.append("tests/integration")
    elif args.test_path:
        pytest_args.append(args.test_path)
    else:
        pytest_args.append("tests/")
    
    if args.cov:
        pytest_args.extend(["--cov=ph", "--cov-report=term-missing"])
    
    if args.verbose:
        pytest_args.append("-v")
    
    return run_pytest(pytest_args)


if __name__ == "__main__":
    sys.exit(main())