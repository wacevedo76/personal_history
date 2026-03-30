"""
pytest fixtures for Personal History tests.
"""

import pytest
import json
from pathlib import Path


@pytest.fixture
def minimal_valid_ph():
    """Minimal valid PH file data."""
    return {
        "version": "0.01.0",
        "identity": {
            "hash": "a" * 64,
            "name": "Test User"
        },
        "timeline": [],
        "signature": "b" * 128
    }


@pytest.fixture
def example_william_ph():
    """Example PH file based on existing example."""
    return {
        "version": "0.01.0",
        "identity": {
            "hash": "8f1d5c8a3b7e9f2a4d6c0b1e5f9a3d7c2b8e1f4a9d6c3b7e0f1a5d8c2b9e4f60",
            "name": "William Acevedo"
        },
        "timeline": [
            {
                "date": "2024-01-01",
                "timestamp": {
                    "commitment": "a1b2c3d4e5f67890123456789012345678901234567890123456789012345600"
                },
                "activities": [
                    {
                        "type": "family",
                        "data": {
                            "activity": "new_years_breakfast",
                            "participants": ["wife", "son"],
                            "meal": "pancakes"
                        },
                        "duration": 45,
                        "shareable": True,
                        "hash": "f1e2d3c4b5a697887766554433221100ffeeddccbbaa99887766554433221100"
                    },
                    {
                        "type": "planning",
                        "data": {
                            "topic": "personal_history_project"
                        },
                        "duration": 60,
                        "shareable": True,
                        "hash": "a0b1c2d3e4f56789012345678901234567890123456789012345678901234500"
                    }
                ],
                "hash": "d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3",
                "note": "Good start to the year - family time followed by project planning"
            }
        ],
        "signature": "a" * 128
    }


@pytest.fixture
def valid_ph_with_chain():
    """PH file with a hash chain for testing forward security."""
    return {
        "version": "0.01.0",
        "identity": {"hash": "a" * 64},
        "timeline": [
            {
                "date": "2024-01-01",
                "hash": "hash_day_1_64_chars_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "activities": [
                    {
                        "type": "work",
                        "data": {"project": "test"},
                        "duration": 120,
                        "shareable": True,
                        "hash": "activity_hash_1_64_chars_bbbbbbbbbbbbbbbbbbbbbbbbbbbb"
                    }
                ]
            },
            {
                "date": "2024-01-02",
                "hash": "hash_day_2_64_chars_cccccccccccccccccccccccccccccccccccccccc",
                "activities": [
                    {
                        "type": "learning",
                        "data": {"topic": "testing"},
                        "duration": 90,
                        "shareable": True,
                        "hash": "activity_hash_2_64_chars_dddddddddddddddddddddddddddd"
                    }
                ]
            }
        ],
        "signature": "signature_128_chars_" + "e" * 108
    }


@pytest.fixture
def valid_ph_file_path(tmp_path):
    """Path to a valid PH file on disk."""
    file_path = tmp_path / "valid.ph.json"
    file_path.write_text(json.dumps({
        "version": "0.01.0",
        "identity": {"hash": "a" * 64},
        "timeline": [],
        "signature": "b" * 128
    }))
    return file_path


# Create fixture files on disk
@pytest.fixture(scope="session")
def fixture_dir():
    """Directory containing fixture files."""
    fixture_path = Path(__file__).parent / "fixtures"
    fixture_path.mkdir(exist_ok=True)
    return fixture_path


@pytest.fixture
def valid_fixture_file(fixture_dir):
    """Create a valid fixture file on disk."""
    file_path = fixture_dir / "valid" / "minimal.ph.json"
    file_path.parent.mkdir(exist_ok=True)
    
    data = {
        "version": "0.01.0",
        "identity": {"hash": "f" * 64},
        "timeline": [],
        "signature": "g" * 128
    }
    
    file_path.write_text(json.dumps(data, indent=2))
    return file_path