#!/usr/bin/env python3
"""
Timestamp utilities for Personal History v0.01
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


def extract_timestamps(ph_file_path: Path) -> Dict[str, Any]:
    """
    Extract all timestamps from a Personal History file.
    
    Args:
        ph_file_path: Path to .ph.json file
        
    Returns:
        Dictionary with timestamp information
    """
    with open(ph_file_path, 'r') as f:
        data = json.load(f)
    
    result = {
        "file": str(ph_file_path),
        "version": data.get("version"),
        "total_days": len(data.get("timeline", [])),
        "days": []
    }
    
    for day in data.get("timeline", []):
        day_info = {
            "date": day.get("date"),
            "commitment_hash": day.get("timestamp", {}).get("commitment"),
            "activities": []
        }
        
        for activity in day.get("activities", []):
            activity_info = {
                "type": activity.get("type"),
                "duration": activity.get("duration", 0),
                "shareable": activity.get("shareable", True),
                "commitment_hash": activity.get("timestamp", {}).get("commitment"),
                "exact_timestamps": {}
            }
            
            # Extract exact timestamps from _private field
            if "_private" in activity:
                private_data = activity["_private"]
                if "exact_start" in private_data:
                    activity_info["exact_timestamps"]["start"] = private_data["exact_start"]
                if "exact_end" in private_data:
                    activity_info["exact_timestamps"]["end"] = private_data["exact_end"]
            
            day_info["activities"].append(activity_info)
        
        result["days"].append(day_info)
    
    return result


def get_activity_timeline(ph_file_path: Path) -> List[Dict[str, Any]]:
    """
    Get chronological timeline of all activities with timestamps.
    
    Args:
        ph_file_path: Path to .ph.json file
        
    Returns:
        List of activities sorted by date/time
    """
    timestamps = extract_timestamps(ph_file_path)
    
    timeline = []
    
    for day in timestamps["days"]:
        date_str = day["date"]
        
        for activity in day["activities"]:
            timeline_entry = {
                "date": date_str,
                "type": activity["type"],
                "duration": activity["duration"],
                "shareable": activity["shareable"]
            }
            
            # Add timestamps if available
            if activity["exact_timestamps"]:
                timeline_entry.update(activity["exact_timestamps"])
            
            timeline.append(timeline_entry)
    
    # Sort by date, then by start time if available
    def sort_key(entry):
        date_key = entry["date"]
        
        # If we have exact start time, use it for sorting within the day
        if "start" in entry:
            try:
                # Parse ISO timestamp
                dt = datetime.fromisoformat(entry["start"].replace('Z', '+00:00'))
                return (date_key, dt)
            except:
                return (date_key, "00:00:00")
        
        return (date_key, "00:00:00")
    
    timeline.sort(key=sort_key)
    return timeline


def analyze_time_patterns(ph_file_path: Path) -> Dict[str, Any]:
    """
    Analyze time patterns from timestamps.
    
    Args:
        ph_file_path: Path to .ph.json file
        
    Returns:
        Dictionary with time pattern analysis
    """
    timeline = get_activity_timeline(ph_file_path)
    
    if not timeline:
        return {"error": "No activities found"}
    
    analysis = {
        "total_activities": len(timeline),
        "activities_with_exact_timestamps": 0,
        "time_ranges": [],
        "daily_patterns": {},
        "activity_type_times": {}
    }
    
    for entry in timeline:
        # Count activities with exact timestamps
        if "start" in entry or "end" in entry:
            analysis["activities_with_exact_timestamps"] += 1
        
        # Collect time ranges
        if "start" in entry and "end" in entry:
            try:
                start_dt = datetime.fromisoformat(entry["start"].replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(entry["end"].replace('Z', '+00:00'))
                
                time_range = {
                    "date": entry["date"],
                    "type": entry["type"],
                    "start": start_dt.strftime("%H:%M:%S"),
                    "end": end_dt.strftime("%H:%M:%S"),
                    "duration_minutes": entry["duration"]
                }
                analysis["time_ranges"].append(time_range)
                
                # Track daily patterns
                day = entry["date"]
                if day not in analysis["daily_patterns"]:
                    analysis["daily_patterns"][day] = []
                analysis["daily_patterns"][day].append({
                    "type": entry["type"],
                    "start": start_dt.strftime("%H:%M:%S"),
                    "end": end_dt.strftime("%H:%M:%S")
                })
                
                # Track activity type times
                activity_type = entry["type"]
                if activity_type not in analysis["activity_type_times"]:
                    analysis["activity_type_times"][activity_type] = {
                        "total_minutes": 0,
                        "count": 0
                    }
                analysis["activity_type_times"][activity_type]["total_minutes"] += entry["duration"]
                analysis["activity_type_times"][activity_type]["count"] += 1
                
            except Exception as e:
                # Skip entries with invalid timestamps
                continue
    
    return analysis


def export_timestamps_csv(ph_file_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Export timestamps to CSV file.
    
    Args:
        ph_file_path: Path to .ph.json file
        output_path: Optional output path (default: same as input with .csv extension)
        
    Returns:
        Path to created CSV file
    """
    if output_path is None:
        output_path = ph_file_path.with_suffix('.timestamps.csv')
    
    timeline = get_activity_timeline(ph_file_path)
    
    with open(output_path, 'w') as f:
        # Write header
        f.write("date,type,duration_minutes,shareable,start_time,end_time,commitment_hash\n")
        
        for entry in timeline:
            date = entry["date"]
            activity_type = entry["type"]
            duration = entry["duration"]
            shareable = "yes" if entry["shareable"] else "no"
            start_time = entry.get("start", "")
            end_time = entry.get("end", "")
            commitment_hash = entry.get("commitment_hash", "")
            
            # Escape commas in strings
            activity_type = activity_type.replace(',', ';')
            
            f.write(f'{date},{activity_type},{duration},{shareable},{start_time},{end_time},{commitment_hash}\n')
    
    return output_path


def print_timestamp_summary(ph_file_path: Path):
    """
    Print human-readable timestamp summary.
    """
    timestamps = extract_timestamps(ph_file_path)
    
    print(f"📅 Personal History Timestamp Analysis")
    print(f"File: {timestamps['file']}")
    print(f"Version: {timestamps['version']}")
    print(f"Total days: {timestamps['total_days']}")
    print("=" * 60)
    
    for day in timestamps["days"]:
        print(f"\n📅 {day['date']}")
        print(f"  Day commitment: {day['commitment_hash'][:16]}..." if day['commitment_hash'] else "  No day commitment")
        
        for activity in day["activities"]:
            print(f"  • {activity['type']}: {activity['duration']} min")
            
            if activity["exact_timestamps"]:
                if "start" in activity["exact_timestamps"]:
                    # Parse and format timestamp
                    try:
                        dt = datetime.fromisoformat(activity["exact_timestamps"]["start"].replace('Z', '+00:00'))
                        print(f"    Start: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    except:
                        print(f"    Start: {activity['exact_timestamps']['start']}")
                
                if "end" in activity["exact_timestamps"]:
                    try:
                        dt = datetime.fromisoformat(activity["exact_timestamps"]["end"].replace('Z', '+00:00'))
                        print(f"    End: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    except:
                        print(f"    End: {activity['exact_timestamps']['end']}")
            
            if activity["commitment_hash"]:
                print(f"    Commitment: {activity['commitment_hash'][:16]}...")


def main():
    """Command-line interface for timestamp utilities."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Personal History Timestamp Utilities")
    parser.add_argument("file", type=Path, help=".ph.json file to analyze")
    parser.add_argument("--export-csv", action="store_true", help="Export timestamps to CSV")
    parser.add_argument("--analyze", action="store_true", help="Analyze time patterns")
    parser.add_argument("--summary", action="store_true", help="Print human-readable summary")
    
    args = parser.parse_args()
    
    if not args.file.exists():
        print(f"Error: File not found: {args.file}")
        return
    
    if args.summary:
        print_timestamp_summary(args.file)
    
    elif args.analyze:
        analysis = analyze_time_patterns(args.file)
        print(json.dumps(analysis, indent=2))
    
    elif args.export_csv:
        output_file = export_timestamps_csv(args.file)
        print(f"✓ Timestamps exported to: {output_file}")
    
    else:
        # Default: show extracted timestamps
        timestamps = extract_timestamps(args.file)
        print(json.dumps(timestamps, indent=2))


if __name__ == "__main__":
    main()