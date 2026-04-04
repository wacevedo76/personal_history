"""
Day Model for Personal History v0.01
"""

import json
import hashlib
from typing import List, Dict
from datetime import datetime
from .activity import Activity


class Day:
    """Represents a Personal History day"""
    
    def __init__(self, date: str, activities: List[Activity]):
        self.date = date
        self.activities = activities
        # Calculate commitment (hash is now a property)
        activity_hashes = sorted([activity.hash for activity in self.activities])
        commitment_input = self.date + "".join(activity_hashes)
        self._commitment = hashlib.sha256(commitment_input.encode()).hexdigest()
    
    def _calculate_hash(self):
        """Calculate day hash from activities"""
        # Sort activities by hash for consistent ordering
        activity_hashes = sorted([activity.hash for activity in self.activities])
        
        # Create commitment input
        commitment_input = self.date + "".join(activity_hashes)
        self._commitment = hashlib.sha256(commitment_input.encode()).hexdigest()
        
        # Calculate day hash
        hash_input = self.date + self._commitment
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    @property
    def hash(self):
        """Day hash (recalculated on every access to ensure integrity)"""
        return self._calculate_hash()
    
    @property
    def commitment(self):
        """Day commitment"""
        return self._commitment
    
    def add_activity(self, activity: Activity):
        """Add activity to day"""
        self.activities.append(activity)
        self._calculate_hash()  # Recalculate hash
    
    def to_dict(self, include_private: bool = False) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "date": self.date,
            "timestamp": {
                "commitment": self.commitment
            },
            "activities": [
                activity.to_dict(include_private=include_private)
                for activity in self.activities
            ],
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Day':
        """Create Day from dictionary"""
        activities = [
            Activity.from_dict(activity_data)
            for activity_data in data.get("activities", [])
        ]
        
        day = cls(
            date=data["date"],
            activities=activities
        )
        
        # Override calculated values with stored ones
        day._commitment = data.get("timestamp", {}).get("commitment", "")
        
        return day
    
    def verify(self) -> bool:
        """Verify day integrity"""
        # Verify all activities
        for activity in self.activities:
            if not activity.verify():
                return False
        
        # Recalculate commitment
        activity_hashes = sorted([activity.hash for activity in self.activities])
        commitment_input = self.date + "".join(activity_hashes)
        calculated_commitment = hashlib.sha256(commitment_input.encode()).hexdigest()
        
        if calculated_commitment != self.commitment:
            return False
        
        # Recalculate day hash
        hash_input = self.date + self.commitment
        calculated_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        return calculated_hash == self.hash
    
    def get_total_duration(self) -> int:
        """Get total duration of all activities in minutes"""
        return sum(activity.duration for activity in self.activities)
    
    def get_shareable_activities(self) -> List[Activity]:
        """Get list of shareable activities"""
        return [activity for activity in self.activities if activity.shareable]
    
    def get_shareable_version(self) -> Dict:
        """Get shareable version (without private data)"""
        return {
            "date": self.date,
            "timestamp": {
                "commitment": self.commitment
            },
            "activities": [
                activity.get_shareable_version()
                for activity in self.activities
                if activity.shareable
            ],
            "hash": self.hash
        }