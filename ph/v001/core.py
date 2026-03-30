"""
Personal History Format v0.01 - Core Implementation (Legacy API)
This module provides backward compatibility with the original API.
New code should use the MVC architecture directly.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

# Import from new MVC structure
from .models.identity import Identity as IdentityModel
from .models.activity import Activity as ActivityModel
from .models.day import Day as DayModel
from .models.file import PersonalHistoryFile as PersonalHistoryFileModel
from .controllers.history_controller import HistoryController


class PersonalHistoryV001:
    """Core implementation of Personal History Format v0.01 (Legacy API)"""
    
    VERSION = "0.01.0"
    
    # Static methods that delegate to new MVC structure
    
    @staticmethod
    def hash_data(data: str) -> str:
        """SHA-256 hash helper"""
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def hash_bytes(data: bytes) -> str:
        """SHA-256 hash for bytes"""
        import hashlib
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def create_timestamp_commitment(exact_start: str, exact_end: str) -> Dict:
        """
        Create a timestamp commitment hiding exact times
        
        Args:
            exact_start: ISO 8601 timestamp with milliseconds
            exact_end: ISO 8601 timestamp with milliseconds
            
        Returns:
            Dictionary with commitment and private data
        """
        # This is now handled by the Activity model
        # For backward compatibility, we simulate it
        import secrets
        nonce = secrets.token_hex(32)
        commitment_input = exact_start + exact_end + nonce
        commitment = PersonalHistoryV001.hash_data(commitment_input)
        
        return {
            "commitment": commitment,
            "_private": {
                "nonce": nonce,
                "exact_start": exact_start,
                "exact_end": exact_end
            }
        }
    
    @staticmethod
    def create_activity(
        activity_type: str,
        data: Dict,
        duration: int,
        exact_start: Optional[str] = None,
        exact_end: Optional[str] = None,
        shareable: bool = True
    ) -> Dict:
        """
        Create an activity with hidden exact times
        
        Args:
            activity_type: Type of activity (work, family, exercise, etc.)
            data: Activity-specific data
            duration: Duration in minutes
            exact_start: Optional exact start time (ISO 8601)
            exact_end: Optional exact end time (ISO 8601)
            shareable: Whether activity can be shared publicly
            
        Returns:
            Activity dictionary with hidden exact times
        """
        # Create using new Activity model
        activity = ActivityModel(
            activity_type=activity_type,
            data=data,
            duration=duration,
            exact_start=exact_start,
            exact_end=exact_end,
            shareable=shareable
        )
        
        # Convert to legacy format
        return activity.to_dict(include_private=True)
    
    @staticmethod
    def create_day(date: str, activities: List[Dict]) -> Dict:
        """
        Create a day entry
        
        Args:
            date: Date in YYYY-MM-DD format
            activities: List of activity dictionaries
            
        Returns:
            Day dictionary
        """
        # Convert activity dicts to Activity models
        activity_models = [
            ActivityModel.from_dict(activity_data)
            for activity_data in activities
        ]
        
        # Create using new Day model
        day = DayModel(date=date, activities=activity_models)
        
        # Convert to legacy format
        return day.to_dict(include_private=False)
    
    @staticmethod
    def create_identity(name: Optional[str] = None) -> Dict:
        """
        Create a new identity
        
        Args:
            name: Optional name for the identity
            
        Returns:
            Identity dictionary
        """
        # Create using new Identity model
        identity = IdentityModel(name=name)
        identity.generate()
        
        # Convert to legacy format
        return identity.to_dict()
    
    @staticmethod
    def create_file(identity: Dict, timeline: List[Dict]) -> Dict:
        """
        Create a Personal History file
        
        Args:
            identity: Identity dictionary
            timeline: List of day dictionaries
            
        Returns:
            Personal History file dictionary
        """
        # Convert identity dict to Identity model
        identity_model = IdentityModel.from_dict(identity)
        
        # Convert day dicts to Day models
        day_models = [
            DayModel.from_dict(day_data)
            for day_data in timeline
        ]
        
        # Create using new PersonalHistoryFile model
        ph_file = PersonalHistoryFileModel(
            identity=identity_model,
            timeline=day_models
        )
        
        # Convert to legacy format
        return ph_file.to_dict(include_private=False)
    
    @staticmethod
    def save_file(data: Dict, filepath: Path):
        """
        Save Personal History file to disk
        
        Args:
            data: Personal History file dictionary
            filepath: Path to save the file
        """
        # Load from dict
        ph_file = PersonalHistoryFileModel.from_dict(data)
        
        # Save using new model
        ph_file.save(filepath, include_private=False)
    
    @staticmethod
    def load_file(filepath: Path) -> Dict:
        """
        Load Personal History file from disk
        
        Args:
            filepath: Path to the file
            
        Returns:
            Personal History file dictionary
        """
        # Load using new model
        ph_file = PersonalHistoryFileModel.load(filepath)
        
        # Convert to legacy format
        return ph_file.to_dict(include_private=False)


# Try to import cryptography libraries for backward compatibility
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Warning: cryptography library not available. Install with: pip install cryptography")
    print("Using simulated cryptography for demonstration.")