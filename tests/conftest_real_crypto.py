"""
pytest fixtures for Personal History tests with REAL cryptography (no mocks).
"""

import pytest
import json
import tempfile
import shutil
import time
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ph.v001.controllers.history_controller import HistoryController
from ph.v001.models.identity import Identity


@pytest.fixture(scope="function")
def temp_data_dir():
    """Create a temporary directory for test data, cleaned up after test."""
    temp_dir = Path(tempfile.mkdtemp(prefix="ph_test_"))
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def history_controller(temp_data_dir):
    """Create a HistoryController with temporary data directory."""
    return HistoryController(temp_data_dir)


@pytest.fixture(scope="function")
def fresh_identity(history_controller):
    """Create a fresh identity with real cryptography for testing."""
    identity = history_controller.create_identity("Test User")
    history_controller.save_identity(identity)
    return identity


@pytest.fixture(scope="function")
def valid_activity():
    """Create a valid activity with real data."""
    from ph.v001.models.activity import Activity
    import datetime
    
    return Activity(
        activity_type="work",
        data={"project": "Test Project", "description": "Test activity"},
        duration=30,  # 30 minutes
        shareable=True
    )


@pytest.fixture(scope="function")
def signed_ph_file(history_controller, fresh_identity, valid_activity):
    """Create a signed PH file with real cryptography."""
    # Add activity to pending
    history_controller.add_to_pending(valid_activity)
    
    # Create output file in temp directory
    temp_dir = history_controller.data_dir.parent
    output_file = temp_dir / "test_signed.ph.json"
    
    # Sync to file (creates and signs)
    ph_file = history_controller.sync_to_file(output_file=output_file)
    
    return {
        "file": ph_file,
        "path": output_file,
        "controller": history_controller,
        "identity": fresh_identity
    }


@pytest.fixture(scope="function")
def timer_test_context(history_controller, fresh_identity):
    """Create context for timer tests with real waiting."""
    return {
        "controller": history_controller,
        "identity": fresh_identity,
        "start_time": None,
        "activity_name": "Test Timer Activity"
    }


class RealTimer:
    """Helper for real timer tests with actual waiting."""
    
    def __init__(self, controller, activity_name="Test Activity", activity_type="work"):
        self.controller = controller
        self.activity_name = activity_name
        self.activity_type = activity_type
        self.start_time = None
        
    def start(self, project=None, description=None):
        """Start a timer with real waiting."""
        data = {}
        if project:
            data["project"] = project
        if description:
            data["description"] = description
            
        # In real usage, this would start a background timer
        # For testing, we'll record start time
        self.start_time = time.time()
        
        # Create a pending activity that represents the timer
        from ph.v001.models.activity import Activity
        activity = Activity(
            activity_type=self.activity_type,
            data=data,
            duration=0,  # Will be calculated when stopped
            shareable=True
        )
        
        # Store in controller's pending (simulating timer start)
        self.controller.add_to_pending(activity)
        return activity
    
    def stop(self, wait_seconds=65):
        """Stop timer after waiting (minimum 65 seconds for valid activity)."""
        if not self.start_time:
            raise ValueError("Timer not started")
        
        # Wait if needed to ensure valid duration
        elapsed = time.time() - self.start_time
        if elapsed < wait_seconds:
            time.sleep(wait_seconds - elapsed)
        
        # Calculate actual duration in minutes
        actual_elapsed = time.time() - self.start_time
        duration_minutes = int(actual_elapsed / 60)
        
        if duration_minutes < 1:
            duration_minutes = 1  # Minimum 1 minute
        
        # Update the pending activity with actual duration
        pending = self.controller.get_pending_activities()
        if pending.get("activities"):
            # Update duration of the first pending activity
            pending["activities"][0]["activities"][0]["duration"] = duration_minutes
            
            # Save updated pending
            pending_file = self.controller.data_dir / "pending.json"
            with open(pending_file, 'w') as f:
                json.dump(pending, f)
        
        return duration_minutes


@pytest.fixture(scope="function")
def real_timer(history_controller):
    """Create a real timer helper for tests."""
    return RealTimer(history_controller)


# Test data validation
@pytest.fixture
def invalid_short_activity():
    """Activity with duration 0 (invalid)."""
    from ph.v001.models.activity import Activity
    
    return Activity(
        activity_type="work",
        data={"project": "Test"},
        duration=0,  # Invalid - must be > 0
        shareable=True
    )


@pytest.fixture
def activity_with_custom_type():
    """Activity with custom type (should be allowed)."""
    from ph.v001.models.activity import Activity
    
    return Activity(
        activity_type="Custom Activity Type",
        data={"description": "Testing custom types"},
        duration=30,
        shareable=True
    )


# File validation helpers
def assert_file_is_valid(file_path, identity_file_path=None):
    """Assert that a PH file is valid with real cryptography."""
    from ph.v001.models.file import PersonalHistoryFile
    from ph.v001.schema import validate_ph_file
    
    # Load file
    ph_file = PersonalHistoryFile.load(file_path)
    
    # Validate schema
    with open(file_path, 'r') as f:
        file_data = json.load(f)
    
    assert validate_ph_file(file_data) is True, "File failed schema validation"
    
    # Verify signature if present
    if ph_file.signature:
        if identity_file_path is None:
            # Try default location
            identity_file_path = file_path.parent / "identity.json"
        
        assert ph_file.verify_signature(identity_file_path) is True, "Signature verification failed"
    
    return ph_file


def create_test_workflow(controller, activities, output_file=None):
    """Helper to create a complete test workflow."""
    if output_file is None:
        output_file = controller.data_dir.parent / "workflow_test.ph.json"
    
    # Add all activities to pending
    for activity in activities:
        controller.add_to_pending(activity)
    
    # Sync to file
    ph_file = controller.sync_to_file(output_file=output_file)
    
    return {
        "file": ph_file,
        "path": output_file,
        "activities": activities
    }