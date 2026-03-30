"""
Unit tests for schema validation of Personal History Format v0.01.
"""

import pytest
import json
from pathlib import Path
from ph.v001.schema import validate_ph_file, PHValidationError, validate_ph_file_with_warnings


class TestSchemaValidation:
    """Test schema validation for PH files."""
    
    def test_validates_minimal_file(self, minimal_valid_ph):
        """Test with minimal valid PH file."""
        assert validate_ph_file(minimal_valid_ph) is True
    
    def test_rejects_missing_version(self):
        """Test missing required version field."""
        ph_missing_version = {
            "identity": {"hash": "a" * 64},
            "timeline": [],
            "signature": "b" * 128
        }
        with pytest.raises(PHValidationError, match="version"):
            validate_ph_file(ph_missing_version)
    
    def test_validates_version_format(self):
        """Version must be exactly '0.01.0'."""
        invalid_version = {
            "version": "1.0.0",
            "identity": {"hash": "a" * 64},
            "timeline": [],
            "signature": "b" * 128
        }
        with pytest.raises(PHValidationError, match="version"):
            validate_ph_file(invalid_version)
    
    def test_validates_identity_hash_format(self):
        """Identity hash must be 64 hex chars."""
        ph_invalid_hash = {
            "version": "0.01.0",
            "identity": {
                "hash": "invalid",  # Not 64 hex chars
                "name": "Test User"
            },
            "timeline": [],
            "signature": "b" * 128
        }
        with pytest.raises(PHValidationError, match="hash"):
            validate_ph_file(ph_invalid_hash)
    
    def test_validates_date_formats(self):
        """Dates must be YYYY-MM-DD format."""
        ph_invalid_date = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [
                {
                    "date": "2024/01/01",  # Wrong format
                    "activities": [],
                    "hash": "c" * 64
                }
            ],
            "signature": "b" * 128
        }
        with pytest.raises(PHValidationError, match="date"):
            validate_ph_file(ph_invalid_date)
    
    def test_validates_activity_types(self):
        """Activity types must be from allowed set."""
        ph_invalid_activity_type = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [
                {
                    "date": "2024-01-01",
                    "activities": [
                        {
                            "type": "invalid_type",  # Not in allowed set
                            "data": {},
                            "duration": 60,
                            "shareable": True,
                            "hash": "d" * 64
                        }
                    ],
                    "hash": "c" * 64
                }
            ],
            "signature": "b" * 128
        }
        with pytest.raises(PHValidationError, match="activity type"):
            validate_ph_file(ph_invalid_activity_type)
    
    def test_validates_hash_format(self):
        """Hashes must be 64 hex characters."""
        ph_invalid_hash_format = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [
                {
                    "date": "2024-01-01",
                    "activities": [],
                    "hash": "invalid"  # Not 64 hex chars
                }
            ],
            "signature": "b" * 128
        }
        with pytest.raises(PHValidationError, match="hash"):
            validate_ph_file(ph_invalid_hash_format)
    
    def test_validates_signature_format(self):
        """Signature must be 128 hex characters."""
        ph_invalid_signature_format = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [],
            "signature": "invalid"  # Not 128 hex chars
        }
        with pytest.raises(PHValidationError, match="signature"):
            validate_ph_file(ph_invalid_signature_format)
    
    def test_identity_requires_hash(self):
        """Identity must have hash field."""
        ph_identity_missing_hash = {
            "version": "0.01.0",
            "identity": {
                "name": "Test User"  # Missing hash
            },
            "timeline": [],
            "signature": "b" * 128
        }
        with pytest.raises(PHValidationError, match="hash"):
            validate_ph_file(ph_identity_missing_hash)
    
    def test_validates_example_file(self, example_william_ph):
        """Validate the example William PH file."""
        assert validate_ph_file(example_william_ph) is True
    
    def test_validates_with_warnings(self):
        """Test validation with warnings for non-chronological dates."""
        ph_with_warning = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [
                {
                    "date": "2024-01-02",
                    "activities": [],
                    "hash": "b" * 64
                },
                {
                    "date": "2024-01-01",  # Out of order
                    "activities": [],
                    "hash": "c" * 64
                }
            ],
            "signature": "d" * 128
        }
        
        result = validate_ph_file_with_warnings(ph_with_warning)
        assert result.valid is True
        assert len(result.warnings) > 0
        assert "chronological" in result.warnings[0].lower()
    
    def test_validates_timeline_gap_warning(self):
        """Test warning for gaps in timeline."""
        ph_with_gap = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [
                {
                    "date": "2024-01-01",
                    "activities": [],
                    "hash": "b" * 64
                },
                {
                    "date": "2024-01-05",  # 3 day gap
                    "activities": [],
                    "hash": "c" * 64
                }
            ],
            "signature": "d" * 128
        }
        
        result = validate_ph_file_with_warnings(ph_with_gap)
        assert result.valid is True
        assert len(result.warnings) > 0
        assert "gap" in result.warnings[0].lower()
    
    def test_validates_activity_duration_positive(self):
        """Activity duration must be positive."""
        ph_negative_duration = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [
                {
                    "date": "2024-01-01",
                    "activities": [
                        {
                            "type": "work",
                            "data": {},
                            "duration": -10,  # Negative!
                            "hash": "b" * 64
                        }
                    ],
                    "hash": "c" * 64
                }
            ],
            "signature": "d" * 128
        }
        
        with pytest.raises(PHValidationError, match="duration"):
            validate_ph_file(ph_negative_duration)
    
    def test_validates_shareable_flag_boolean(self):
        """Shareable flag must be boolean if present."""
        ph_invalid_shareable = {
            "version": "0.01.0",
            "identity": {"hash": "a" * 64},
            "timeline": [
                {
                    "date": "2024-01-01",
                    "activities": [
                        {
                            "type": "work",
                            "data": {},
                            "duration": 60,
                            "shareable": "yes",  # Not boolean
                            "hash": "b" * 64
                        }
                    ],
                    "hash": "c" * 64
                }
            ],
            "signature": "d" * 128
        }
        
        with pytest.raises(PHValidationError, match="shareable"):
            validate_ph_file(ph_invalid_shareable)