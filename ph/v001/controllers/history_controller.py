"""
History Controller for Personal History v0.01
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from ..models.identity import Identity
from ..models.activity import Activity
from ..models.day import Day
from ..models.file import PersonalHistoryFile


class HistoryController:
    """Controller for Personal History operations"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path.home() / ".personal_history"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def create_identity(self, name: Optional[str] = None) -> Identity:
        """Create a new identity"""
        identity = Identity(name=name)
        identity.generate()
        return identity
    
    def save_identity(self, identity: Identity):
        """Save identity to file"""
        identity_file = self.data_dir / "identity.json"
        with open(identity_file, 'w') as f:
            json.dump(identity.to_dict(), f, indent=2)
    
    def load_identity(self) -> Optional[Identity]:
        """Load identity from file"""
        identity_file = self.data_dir / "identity.json"
        if not identity_file.exists():
            return None
        
        with open(identity_file, 'r') as f:
            data = json.load(f)
        
        return Identity.from_dict(data)
    
    def create_activity(
        self,
        activity_type: str,
        data: Dict,
        duration: int,
        shareable: bool = True
    ) -> Activity:
        """Create a new activity"""
        return Activity(
            activity_type=activity_type,
            data=data,
            duration=duration,
            shareable=shareable
        )
    
    def create_day(self, date: str, activities: List[Activity]) -> Day:
        """Create a new day"""
        return Day(date=date, activities=activities)
    
    def create_file(self, identity: Identity, timeline: List[Day]) -> PersonalHistoryFile:
        """Create a Personal History file"""
        return PersonalHistoryFile(identity=identity, timeline=timeline)
    
    def save_file(self, ph_file: PersonalHistoryFile, filepath: Path, include_private: bool = False):
        """Save Personal History file"""
        ph_file.save(filepath, include_private=include_private)
    
    def load_file(self, filepath: Path) -> PersonalHistoryFile:
        """Load Personal History file"""
        return PersonalHistoryFile.load(filepath)
    
    def add_to_pending(self, activity: Activity, date: Optional[str] = None):
        """Add activity to pending list"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        pending_file = self.data_dir / "pending.json"
        
        if pending_file.exists():
            with open(pending_file, 'r') as f:
                pending = json.load(f)
        else:
            pending = {"activities": []}
        
        # Find or create day entry
        day_entry = None
        for day in pending["activities"]:
            if day["date"] == date:
                day_entry = day
                break
        
        if day_entry is None:
            day_entry = {"date": date, "activities": []}
            pending["activities"].append(day_entry)
        
        # Add activity (without private data)
        activity_dict = activity.to_dict(include_private=False)
        day_entry["activities"].append(activity_dict)
        
        # Save pending activities
        with open(pending_file, 'w') as f:
            json.dump(pending, f, indent=2)
    
    def get_pending_activities(self) -> Dict:
        """Get pending activities"""
        pending_file = self.data_dir / "pending.json"
        
        if not pending_file.exists():
            return {"activities": []}
        
        with open(pending_file, 'r') as f:
            return json.load(f)
    
    def clear_pending_activities(self):
        """Clear pending activities"""
        pending_file = self.data_dir / "pending.json"
        with open(pending_file, 'w') as f:
            json.dump({"activities": []}, f)
    
    def sync_to_file(self, output_file: Optional[Path] = None) -> PersonalHistoryFile:
        """
        Sync pending activities to Personal History file
        
        Args:
            output_file: Output file path (default: ~/personal_history.ph.json)
            
        Returns:
            Created Personal History file
        """
        # Load identity
        identity = self.load_identity()
        if not identity:
            raise ValueError("No identity found. Run 'ph init' first.")
        
        # Load pending activities
        pending = self.get_pending_activities()
        
        # Convert pending activities to Day objects
        timeline = []
        for pending_day in pending.get("activities", []):
            activities = [
                Activity.from_dict(activity_data)
                for activity_data in pending_day.get("activities", [])
            ]
            
            day = Day(
                date=pending_day["date"],
                activities=activities
            )
            timeline.append(day)
        
        # Create Personal History file
        ph_file = PersonalHistoryFile(identity=identity, timeline=timeline)
        
        # Sign the file
        ph_file.sign()
        
        # Save to file
        if output_file is None:
            output_file = Path.home() / "personal_history.ph.json"
        
        ph_file.save(output_file, include_private=False)
        
        # Clear pending activities
        self.clear_pending_activities()
        
        return ph_file
    
    def analyze_file(self, filepath: Path) -> Dict:
        """Analyze Personal History file"""
        ph_file = self.load_file(filepath)
        
        return {
            "file": str(filepath),
            "version": ph_file.VERSION,
            "total_days": len(ph_file.timeline),
            "total_activities": ph_file.get_activity_count(),
            "total_duration_minutes": ph_file.get_total_duration(),
            "total_duration_hours": ph_file.get_total_duration() / 60,
            "signature_valid": ph_file.verify_signature() if ph_file.signature else False,
            "file_valid": ph_file.verify()
        }