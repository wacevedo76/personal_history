"""
Integration tests for Personal History core module.
Tests the existing core.py functionality with pytest.
"""

import pytest
import json
from pathlib import Path
from ph.v001.core import PersonalHistoryV001
from ph.v001.schema import validate_ph_file


class TestCoreIntegration:
    """Integration tests for core module."""
    
    def test_create_identity(self):
        """Test identity creation."""
        identity = PersonalHistoryV001.create_identity("Test User")
        
        assert "identity_hash" in identity
        assert "name" in identity
        assert identity["name"] == "Test User"
        assert len(identity["identity_hash"]) == 64
        assert all(c in "0123456789abcdef" for c in identity["identity_hash"])
        
        # Should have private key for signing
        assert "private_key" in identity
        assert "public_key" in identity
    
    def test_create_activity(self):
        """Test activity creation."""
        activity = PersonalHistoryV001.create_activity(
            "work",
            {"project": "test_project"},
            120,  # 2 hours
            shareable=True
        )
        
        assert activity["type"] == "work"
        assert activity["data"] == {"project": "test_project"}
        assert activity["duration"] == 120
        assert activity["shareable"] is True
        assert "hash" in activity
        assert len(activity["hash"]) == 64
        assert "timestamp" in activity
        assert "commitment" in activity["timestamp"]
        assert len(activity["timestamp"]["commitment"]) == 64
    
    def test_create_day(self):
        """Test day creation."""
        activity = PersonalHistoryV001.create_activity(
            "learning",
            {"topic": "testing"},
            90
        )
        
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity],
            note="Test day"
        )
        
        assert day["date"] == "2024-01-01"
        assert len(day["activities"]) == 1
        assert day["activities"][0]["type"] == "learning"
        assert "hash" in day
        assert len(day["hash"]) == 64
        assert day["note"] == "Test day"
    
    def test_create_and_validate_file(self):
        """Test creating a valid PH file that passes schema validation."""
        identity = PersonalHistoryV001.create_identity("Test User")
        activity = PersonalHistoryV001.create_activity(
            "work",
            {"project": "integration_test"},
            180
        )
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity]
        )
        
        # Create file without signature first
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Should pass schema validation
        assert validate_ph_file(ph_file) is True
        
        # Check structure
        assert ph_file["version"] == "0.01.0"
        assert ph_file["identity"]["hash"] == identity["identity_hash"]
        assert len(ph_file["timeline"]) == 1
        assert ph_file["timeline"][0]["date"] == "2024-01-01"
    
    @pytest.mark.skipif(not PersonalHistoryV001._crypto_available(),
                       reason="Cryptography library not available")
    def test_sign_and_verify_file(self):
        """Test file signing and verification (requires cryptography)."""
        identity = PersonalHistoryV001.create_identity("Test User")
        activity = PersonalHistoryV001.create_activity(
            "family",
            {"event": "dinner"},
            60
        )
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity]
        )
        
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Sign the file
        signature = PersonalHistoryV001.sign_file(ph_file, identity["private_key"])
        ph_file["signature"] = signature
        
        # Verify the signature
        is_valid = PersonalHistoryV001.verify_file(ph_file, identity["public_key"])
        assert is_valid is True
        
        # Should pass schema validation
        assert validate_ph_file(ph_file) is True
    
    def test_save_and_load_file(self, tmp_path):
        """Test saving and loading PH files."""
        identity = PersonalHistoryV001.create_identity("Test User")
        activity = PersonalHistoryV001.create_activity(
            "planning",
            {"goal": "test_saving"},
            45
        )
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity]
        )
        
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Save to file
        file_path = tmp_path / "test.ph.json"
        PersonalHistoryV001.save_file(ph_file, file_path)
        
        assert file_path.exists()
        
        # Load from file
        loaded_file = PersonalHistoryV001.load_file(file_path)
        
        # Should be identical (except signature if not present)
        assert loaded_file["version"] == ph_file["version"]
        assert loaded_file["identity"]["hash"] == ph_file["identity"]["hash"]
        assert len(loaded_file["timeline"]) == len(ph_file["timeline"])
    
    def test_analyze_time(self):
        """Test time analysis functionality."""
        identity = PersonalHistoryV001.create_identity("Test User")
        
        # Create multiple activities
        activities = [
            PersonalHistoryV001.create_activity("work", {"task": "coding"}, 120),
            PersonalHistoryV001.create_activity("learning", {"topic": "python"}, 60),
            PersonalHistoryV001.create_activity("health", {"exercise": "walk"}, 30)
        ]
        
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=activities
        )
        
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Analyze time
        analysis = PersonalHistoryV001.analyze_time(ph_file)
        
        assert analysis["days_analyzed"] == 1
        assert analysis["total_tracked_hours"] == 3.5  # 210 minutes = 3.5 hours
        assert "by_type" in analysis
        assert "work" in analysis["by_type"]
        assert "learning" in analysis["by_type"]
        assert "health" in analysis["by_type"]
    
    def test_export_shareable(self):
        """Test shareable export functionality."""
        identity = PersonalHistoryV001.create_identity("Test User")
        
        # Create mixed activities (shareable and private)
        activities = [
            PersonalHistoryV001.create_activity("work", {"project": "public"}, 120, shareable=True),
            PersonalHistoryV001.create_activity("health", {"issue": "private"}, 60, shareable=False),
            PersonalHistoryV001.create_activity("family", {"event": "dinner"}, 90, shareable=True)
        ]
        
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=activities
        )
        
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Export shareable
        shareable = PersonalHistoryV001.export_shareable(ph_file)
        
        # Should only include shareable activities
        assert len(shareable) == 1  # One day
        day_activities = shareable[0]["activities"]
        assert len(day_activities) == 2  # Only work and family (not health)
        
        activity_types = {a["type"] for a in day_activities}
        assert "work" in activity_types
        assert "family" in activity_types
        assert "health" not in activity_types
        
        # All exported activities should be shareable
        for activity in day_activities:
            assert activity.get("shareable", True) is True