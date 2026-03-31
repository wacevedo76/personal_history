"""
Integration tests for complete workflow with REAL cryptography.
"""

import pytest
import json
import tempfile
import shutil
import time
from pathlib import Path
import datetime

# Test complete workflow: identity → activity → sync → verify
def test_complete_workflow_with_real_crypto():
    """Test complete workflow with real cryptography."""
    from ph.v001.controllers.history_controller import HistoryController
    from ph.v001.models.activity import Activity
    
    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp())
    try:
        # Create controller
        controller = HistoryController(temp_dir)
        
        # 1. Create identity
        identity = controller.create_identity("Workflow Test User")
        controller.save_identity(identity)
        
        # Verify identity was saved
        identity_file = temp_dir / "identity.json"
        assert identity_file.exists()
        
        with open(identity_file, 'r') as f:
            saved_identity = json.load(f)
        
        assert saved_identity["name"] == "Workflow Test User"
        assert "public_key" in saved_identity
        assert "private_key" in saved_identity
        
        # 2. Create and add activity
        activity = controller.create_activity(
            activity_type="work",
            data={"project": "Workflow Test", "description": "Testing complete workflow"},
            duration=45,
            shareable=True
        )
        
        controller.add_to_pending(activity)
        
        # Verify pending was created
        pending_file = temp_dir / "pending.json"
        assert pending_file.exists()
        
        with open(pending_file, 'r') as f:
            pending = json.load(f)
        
        assert "activities" in pending
        assert len(pending["activities"]) > 0
        
        # 3. Sync to file
        output_file = temp_dir / "workflow_test.ph.json"
        ph_file = controller.sync_to_file(output_file=output_file)
        
        assert output_file.exists()
        assert ph_file.signature is not None
        
        # 4. Load and verify
        from ph.v001.models.file import PersonalHistoryFile
        from ph.v001.schema import validate_ph_file
        
        loaded_file = PersonalHistoryFile.load(output_file)
        
        # Validate schema
        with open(output_file, 'r') as f:
            file_data = json.load(f)
        
        assert validate_ph_file(file_data) is True, "File should pass schema validation"
        
        # Verify signature
        assert loaded_file.verify_signature(identity_file_path=identity_file) is True, \
            "Signature should verify"
        
        # 5. Check file contents
        assert loaded_file.identity.name == "Workflow Test User"
        assert len(loaded_file.timeline) == 1
        
        day = loaded_file.timeline[0]
        assert day.date == datetime.date.today().isoformat()
        assert len(day.activities) == 1
        
        saved_activity = day.activities[0]
        assert saved_activity.type == "work"
        assert saved_activity.duration == 45
        assert saved_activity.data["project"] == "Workflow Test"
        
        print("✓ Complete workflow test passed")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_multiple_activities_single_day():
    """Test adding multiple activities to a single day."""
    from ph.v001.controllers.history_controller import HistoryController
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        controller = HistoryController(temp_dir)
        
        # Create identity
        identity = controller.create_identity("Multi-Activity Test")
        controller.save_identity(identity)
        
        # Add multiple activities
        activities = [
            ("work", "Project A", 60),
            ("learning", "Study cryptography", 90),
            ("health", "Exercise", 45),
            ("family", "Dinner", 60)
        ]
        
        for activity_type, description, duration in activities:
            activity = controller.create_activity(
                activity_type=activity_type,
                data={"description": description},
                duration=duration,
                shareable=True
            )
            controller.add_to_pending(activity)
        
        # Sync
        output_file = temp_dir / "multi_activity.ph.json"
        ph_file = controller.sync_to_file(output_file=output_file)
        
        # Load and verify
        from ph.v001.models.file import PersonalHistoryFile
        
        loaded_file = PersonalHistoryFile.load(output_file)
        identity_file = temp_dir / "identity.json"
        
        assert loaded_file.verify_signature(identity_file_path=identity_file) is True
        
        # Check all activities are present
        day = loaded_file.timeline[0]
        assert len(day.activities) == len(activities)
        
        # Check activity types
        activity_types = [a.type for a in day.activities]
        expected_types = [a[0] for a in activities]
        assert set(activity_types) == set(expected_types)
        
        print("✓ Multiple activities test passed")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_custom_activity_types():
    """Test that custom activity types are allowed."""
    from ph.v001.controllers.history_controller import HistoryController
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        controller = HistoryController(temp_dir)
        
        # Create identity
        identity = controller.create_identity("Custom Types Test")
        controller.save_identity(identity)
        
        # Add activities with custom types
        custom_activities = [
            ("Creative Writing", "Wrote a short story", 120),
            ("Meditation", "Morning meditation session", 30),
            ("Gardening", "Planted new vegetables", 90),
            ("DIY Project", "Built a bookshelf", 180)
        ]
        
        for activity_type, description, duration in custom_activities:
            activity = controller.create_activity(
                activity_type=activity_type,
                data={"description": description},
                duration=duration,
                shareable=True
            )
            controller.add_to_pending(activity)
        
        # Sync
        output_file = temp_dir / "custom_types.ph.json"
        ph_file = controller.sync_to_file(output_file=output_file)
        
        # Load and verify
        from ph.v001.models.file import PersonalHistoryFile
        from ph.v001.schema import validate_ph_file
        
        loaded_file = PersonalHistoryFile.load(output_file)
        identity_file = temp_dir / "identity.json"
        
        # Should validate successfully
        with open(output_file, 'r') as f:
            file_data = json.load(f)
        
        assert validate_ph_file(file_data) is True, "Custom types should pass validation"
        assert loaded_file.verify_signature(identity_file_path=identity_file) is True
        
        print("✓ Custom activity types test passed")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_activity_with_description_field():
    """Test the new --description flag functionality."""
    from ph.v001.controllers.history_controller import HistoryController
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        controller = HistoryController(temp_dir)
        
        # Create identity
        identity = controller.create_identity("Description Test")
        controller.save_identity(identity)
        
        # Add activity with description in data field
        activity = controller.create_activity(
            activity_type="work",  # Standard type
            data={
                "project": "Test Project",
                "description": "This is a detailed description of the activity"
            },
            duration=75,
            shareable=True
        )
        
        controller.add_to_pending(activity)
        
        # Sync
        output_file = temp_dir / "description_test.ph.json"
        ph_file = controller.sync_to_file(output_file=output_file)
        
        # Load and check
        from ph.v001.models.file import PersonalHistoryFile
        
        loaded_file = PersonalHistoryFile.load(output_file)
        day = loaded_file.timeline[0]
        saved_activity = day.activities[0]
        
        # Should have description in data
        assert "description" in saved_activity.data
        assert saved_activity.data["description"] == "This is a detailed description of the activity"
        
        # Type should be "work" not the description
        assert saved_activity.type == "work"
        
        print("✓ Activity description field test passed")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_file_sharing_shareable_version():
    """Test getting shareable version (without private data)."""
    from ph.v001.controllers.history_controller import HistoryController
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        controller = HistoryController(temp_dir)
        
        # Create identity
        identity = controller.create_identity("Sharing Test")
        controller.save_identity(identity)
        
        # Add mix of shareable and non-shareable activities
        activities = [
            ("work", "Project X", 120, True),   # Shareable
            ("work", "Confidential Project", 90, False),  # Not shareable
            ("learning", "Public research", 60, True),    # Shareable
        ]
        
        for activity_type, description, duration, shareable in activities:
            activity = controller.create_activity(
                activity_type=activity_type,
                data={"description": description},
                duration=duration,
                shareable=shareable
            )
            controller.add_to_pending(activity)
        
        # Sync
        output_file = temp_dir / "sharing_test.ph.json"
        ph_file = controller.sync_to_file(output_file=output_file)
        
        # Get shareable version
        shareable_data = ph_file.get_shareable_version()
        
        # Check structure
        assert "version" in shareable_data
        assert "identity" in shareable_data
        assert "timeline" in shareable_data
        assert "signature" not in shareable_data  # No signature in shareable version
        
        # Check only shareable activities are included
        timeline = shareable_data["timeline"]
        assert len(timeline) == 1  # Still one day
        
        day = timeline[0]
        activities = day["activities"]
        
        # Should have 2 shareable activities (not 3)
        assert len(activities) == 2
        
        # Check descriptions
        descriptions = [a["data"]["description"] for a in activities]
        assert "Project X" in descriptions
        assert "Public research" in descriptions
        assert "Confidential Project" not in descriptions  # Not shareable
        
        print("✓ File sharing test passed")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# Note: Timer tests with real waiting would go here, but they would make tests very slow
# We'll create separate timer tests that can be run when needed

if __name__ == "__main__":
    # Run tests
    test_complete_workflow_with_real_crypto()
    test_multiple_activities_single_day()
    test_custom_activity_types()
    test_activity_with_description_field()
    test_file_sharing_shareable_version()
    
    print("\n✅ All workflow integration tests passed with real cryptography!")