"""
Unit tests for file signing and verification with REAL cryptography.
"""

import pytest
import json
import base64
import tempfile
import shutil
from pathlib import Path
import datetime

# Test file signing with real cryptography
def test_file_signing_creates_real_signature():
    """Test that PersonalHistoryFile.sign() creates real Ed25519 signatures."""
    from ph.v001.models.identity import Identity
    from ph.v001.models.file import PersonalHistoryFile
    from ph.v001.models.day import Day
    from ph.v001.models.activity import Activity
    
    # Create identity with real keys
    identity = Identity(name="Signing Test").generate()
    
    # Create a simple file with one activity
    today = datetime.date.today().isoformat()
    activity = Activity(
        activity_type="work",
        data={"project": "Test"},
        duration=30,
        shareable=True
    )
    
    day = Day(date=today, activities=[activity])
    ph_file = PersonalHistoryFile(identity=identity, timeline=[day])
    
    # Sign the file
    assert ph_file.sign() is True, "File signing should succeed"
    assert ph_file.signature is not None, "Signature should be created"
    
    # Check signature format
    sig = ph_file.signature
    assert len(sig) > 0, "Signature should not be empty"
    
    # Should be either 128 hex chars or base64
    import re
    hex_pattern = re.compile(r'^[a-f0-9]{128}$')
    base64_pattern = re.compile(r'^[A-Za-z0-9+/]{86,88}={0,2}$')
    
    assert hex_pattern.match(sig) or base64_pattern.match(sig), \
        f"Signature should be 128 hex chars or base64, got: {sig[:50]}..."
    
    # If base64, decode and check it's 64 bytes
    if base64_pattern.match(sig):
        decoded = base64.b64decode(sig)
        assert len(decoded) == 64, f"Ed25519 signature should be 64 bytes, got {len(decoded)}"


def test_file_verification_with_real_crypto():
    """Test that file verification works with real cryptography."""
    from ph.v001.models.identity import Identity
    from ph.v001.models.file import PersonalHistoryFile
    from ph.v001.models.day import Day
    from ph.v001.models.activity import Activity
    import tempfile
    
    # Create identity with real keys
    identity = Identity(name="Verification Test").generate()
    
    # Save identity to temp file for verification
    temp_dir = Path(tempfile.mkdtemp())
    try:
        identity_file = temp_dir / "identity.json"
        with open(identity_file, 'w') as f:
            json.dump(identity.to_dict(), f, indent=2)
        
        # Create and sign a file
        today = datetime.date.today().isoformat()
        activity = Activity(
            activity_type="learning",
            data={"topic": "Cryptography"},
            duration=45,
            shareable=True
        )
        
        day = Day(date=today, activities=[activity])
        ph_file = PersonalHistoryFile(identity=identity, timeline=[day])
        
        assert ph_file.sign() is True, "Should sign successfully"
        
        # Verify signature
        assert ph_file.verify_signature(identity_file_path=identity_file) is True, \
            "Signature verification should pass"
        
        # Tamper with the file and verification should fail
        original_signature = ph_file.signature
        ph_file.signature = "a" * 128  # Wrong signature
        
        assert ph_file.verify_signature(identity_file_path=identity_file) is False, \
            "Tampered signature should fail verification"
        
        # Restore and should verify again
        ph_file.signature = original_signature
        assert ph_file.verify_signature(identity_file_path=identity_file) is True, \
            "Restored signature should verify"
            
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_file_save_load_roundtrip():
    """Test that file can be saved to disk and loaded back with valid signature."""
    from ph.v001.models.identity import Identity
    from ph.v001.models.file import PersonalHistoryFile
    from ph.v001.models.day import Day
    from ph.v001.models.activity import Activity
    import tempfile
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        # Create identity and save it
        identity = Identity(name="Roundtrip Test").generate()
        identity_file = temp_dir / "identity.json"
        with open(identity_file, 'w') as f:
            json.dump(identity.to_dict(), f, indent=2)
        
        # Create file
        today = datetime.date.today().isoformat()
        activity1 = Activity(
            activity_type="work",
            data={"project": "Project A"},
            duration=120,
            shareable=True
        )
        activity2 = Activity(
            activity_type="health",
            data={"exercise": "Running"},
            duration=60,
            shareable=True
        )
        
        day = Day(date=today, activities=[activity1, activity2])
        original_file = PersonalHistoryFile(identity=identity, timeline=[day])
        
        # Sign and save
        assert original_file.sign() is True
        output_file = temp_dir / "test.ph.json"
        original_file.save(output_file)
        
        # Load back
        loaded_file = PersonalHistoryFile.load(output_file)
        
        # Verify signature
        assert loaded_file.verify_signature(identity_file_path=identity_file) is True, \
            "Loaded file should have valid signature"
        
        # Check data integrity
        assert len(loaded_file.timeline) == 1
        assert loaded_file.timeline[0].date == today
        assert len(loaded_file.timeline[0].activities) == 2
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_file_hash_consistency():
    """Test that file hash calculation is consistent for same content."""
    from ph.v001.models.identity import Identity
    from ph.v001.models.file import PersonalHistoryFile
    from ph.v001.models.day import Day
    from ph.v001.models.activity import Activity
    
    # Create two identical files
    identity = Identity(name="Hash Test").generate()
    
    today = datetime.date.today().isoformat()
    activity = Activity(
        activity_type="work",
        data={"project": "Test"},
        duration=30,
        shareable=True
    )
    
    day = Day(date=today, activities=[activity])
    
    file1 = PersonalHistoryFile(identity=identity, timeline=[day])
    file2 = PersonalHistoryFile(identity=identity, timeline=[day])
    
    # Calculate hashes
    hash1 = file1.calculate_file_hash()
    hash2 = file2.calculate_file_hash()
    
    # Should be identical
    assert hash1 == hash2, "Same content should produce same hash"
    
    # Sign both files
    assert file1.sign() is True
    assert file2.sign() is True
    
    # Signatures should be identical (same content, same key)
    assert file1.signature == file2.signature, "Same content with same key should produce same signature"


def test_file_with_multiple_days():
    """Test signing and verification with multiple days."""
    from ph.v001.models.identity import Identity
    from ph.v001.models.file import PersonalHistoryFile
    from ph.v001.models.day import Day
    from ph.v001.models.activity import Activity
    import tempfile
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        identity = Identity(name="Multi-Day Test").generate()
        identity_file = temp_dir / "identity.json"
        with open(identity_file, 'w') as f:
            json.dump(identity.to_dict(), f, indent=2)
        
        # Create activities for multiple days
        activities = []
        for i in range(3):
            date = f"2024-01-{i+1:02d}"
            day_activities = [
                Activity(
                    activity_type="work",
                    data={"project": f"Project {i}"},
                    duration=60 * (i + 1),  # 60, 120, 180 minutes
                    shareable=True
                )
            ]
            day = Day(date=date, activities=day_activities)
            activities.append(day)
        
        # Create and sign file
        ph_file = PersonalHistoryFile(identity=identity, timeline=activities)
        assert ph_file.sign() is True
        
        # Save and load
        output_file = temp_dir / "multi_day.ph.json"
        ph_file.save(output_file)
        
        loaded_file = PersonalHistoryFile.load(output_file)
        
        # Verify
        assert loaded_file.verify_signature(identity_file_path=identity_file) is True
        assert len(loaded_file.timeline) == 3
        
        # Check day order is preserved
        dates = [day.date for day in loaded_file.timeline]
        assert dates == ["2024-01-01", "2024-01-02", "2024-01-03"]
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_unsigned_file_verification():
    """Test that file without signature verification returns False."""
    from ph.v001.models.identity import Identity
    from ph.v001.models.file import PersonalHistoryFile
    from ph.v001.models.day import Day
    from ph.v001.models.activity import Activity
    import tempfile
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        identity = Identity(name="Unsigned Test").generate()
        identity_file = temp_dir / "identity.json"
        with open(identity_file, 'w') as f:
            json.dump(identity.to_dict(), f, indent=2)
        
        # Create file without signing
        today = datetime.date.today().isoformat()
        activity = Activity(
            activity_type="work",
            data={"project": "Test"},
            duration=30,
            shareable=True
        )
        
        day = Day(date=today, activities=[activity])
        ph_file = PersonalHistoryFile(identity=identity, timeline=[day])
        
        # No signature, verification should return False
        assert ph_file.verify_signature(identity_file_path=identity_file) is False
        
        # Save without signature
        output_file = temp_dir / "unsigned.ph.json"
        ph_file.save(output_file)
        
        # Load and check no signature
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert "signature" not in data, "Unsigned file should not have signature"
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    # Run tests directly
    test_file_signing_creates_real_signature()
    print("✓ test_file_signing_creates_real_signature passed")
    
    test_file_verification_with_real_crypto()
    print("✓ test_file_verification_with_real_crypto passed")
    
    test_file_save_load_roundtrip()
    print("✓ test_file_save_load_roundtrip passed")
    
    test_file_hash_consistency()
    print("✓ test_file_hash_consistency passed")
    
    test_file_with_multiple_days()
    print("✓ test_file_with_multiple_days passed")
    
    test_unsigned_file_verification()
    print("✓ test_unsigned_file_verification passed")
    
    print("\n✅ All file signing tests passed with real cryptography!")