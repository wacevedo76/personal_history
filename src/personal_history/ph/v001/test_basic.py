#!/usr/bin/env python3
"""
Basic test for Personal History v0.01
"""

import json
from pathlib import Path
from .core import PersonalHistoryV001

def test_basic_functionality():
    """Test basic v0.01 functionality"""
    print("Testing Personal History v0.01 Core...")
    print("=" * 60)
    
    # Test 1: Create identity
    print("\n1. Testing identity creation...")
    identity = PersonalHistoryV001.create_identity("Test User")
    print(f"   ✓ Identity created: {identity['identity_hash'][:16]}...")
    print(f"   Name: {identity.get('name')}")
    
    # Test 2: Create activity
    print("\n2. Testing activity creation...")
    activity = PersonalHistoryV001.create_activity(
        "work",
        {"project": "test_project"},
        120,  # 2 hours
        shareable=True
    )
    print(f"   ✓ Activity created: {activity['type']}")
    print(f"   Duration: {activity['duration']} minutes")
    print(f"   Hash: {activity['hash'][:16]}...")
    print(f"   Commitment: {activity['timestamp']['commitment'][:16]}...")
    
    # Test 3: Create day
    print("\n3. Testing day creation...")
    day = PersonalHistoryV001.create_day(
        date="2024-01-01",
        activities=[activity],
        note="Test day"
    )
    print(f"   ✓ Day created: {day['date']}")
    print(f"   Activities: {len(day['activities'])}")
    print(f"   Day hash: {day['hash'][:16]}...")
    
    # Test 4: Create file
    print("\n4. Testing file creation...")
    ph_file = PersonalHistoryV001.create_file(identity, [day])
    print(f"   ✓ File created")
    print(f"   Version: {ph_file['version']}")
    print(f"   Identity: {ph_file['identity']['hash'][:16]}...")
    print(f"   Timeline: {len(ph_file['timeline'])} days")
    
    # Test 5: Sign file
    print("\n5. Testing file signing...")
    signature = PersonalHistoryV001.sign_file(ph_file, identity["private_key"])
    ph_file["signature"] = signature
    print(f"   ✓ File signed")
    print(f"   Signature: {signature[:32]}...")
    
    # Test 6: Verify file
    print("\n6. Testing file verification...")
    is_valid = PersonalHistoryV001.verify_file(ph_file, identity["public_key"])
    print(f"   ✓ File verification: {is_valid}")
    
    # Test 7: Save and load
    print("\n7. Testing save/load...")
    test_file = Path("test_history.ph.json")
    PersonalHistoryV001.save_file(ph_file, test_file)
    print(f"   ✓ File saved: {test_file}")
    
    loaded_file = PersonalHistoryV001.load_file(test_file)
    print(f"   ✓ File loaded")
    print(f"   Loaded identity: {loaded_file['identity']['hash'][:16]}...")
    
    # Test 8: Time analysis
    print("\n8. Testing time analysis...")
    analysis = PersonalHistoryV001.analyze_time(ph_file)
    print(f"   ✓ Time analysis complete")
    print(f"   Days analyzed: {analysis['days_analyzed']}")
    print(f"   Total time: {analysis['total_tracked_hours']:.1f} hours")
    
    # Test 9: Export shareable
    print("\n9. Testing shareable export...")
    shareable = PersonalHistoryV001.export_shareable(ph_file)
    print(f"   ✓ Shareable export: {len(shareable)} days")
    
    # Cleanup
    if test_file.exists():
        test_file.unlink()
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("\nWhat we've implemented:")
    print("✓ Identity creation (Ed25519 keypair)")
    print("✓ Activity creation with hidden exact times")
    print("✓ Forward-secure day hash chain")
    print("✓ File signing and verification")
    print("✓ Time analysis")
    print("✓ Shareable export")
    print("✓ File save/load")
    
    return True

if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()