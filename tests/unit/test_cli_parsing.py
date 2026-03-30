#!/usr/bin/env python3
"""
Unit tests for CLI parsing functionality.
"""

import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ph.v001.cli import parse_duration


class TestDurationParsing:
    """Test duration parsing functionality."""
    
    def test_parse_duration_minutes(self):
        """Test parsing minutes."""
        assert parse_duration("90") == 90
        assert parse_duration("45") == 45
        assert parse_duration("0") == 0
    
    def test_parse_duration_hours(self):
        """Test parsing hours."""
        assert parse_duration("2h") == 120
        assert parse_duration("1.5h") == 90
        assert parse_duration("0.5h") == 30
    
    def test_parse_duration_hours_minutes(self):
        """Test parsing hours and minutes."""
        assert parse_duration("1h30") == 90
        assert parse_duration("1hr30") == 90
        assert parse_duration("2h45") == 165
    
    def test_parse_duration_minutes_only(self):
        """Test parsing minutes format."""
        assert parse_duration("45m") == 45
        assert parse_duration("90m") == 90
    
    def test_parse_duration_colon_format(self):
        """Test parsing colon format."""
        assert parse_duration("1:30") == 90
        assert parse_duration("2:45") == 165
    
    def test_parse_duration_empty(self):
        """Test parsing empty duration."""
        assert parse_duration("") == 0
        assert parse_duration(None) == 0
    
    def test_parse_duration_invalid(self):
        """Test parsing invalid duration raises error."""
        with pytest.raises(ValueError, match="Could not parse duration"):
            parse_duration("invalid")
        
        with pytest.raises(ValueError, match="Could not parse duration"):
            parse_duration("abc123")
    
    def test_parse_duration_case_insensitive(self):
        """Test parsing is case insensitive."""
        assert parse_duration("1H30") == 90
        assert parse_duration("1HR30") == 90
        assert parse_duration("45M") == 45
    
    def test_parse_duration_with_spaces(self):
        """Test parsing with spaces."""
        assert parse_duration("1 h 30") == 90
        assert parse_duration("2 h") == 120


class TestCLIImports:
    """Test CLI module imports."""
    
    def test_cli_imports(self):
        """Test that CLI module imports correctly."""
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
            analyze_command,
            demo_command,
            main
        )
        
        # Just check they exist
        assert parse_duration is not None
        assert init_command is not None
        assert add_command is not None
        assert start_command is not None
        assert stop_command is not None
        assert tasks_command is not None
        assert pending_command is not None
        assert sync_command is not None
        assert verify_command is not None
        assert analyze_command is not None
        assert demo_command is not None
        assert main is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])