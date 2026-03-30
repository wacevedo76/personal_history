#!/usr/bin/env python3
"""
Simple test script that doesn't require pytest.
"""

import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ph.v001.schema import validate_ph_file, PHValidationError
from ph.v001.core import PersonalHistoryV001


def test_schema_validation():
    """Test schema validation."""
    print("Testing schema validation...")
    
    # Test 1: Minimal valid file
    data = {
        'version': '0.01.0',
        'identity': {'hash': 'a' * 64},
        'timeline': [],
        'signature': 'b' * 128
    }
    
    try:
        result = validate_ph_file(data)
        print("✅ Test 1: Minimal valid file - PASS")
    except PHValidationError as e:
        print(f"❌ Test 1: Minimal valid file - FAIL: {e}")
        return False
    
    # Test 2: Invalid version
    data_invalid_version = {
        'version': '1.0.0',
        'identity': {'hash': 'a' * 64},
        'timeline': [],
        'signature': 'b' * 128
    }
    
    try:
        validate_ph_file(data_invalid_version)
        print("❌ Test 2: Invalid version - FAIL: Should have raised error")
        return False
    except PHValidationError as e:
        if "version" in str(e).lower():
            print("✅ Test 2: Invalid version - PASS")
        else:
            print(f"❌ Test 2: Invalid version - FAIL: Wrong error: {e}")
            return False
    
    # Test 3: Missing required field
    data_missing_field = {
        'version': '0.01.0',
        'identity': {'hash': 'a' * 64},
        # Missing timeline
        'signature': 'b' * 128
    }
    
    try:
        validate_ph_file(data_missing_field)
        print("❌ Test 3: Missing field - FAIL: Should have raised error")
        return False
    except PHValidationError as e:
        if "timeline" in str(e).lower():
            print("✅ Test 3: Missing field - PASS")
        else:
            print(f"❌ Test 3: Missing field - FAIL: Wrong error: {e}")
            return False
    
    return True


def test_core_functionality():
    """Test core module functionality."""
    print("\nTesting core functionality...")
    
    try:
        # Test identity creation
        identity = PersonalHistoryV001.create_identity("Test User")
        print(f"✅ Identity created: {identity['identity_hash'][:16]}...")
        
        # Test activity creation
        activity = PersonalHistoryV001.create_activity(
            "work",
            {"project": "test"},
            120
        )
        print(f"✅ Activity created: {activity['type']}")
        
        # Test day creation
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity]
        )
        print(f"✅ Day created: {day['date']}")
        
        # Test file creation
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        print(f"✅ File created with {len(ph_file['timeline'])} days")
        
        # The created file has signature: None, need to add a dummy signature for validation
        ph_file["signature"] = "c" * 128
        
        # Validate the created file
        validate_ph_file(ph_file)
        print("✅ Created file passes schema validation (with dummy signature)")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Personal History Test Suite")
    print("=" * 60)
    
    schema_ok = test_schema_validation()
    core_ok = test_core_functionality()
    
    print("\n" + "=" * 60)
    if schema_ok and core_ok:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())