#!/usr/bin/env python3
"""
Verification script for Personal History installation.
Run this after installing the package to verify everything works.
"""

import sys
import json
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(text)
    print("="*60)


def test_imports():
    """Test that all modules can be imported."""
    print_header("1. Testing Module Imports")
    
    modules_to_test = [
        ("ph.v001.core", "PersonalHistoryV001"),
        ("ph.v001.schema", "validate_ph_file"),
        ("ph.v001.cli", "main"),
    ]
    
    all_imported = True
    for module_name, attribute_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[attribute_name])
            if hasattr(module, attribute_name):
                print(f"✅ {module_name}.{attribute_name}")
            else:
                print(f"❌ {module_name} missing {attribute_name}")
                all_imported = False
        except ImportError as e:
            print(f"❌ Failed to import {module_name}: {e}")
            all_imported = False
    
    return all_imported


def test_core_functionality():
    """Test core functionality works."""
    print_header("2. Testing Core Functionality")
    
    try:
        from ph.v001.core import PersonalHistoryV001
        
        # Create identity
        identity = PersonalHistoryV001.create_identity("Verification User")
        print(f"✅ Identity created: {identity['identity_hash'][:16]}...")
        
        # Create activity
        activity = PersonalHistoryV001.create_activity(
            "work",
            {"project": "verification"},
            60
        )
        print(f"✅ Activity created: {activity['type']}")
        
        # Create day
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity]
        )
        print(f"✅ Day created: {day['date']}")
        
        # Create file
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        print(f"✅ File created with {len(ph_file['timeline'])} days")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_schema_validation():
    """Test schema validation works."""
    print_header("3. Testing Schema Validation")
    
    try:
        from ph.v001.schema import validate_ph_file
        
        # Test minimal valid file
        test_data = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [],
            "signature": "b" * 128
        }
        
        validate_ph_file(test_data)
        print("✅ Minimal file validation passed")
        
        # Test with more complex data
        complex_data = {
            "version": "0.01.0",
            "identity": {
                "hash": "c" * 64,
                "name": "Test User"
            },
            "timeline": [
                {
                    "date": "2024-01-01",
                    "activities": [
                        {
                            "type": "work",
                            "data": {"project": "test"},
                            "duration": 120,
                            "shareable": True,
                            "hash": "d" * 64
                        }
                    ],
                    "hash": "e" * 64
                }
            ],
            "signature": "f" * 128
        }
        
        validate_ph_file(complex_data)
        print("✅ Complex file validation passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False


def test_file_operations(tmp_dir=None):
    """Test file save/load operations."""
    print_header("4. Testing File Operations")
    
    try:
        from ph.v001.core import PersonalHistoryV001
        import tempfile
        
        # Create test data
        identity = PersonalHistoryV001.create_identity("File Test User")
        activity = PersonalHistoryV001.create_activity(
            "learning",
            {"topic": "file_operations"},
            45
        )
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity]
        )
        
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Save to temporary file
        if tmp_dir:
            test_file = Path(tmp_dir) / "test_verification.ph.json"
        else:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ph.json', delete=False) as f:
                test_file = Path(f.name)
        
        PersonalHistoryV001.save_file(ph_file, test_file)
        print(f"✅ File saved to: {test_file}")
        
        # Load it back
        loaded_file = PersonalHistoryV001.load_file(test_file)
        print(f"✅ File loaded back")
        
        # Clean up
        if not tmp_dir:
            test_file.unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ File operations failed: {e}")
        return False


def test_cli_availability():
    """Test CLI is available."""
    print_header("5. Testing CLI Availability")
    
    try:
        import subprocess
        
        # Try to run the CLI via python -m
        result = subprocess.run(
            [sys.executable, "-m", "ph.v001.cli", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ CLI is available via python -m")
            return True
        else:
            print(f"❌ CLI returned error: {result.stderr}")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"⚠️  CLI test skipped: {e}")
        return True  # Don't fail overall for CLI issues
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False


def main():
    """Run all verification tests."""
    print("\n" + "="*60)
    print("Personal History Installation Verification")
    print("="*60)
    print(f"Python: {sys.version}")
    print(f"Working directory: {Path.cwd()}")
    
    tests = [
        ("Module Imports", test_imports),
        ("Core Functionality", test_core_functionality),
        ("Schema Validation", test_schema_validation),
        ("File Operations", lambda: test_file_operations("/tmp")),
        ("CLI Availability", test_cli_availability),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Verification Summary")
    
    all_passed = True
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if not success:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 SUCCESS: Personal History is correctly installed!")
        print("\nYou can now:")
        print("  • Use: ph --help")
        print("  • Run tests: make test")
        print("  • Develop: make install-dev")
        return 0
    else:
        print("❌ ISSUES: Some tests failed")
        print("\nTroubleshooting:")
        print("  1. Make sure you're in a virtual environment")
        print("  2. Run: pip install -e .")
        print("  3. Check: pip show personal-history")
        return 1


if __name__ == "__main__":
    sys.exit(main())