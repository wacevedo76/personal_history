"""
Time Tracking Controller for Personal History v0.01
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from ..models.activity import Activity


class TimeTrackingController:
    """Controller for time tracking operations"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path.home() / ".personal_history"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def start_timer(self, activity_name: str, activity_type: Optional[str] = None, data: Optional[Dict] = None):
        """Start timing an activity"""
        timers_file = self.data_dir / "timers.json"
        
        if timers_file.exists():
            with open(timers_file, 'r') as f:
                timers = json.load(f)
        else:
            timers = {"active_timers": {}}
        
        # Check if activity already being timed
        if activity_name in timers["active_timers"]:
            raise ValueError(f"Activity '{activity_name}' is already being timed")
        
        # Start timer
        timers["active_timers"][activity_name] = {
            "start_time": datetime.now().isoformat(),
            "type": activity_type or activity_name,
            "data": data or {}
        }
        
        # Save timers
        with open(timers_file, 'w') as f:
            json.dump(timers, f, indent=2)
    
    def stop_timer(self, activity_name: str) -> Dict:
        """Stop timing an activity and return elapsed time"""
        timers_file = self.data_dir / "timers.json"
        
        if not timers_file.exists():
            raise ValueError("No active timers found")
        
        with open(timers_file, 'r') as f:
            timers = json.load(f)
        
        # Check if activity is being timed
        if activity_name not in timers["active_timers"]:
            raise ValueError(f"Activity '{activity_name}' is not being timed")
        
        # Calculate duration
        timer_data = timers["active_timers"][activity_name]
        start_time = datetime.fromisoformat(timer_data["start_time"])
        end_time = datetime.now()
        duration_seconds = (end_time - start_time).total_seconds()
        duration_minutes = int(duration_seconds / 60)
        
        # Remove from active timers
        del timers["active_timers"][activity_name]
        
        # Save updated timers
        with open(timers_file, 'w') as f:
            json.dump(timers, f, indent=2)
        
        return {
            "activity_name": activity_name,
            "activity_type": timer_data["type"],
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": duration_seconds,
            "duration_minutes": duration_minutes,
            "data": timer_data["data"]
        }
    
    def get_active_timers(self) -> Dict:
        """Get all active timers"""
        timers_file = self.data_dir / "timers.json"
        
        if not timers_file.exists():
            return {"active_timers": {}}
        
        with open(timers_file, 'r') as f:
            return json.load(f)
    
    def create_activity_from_timer(self, timer_result: Dict, shareable: bool = True) -> Activity:
        """Create Activity from timer result"""
        return Activity(
            activity_type=timer_result["activity_type"],
            data=timer_result["data"],
            duration=timer_result["duration_minutes"],
            exact_start=timer_result["start_time"].isoformat() + "Z",
            exact_end=timer_result["end_time"].isoformat() + "Z",
            shareable=shareable
        )
    
    def get_timer_summary(self) -> Dict:
        """Get summary of active timers"""
        timers = self.get_active_timers()
        
        summary = {
            "active_timers": len(timers["active_timers"]),
            "timers": []
        }
        
        for activity_name, timer_data in timers["active_timers"].items():
            start_time = datetime.fromisoformat(timer_data["start_time"])
            elapsed = datetime.now() - start_time
            elapsed_minutes = int(elapsed.total_seconds() / 60)
            
            summary["timers"].append({
                "activity_name": activity_name,
                "activity_type": timer_data["type"],
                "start_time": start_time,
                "elapsed_minutes": elapsed_minutes,
                "elapsed_hours": elapsed.total_seconds() / 3600,
                "data": timer_data["data"]
            })
        
        return summary