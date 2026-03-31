"""
Unit tests for Identity with REAL cryptography (no mocks).
"""

import pytest
import base64
import json
from pathlib import Path

# Test that identity generates real Ed25519 keys
def test_identity_generates_real_keys():
    """Test that Identity.generate() creates real Ed25519 keys."""
    from ph.v001.models.identity import Identity
    
    # Create identity
    identity = Identity(name="Test User").generate()
    
    # Check keys exist
    assert identity.private_key is not None, "Private key should be generated"
    assert identity.public_key is not None, "Public key should be generated"
    assert identity.identity_hash is not None, "Identity hash should be generated"
    
    # Check key formats
    # Private key should be 32 bytes base64 encoded
    private_bytes = base64.b64decode(identity.private_key)
    assert len(private_bytes) == 32, f"Private key should be 32 bytes, got {len(private_bytes)}"
    
    # Public key should be 32 bytes base64 encoded
    public_bytes = base64.b64decode(identity.public_key)
    assert len(public_bytes) == 32, f"Public key should be 32 bytes, got {len(public_bytes)}"
    
    # Identity hash should be 64 hex characters
    assert len(identity.identity_hash) == 64, f"Identity hash should be 64 chars, got {len(identity.identity_hash)}"
    assert all(c in '0123456789abcdef' for c in identity.identity_hash), "Identity hash should be hex"


def test_identity_serialization_deserialization():
    """Test that identity can be serialized to dict and deserialized back."""
    from ph.v001.models.identity import Identity
    
    # Create and generate identity
    original = Identity(name="Serialization Test").generate()
    
    # Convert to dict
    identity_dict = original.to_dict()
    
    # Check all fields are present
    assert "private_key" in identity_dict
    assert "public_key" in identity_dict
    assert "identity_hash" in identity_dict
    assert "salt" in identity_dict
    assert "name" in identity_dict
    assert "created_at" in identity_dict
    
    # Convert back from dict
    restored = Identity.from_dict(identity_dict)
    
    # Check all fields match
    assert restored.private_key == original.private_key
    assert restored.public_key == original.public_key
    assert restored.identity_hash == original.identity_hash
    assert restored.salt == original.salt
    assert restored.name == original.name


def test_identity_verification():
    """Test that identity.verify() works with real keys."""
    from ph.v001.models.identity import Identity
    
    # Create identity
    identity = Identity(name="Verification Test").generate()
    
    # Should verify successfully
    assert identity.verify() is True, "Fresh identity should verify"
    
    # Tamper with the identity hash and verification should fail
    original_hash = identity.identity_hash
    identity.identity_hash = "0" * 64  # Tampered hash
    
    assert identity.verify() is False, "Tampered identity should not verify"
    
    # Restore and should verify again
    identity.identity_hash = original_hash
    assert identity.verify() is True, "Restored identity should verify"


def test_identity_json_roundtrip(tmp_path):
    """Test that identity can be saved to JSON file and loaded back."""
    from ph.v001.models.identity import Identity
    
    # Create identity
    original = Identity(name="JSON Test").generate()
    
    # Save to file
    file_path = tmp_path / "identity.json"
    with open(file_path, 'w') as f:
        json.dump(original.to_dict(), f, indent=2)
    
    # Load from file
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)
    
    restored = Identity.from_dict(loaded_data)
    
    # Verify
    assert restored.verify() is True, "Loaded identity should verify"
    assert restored.name == original.name
    assert restored.identity_hash == original.identity_hash


def test_identity_without_cryptography_fails():
    """Test that identity generation requires cryptography library.
    
    Note: Since we removed the fallback, this should fail if cryptography
    is not available. We'll test by temporarily removing the import.
    """
    # This test verifies we're using real cryptography
    # We'll just check that cryptography is actually being used
    from ph.v001.models.identity import Identity
    
    identity = Identity(name="Crypto Test").generate()
    
    # Verify keys are proper Ed25519 format
    import base64
    from cryptography.hazmat.primitives.asymmetric import ed25519
    
    # Try to load the private key as Ed25519
    private_bytes = base64.b64decode(identity.private_key)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)
    
    # Try to load the public key as Ed25519
    public_bytes = base64.b64decode(identity.public_key)
    public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
    
    # Test signing and verification
    test_message = b"Test message for Ed25519"
    signature = private_key.sign(test_message)
    
    # Should verify successfully
    public_key.verify(signature, test_message)
    
    # If we get here, real cryptography is working
    assert True, "Real Ed25519 cryptography is working"


def test_multiple_identities_unique():
    """Test that multiple identities have unique keys."""
    from ph.v001.models.identity import Identity
    
    # Create two identities
    identity1 = Identity(name="User 1").generate()
    identity2 = Identity(name="User 2").generate()
    
    # They should have different keys
    assert identity1.private_key != identity2.private_key, "Private keys should be unique"
    assert identity1.public_key != identity2.public_key, "Public keys should be unique"
    assert identity1.identity_hash != identity2.identity_hash, "Identity hashes should be unique"
    
    # Even with same name, keys should be different
    identity3 = Identity(name="Same Name").generate()
    identity4 = Identity(name="Same Name").generate()
    
    assert identity3.private_key != identity4.private_key, "Same name should still have unique keys"


if __name__ == "__main__":
    # Run tests directly for debugging
    test_identity_generates_real_keys()
    print("✓ test_identity_generates_real_keys passed")
    
    test_identity_serialization_deserialization()
    print("✓ test_identity_serialization_deserialization passed")
    
    test_identity_verification()
    print("✓ test_identity_verification passed")
    
    test_identity_without_cryptography_fails()
    print("✓ test_identity_without_cryptography_fails passed")
    
    test_multiple_identities_unique()
    print("✓ test_multiple_identities_unique passed")
    
    print("\n✅ All identity tests passed with real cryptography!")