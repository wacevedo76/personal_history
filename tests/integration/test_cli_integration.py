#!/usr/bin/env python3
"""
Integration tests for CLI functionality.
"""

import pytest
import sys
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ph.v001.cli import (
    parse_duration,
    init_command,
    add_command,
    start_command,
    stop_command,
    tasks_command,
    pending_command,
    sync_command,
    verify_command,
    analyze_command
)
from ph.v001.core import PersonalHistoryV001
from ph.v001.schema import validate_ph_file


class TestCLIIntegration:
    """Integration tests for CLI commands."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.home_dir = Path(self.test_dir)
        
        # Mock Path.home to return test directory
        self.original_home = Path.home
        Path.home = lambda: self.home_dir
        
        # Create .personal_history directory
        self.personal_history_dir = self.home_dir / ".personal_history"
        self.personal_history_dir.mkdir(exist_ok=True)
    
    def teardown_method(self):
        """Clean up test environment."""
        # Restore original Path.home
        Path.home = self.original_home
        
        # Clean up test directory
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init_command(self):
        """Test init command creates identity file."""
        # Mock args
        class Args:
            name = "Test User"
        
        args = Args()
        
        # Run init command
        with patch('builtins.print') as mock_print:
            init_command(args)
        
        # Check identity file was created
        identity_file = self.personal_history_dir / "identity.json"
        assert identity_file.exists()
        
        # Check identity file content
        with open(identity_file, 'r') as f:
            identity = json.load(f)
        
        assert "identity_hash" in identity
        assert "name" in identity
        assert identity["name"] == "Test User"
        assert "created_at" in identity
    
    def test_add_command_without_init(self):
        """Test add command fails without identity."""
        # Mock args
        class Args:
            type = "work"
            duration = "1h"
            date = "2024-01-01"
            project = "test"
            meal = None
            distance = None
            with_people = None
            private = False
        
        args = Args()
        
        # Run add command (should fail)
        with patch('builtins.print') as mock_print:
            add_command(args)
        
        # Check error message was printed
        mock_print.assert_called_with("Error: No identity found. Run 'ph init' first.")
    
    def test_add_command_with_identity(self):
        """Test add command with existing identity."""
        # First create identity
        identity = PersonalHistoryV001.create_identity("Test User")
        identity_file = self.personal_history_dir / "identity.json"
        with open(identity_file, 'w') as f:
            json.dump(identity, f, indent=2)
        
        # Mock args
        class Args:
            type = "work"
            duration = "1h30"
            date = "2024-01-01"
            project = "test project"
            meal = None
            distance = None
            with_people = None
            private = False
        
        args = Args()
        
        # Run add command
        with patch('builtins.print') as mock_print:
            add_command(args)
        
        # Check pending file was created
        pending_file = self.personal_history_dir / "pending.json"
        assert pending_file.exists()
        
        # Check pending file content
        with open(pending_file, 'r') as f:
            pending = json.load(f)
        
        assert "activities" in pending
        assert len(pending["activities"]) == 1
        assert pending["activities"][0]["date"] == "2024-01-01"
        assert len(pending["activities"][0]["activities"]) == 1
        activity = pending["activities"][0]["activities"][0]
        assert activity["type"] == "work"
        assert activity["duration"] == 90  # 1h30 = 90 minutes
        assert activity["data"]["project"] == "test project"
    
    def test_start_command(self):
        """Test start command creates timer."""
        # Mock args
        class Args:
            activity = "coding"
            type = "work"
            project = "Personal History"
            meal = None
        
        args = Args()
        
        # Run start command
        with patch('builtins.print') as mock_print:
            start_command(args)
        
        # Check timers file was created
        timers_file = self.personal_history_dir / "timers.json"
        assert timers_file.exists()
        
        # Check timers file content
        with open(timers_file, 'r') as f:
            timers = json.load(f)
        
        assert "active_timers" in timers
        assert "coding" in timers["active_timers"]
        timer_data = timers["active_timers"]["coding"]
        assert timer_data["type"] == "work"
        assert timer_data["data"]["project"] == "Personal History"
        assert "start_time" in timer_data
    
    def test_stop_command_without_timer(self):
        """Test stop command without active timer."""
        # Mock args
        class Args:
            activity = "coding"
            auto_add = False
        
        args = Args()
        
        # Run stop command
        with patch('builtins.print') as mock_print:
            stop_command(args)
        
        # Check error message was printed
        mock_print.assert_called_with("No active timers found.")
    
    def test_tasks_command_no_data(self):
        """Test tasks command with no data."""
        # Mock args
        class Args:
            pass
        
        args = Args()
        
        # Run tasks command
        with patch('builtins.print') as mock_print:
            tasks_command(args)
        
        # Check appropriate messages were printed
        calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("No active timers" in str(call) for call in calls)
        assert any("No pending activities" in str(call) for call in calls)
    
    def test_pending_command_no_data(self):
        """Test pending command with no data."""
        # Mock args
        class Args:
            pass
        
        args = Args()
        
        # Run pending command
        with patch('builtins.print') as mock_print:
            pending_command(args)
        
        # Check message was printed
        mock_print.assert_called_with("No pending activities.")
    
    def test_verify_command_valid_file(self):
        """Test verify command with valid file."""
        # Create a valid Personal History file
        identity = PersonalHistoryV001.create_identity("Test User")
        activity = PersonalHistoryV001.create_activity("work", {"project": "test"}, 60)
        day = PersonalHistoryV001.create_day("2024-01-01", [activity])
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        ph_file["signature"] = "a" * 128
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ph.json', delete=False) as f:
            temp_file = Path(f.name)
            json.dump(ph_file, f, indent=2)
        
        try:
            # Mock args
            class Args:
                file = temp_file
            
            args = Args()
            
            # Run verify command
            with patch('builtins.print') as mock_print:
                verify_command(args)
            
            # Check success message was printed
            mock_print.assert_called_with(f"✓ {temp_file} is a valid Personal History v0.01 file")
        
        finally:
            # Clean up
            temp_file.unlink()
    
    def test_analyze_command(self):
        """Test analyze command."""
        # Create a Personal History file
        identity = PersonalHistoryV001.create_identity("Test User")
        activity1 = PersonalHistoryV001.create_activity("work", {"project": "test"}, 120)
        activity2 = PersonalHistoryV001.create_activity("exercise", {}, 45)
        day = PersonalHistoryV001.create_day("2024-01-01", [activity1, activity2])
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ph.json', delete=False) as f:
            temp_file = Path(f.name)
            json.dump(ph_file, f, indent=2)
        
        try:
            # Mock args
            class Args:
                file = temp_file
                export_shareable = False
            
            args = Args()
            
            # Run analyze command
            with patch('builtins.print') as mock_print:
                analyze_command(args)
            
            # Check analysis was printed
            calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Total days: 1" in str(call) for call in calls)
            assert any("Total activities: 2" in str(call) for call in calls)
            assert any("Total time: 165 minutes" in str(call) for call in calls)
        
        finally:
            # Clean up
            temp_file.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])