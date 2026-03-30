#!/usr/bin/env python3
"""
Personal History v0.01 - Enhanced Command Line Interface
With smart duration parsing and time tracking features.
"""

import argparse
import json
import sys
import re
from datetime import datetime
from pathlib import Path
from .core import PersonalHistoryV001


def parse_duration(duration_str):
    """
    Parse duration string into minutes.
    Supports formats:
    - "90" (minutes)
    - "1h30" or "1hr30" (1 hour 30 minutes)
    - "2h" (2 hours)
    - "45m" (45 minutes)
    - "1.5h" (1.5 hours)
    - "1:30" (1 hour 30 minutes)
    """
    if not duration_str:
        return 0
    
    # If it's just a number, assume minutes
    if duration_str.isdigit():
        return int(duration_str)
    
    duration_str = duration_str.lower().replace('hr', 'h').replace('hour', 'h').replace('min', 'm').replace('minutes', 'm')
    
    # Try to parse as decimal hours
    if duration_str.endswith('h'):
        try:
            hours = float(duration_str[:-1])
            return int(hours * 60)
        except ValueError:
            pass
    
    # Try to parse as minutes
    if duration_str.endswith('m'):
        try:
            minutes = int(duration_str[:-1])
            return minutes
        except ValueError:
            pass
    
    # Try to parse as "1h30" format
    match = re.match(r'(\d+)\s*h\s*(\d+)?\s*m?', duration_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours * 60 + minutes
    
    # Try to parse as "1:30" format
    match = re.match(r'(\d+):(\d+)', duration_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        return hours * 60 + minutes
    
    # Try to parse as decimal
    try:
        return int(float(duration_str) * 60)  # Assume hours if decimal
    except ValueError:
        raise ValueError(f"Could not parse duration: {duration_str}. Use formats like '90', '1h30', '2h', '45m', '1.5h', or '1:30'")


def init_command(args):
    """Initialize a new Personal History identity"""
    print("Initializing Personal History identity...")
    
    identity = PersonalHistoryV001.create_identity(args.name)
    
    # Save identity to file
    identity_file = Path.home() / ".personal_history" / "identity.json"
    identity_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(identity_file, 'w') as f:
        json.dump(identity, f, indent=2)
    
    print(f"✓ Identity created: {identity['identity_hash'][:16]}...")
    if args.name:
        print(f"  Name: {args.name}")
    print(f"  Identity saved to: {identity_file}")
    print("\n⚠️  IMPORTANT: Backup your identity file securely!")
    
    return identity


def add_command(args):
    """Add an activity to pending list"""
    # Load identity
    identity_file = Path.home() / ".personal_history" / "identity.json"
    if not identity_file.exists():
        print("Error: No identity found. Run 'ph init' first.")
        return
    
    with open(identity_file, 'r') as f:
        identity = json.load(f)
    
    # Parse duration if provided
    duration_minutes = 0
    if args.duration:
        try:
            duration_minutes = parse_duration(args.duration)
            print(f"✓ Duration parsed: {duration_minutes} minutes ({args.duration})")
        except ValueError as e:
            print(f"Error: {e}")
            return
    
    # Create activity data
    activity_data = {}
    if args.project:
        activity_data["project"] = args.project
    if args.meal:
        activity_data["meal"] = args.meal
    if args.distance:
        activity_data["distance_km"] = args.distance
    if args.with_people:
        activity_data["with"] = args.with_people.split(',')
    
    activity = PersonalHistoryV001.create_activity(
        activity_type=args.type,
        data=activity_data,
        duration=duration_minutes,
        shareable=not args.private
    )
    
    # Save to pending activities
    pending_file = Path.home() / ".personal_history" / "pending.json"
    if pending_file.exists():
        with open(pending_file, 'r') as f:
            pending = json.load(f)
    else:
        pending = {"activities": []}
    
    # Add date if not specified
    if not args.date:
        args.date = datetime.now().strftime("%Y-%m-%d")
    
    # Find or create day entry
    day_entry = None
    for day in pending["activities"]:
        if day["date"] == args.date:
            day_entry = day
            break
    
    if day_entry is None:
        day_entry = {"date": args.date, "activities": []}
        pending["activities"].append(day_entry)
    
    # Add activity (remove private data for storage)
    activity_clean = activity.copy()
    activity_clean.pop("_private", None)
    day_entry["activities"].append(activity_clean)
    
    # Save pending activities
    with open(pending_file, 'w') as f:
        json.dump(pending, f, indent=2)
    
    print(f"✓ Activity added: {args.type}")
    if duration_minutes > 0:
        print(f"  Duration: {duration_minutes} minutes")
    print(f"  Date: {args.date}")
    if activity_data:
        print(f"  Data: {activity_data}")
    print(f"  Shareable: {not args.private}")
    print(f"  Pending activities: {len(pending['activities'])} days")


def start_command(args):
    """Start timing an activity"""
    # Load or create timers file
    timers_file = Path.home() / ".personal_history" / "timers.json"
    if timers_file.exists():
        with open(timers_file, 'r') as f:
            timers = json.load(f)
    else:
        timers = {"active_timers": {}}
    
    # Check if activity already being timed
    if args.activity in timers["active_timers"]:
        print(f"⚠️  Activity '{args.activity}' is already being timed")
        return
    
    # Start timer
    timers["active_timers"][args.activity] = {
        "start_time": datetime.now().isoformat(),
        "type": args.type if args.type else args.activity,
        "data": {}
    }
    
    # Add optional data
    if args.project:
        timers["active_timers"][args.activity]["data"]["project"] = args.project
    if args.meal:
        timers["active_timers"][args.activity]["data"]["meal"] = args.meal
    
    # Save timers
    with open(timers_file, 'w') as f:
        json.dump(timers, f, indent=2)
    
    print(f"⏱️  Started timing: {args.activity}")
    print(f"  Started at: {datetime.now().strftime('%H:%M:%S')}")
    if args.type:
        print(f"  Type: {args.type}")


def stop_command(args):
    """Stop timing an activity and add to pending"""
    # Load timers
    timers_file = Path.home() / ".personal_history" / "timers.json"
    if not timers_file.exists():
        print("No active timers found.")
        return
    
    with open(timers_file, 'r') as f:
        timers = json.load(f)
    
    # Check if activity is being timed
    if args.activity not in timers["active_timers"]:
        print(f"Activity '{args.activity}' is not being timed.")
        print(f"Active timers: {list(timers['active_timers'].keys())}")
        return
    
    # Calculate duration
    timer_data = timers["active_timers"][args.activity]
    start_time = datetime.fromisoformat(timer_data["start_time"])
    end_time = datetime.now()
    duration_seconds = (end_time - start_time).total_seconds()
    duration_minutes = int(duration_seconds / 60)
    
    # Remove from active timers
    del timers["active_timers"][args.activity]
    
    # Save updated timers
    with open(timers_file, 'w') as f:
        json.dump(timers, f, indent=2)
    
    print(f"⏱️  Stopped timing: {args.activity}")
    print(f"  Duration: {duration_minutes} minutes ({duration_seconds/3600:.2f} hours)")
    print(f"  Time range: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
    
    # Ask if user wants to add to pending
    if args.auto_add or input("\nAdd to pending activities? (y/N): ").lower() == 'y':
        # Create a temporary args object for add_command
        class TempArgs:
            pass
        
        temp_args = TempArgs()
        temp_args.type = timer_data["type"]
        temp_args.duration = str(duration_minutes)
        temp_args.date = datetime.now().strftime("%Y-%m-%d")
        temp_args.project = timer_data["data"].get("project")
        temp_args.meal = timer_data["data"].get("meal")
        temp_args.distance = None
        temp_args.with_people = None
        temp_args.private = False
        
        # Call add_command
        add_command(temp_args)


def tasks_command(args):
    """Show active timers and pending activities"""
    # Load timers
    timers_file = Path.home() / ".personal_history" / "timers.json"
    if timers_file.exists():
        with open(timers_file, 'r') as f:
            timers = json.load(f)
    else:
        timers = {"active_timers": {}}
    
    # Load pending activities
    pending_file = Path.home() / ".personal_history" / "pending.json"
    if pending_file.exists():
        with open(pending_file, 'r') as f:
            pending = json.load(f)
    else:
        pending = {"activities": []}
    
    print("📋 Personal History Tasks")
    print("=" * 60)
    
    # Show active timers
    if timers["active_timers"]:
        print("\n⏱️  ACTIVE TIMERS:")
        for activity, timer_data in timers["active_timers"].items():
            start_time = datetime.fromisoformat(timer_data["start_time"])
            elapsed = datetime.now() - start_time
            elapsed_minutes = int(elapsed.total_seconds() / 60)
            
            print(f"  • {activity}")
            print(f"    Type: {timer_data['type']}")
            print(f"    Started: {start_time.strftime('%H:%M:%S')}")
            print(f"    Elapsed: {elapsed_minutes} minutes ({elapsed.total_seconds()/3600:.2f} hours)")
            if timer_data["data"]:
                print(f"    Data: {timer_data['data']}")
            print()
    else:
        print("\n⏱️  No active timers")
        print("   Use: ph start <activity>")
    
    # Show pending activities
    total_pending = 0
    for day in pending.get("activities", []):
        total_pending += len(day.get("activities", []))
    
    if total_pending > 0:
        print(f"\n📝 PENDING ACTIVITIES: {total_pending} activities waiting to sync")
        print("   Use: ph pending (to see details)")
        print("   Use: ph sync (to sync to history file)")
    else:
        print("\n📝 No pending activities")
    
    print("\n" + "=" * 60)
    print("Quick commands:")
    print("  ph start <activity>      - Start timing an activity")
    print("  ph stop <activity>       - Stop timing and add to pending")
    print("  ph add <type> --duration - Add activity with duration")
    print("  ph sync                  - Sync pending to history file")


def pending_command(args):
    """Show pending activities"""
    pending_file = Path.home() / ".personal_history" / "pending.json"
    if not pending_file.exists():
        print("No pending activities.")
        return
    
    with open(pending_file, 'r') as f:
        pending = json.load(f)
    
    print("Pending Activities:")
    print("=" * 60)
    
    total_activities = 0
    for day in pending.get("activities", []):
        print(f"\n📅 {day['date']}:")
        for activity in day.get("activities", []):
            total_activities += 1
            shareable = "✓" if activity.get("shareable", True) else "✗"
            duration = activity.get("duration", 0)
            print(f"  {shareable} {activity['type']:15} {duration:3} min")
            if activity.get("data"):
                print(f"       {activity['data']}")
    
    print(f"\nTotal: {total_activities} activities pending sync")


def sync_command(args):
    """Sync pending activities to Personal History file"""
    # Load identity
    identity_file = Path.home() / ".personal_history" / "identity.json"
    if not identity_file.exists():
        print("Error: No identity found. Run 'ph init' first.")
        return
    
    with open(identity_file, 'r') as f:
        identity = json.load(f)
    
    # Load pending activities
    pending_file = Path.home() / ".personal_history" / "pending.json"
    if not pending_file.exists() or not pending_file.stat().st_size:
        print("No pending activities to sync.")
        return
    
    with open(pending_file, 'r') as f:
        pending = json.load(f)
    
    print("Syncing activities...")
    print("=" * 60)
    
    # Create or load Personal History file
    history_file = Path.home() / "personal_history.ph.json"
    if history_file.exists():
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = PersonalHistoryV001.create_file(identity, [])
    
    # Convert pending activities to days
    for pending_day in pending.get("activities", []):
        # Check if day already exists in history
        day_exists = False
        for history_day in history["timeline"]:
            if history_day["date"] == pending_day["date"]:
                # Merge activities
                history_day["activities"].extend(pending_day["activities"])
                day_exists = True
                break
        
        if not day_exists:
            # Create new day
            new_day = PersonalHistoryV001.create_day(
                date=pending_day["date"],
                activities=pending_day["activities"]
            )
            history["timeline"].append(new_day)
    
    # Save history file
    PersonalHistoryV001.save_file(history, history_file)
    
    # Clear pending activities
    with open(pending_file, 'w') as f:
        json.dump({"activities": []}, f)
    
    print(f"✓ Synced {len(pending.get('activities', []))} days to {history_file}")
    print("✓ Pending activities cleared")


def verify_command(args):
    """Verify Personal History file"""
    from .schema import validate_ph_file
    
    try:
        with open(args.file, 'r') as f:
            data = json.load(f)
        
        validate_ph_file(data)
        print(f"✓ {args.file} is a valid Personal History v0.01 file")
        
    except Exception as e:
        print(f"❌ {args.file} is invalid: {e}")
        sys.exit(1)


def analyze_command(args):
    """Analyze time from Personal History file"""
    # If no file specified, use default
    if args.file is None:
        default_file = Path.home() / "personal_history.ph.json"
        if default_file.exists():
            args.file = default_file
            print(f"Using default file: {args.file}")
        else:
            print("Error: No file specified and default file not found.")
            print(f"Default location: {default_file}")
            print("Run 'ph sync' first to create a history file, or specify a file.")
            sys.exit(1)
    
    try:
        with open(args.file, 'r') as f:
            data = json.load(f)
        
        print(f"Analyzing: {args.file}")
        print("=" * 60)
        
        total_days = len(data.get("timeline", []))
        total_activities = 0
        total_minutes = 0
        
        for day in data.get("timeline", []):
            total_activities += len(day.get("activities", []))
            for activity in day.get("activities", []):
                total_minutes += activity.get("duration", 0)
        
        print(f"Total days: {total_days}")
        print(f"Total activities: {total_activities}")
        print(f"Total time: {total_minutes} minutes ({total_minutes/60:.1f} hours)")
        
        if args.export_shareable:
            print("\nExporting shareable activities...")
            shareable_activities = []
            for day in data.get("timeline", []):
                for activity in day.get("activities", []):
                    if activity.get("shareable", True):
                        shareable_activities.append({
                            "date": day["date"],
                            "type": activity["type"],
                            "duration": activity.get("duration", 0),
                            "data": activity.get("data", {})
                        })
            
            export_file = args.file.with_suffix('.shareable.json')
            with open(export_file, 'w') as f:
                json.dump(shareable_activities, f, indent=2)
            print(f"✓ Exported {len(shareable_activities)} shareable activities to {export_file}")
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        sys.exit(1)


def demo_command(args):
    """Run demonstration of v0.01 features"""
    print("Personal History v0.01 - Demonstration")
    print("=" * 60)
    
    # Create demo identity
    identity = PersonalHistoryV001.create_identity("Demo User")
    print(f"1. Identity created: {identity['identity_hash'][:16]}...")
    
    # Create activities
    work_activity = PersonalHistoryV001.create_activity(
        "work",
        {"project": "demo"},
        120
    )
    print(f"2. Activity created: {work_activity['type']}")
    
    # Create day
    day = PersonalHistoryV001.create_day(
        date="2024-01-01",
        activities=[work_activity]
    )
    print(f"3. Day created: {day['date']} with {len(day['activities'])} activities")
    
    # Create file
    ph_file = PersonalHistoryV001.create_file(identity, [day])
    ph_file["signature"] = "a" * 128
    print(f"4. File created with version: {ph_file['version']}")
    
    # Validate
    from .schema import validate_ph_file
    validate_ph_file(ph_file)
    print("5. File validation passed")
    
    print("\n🎉 Demonstration complete!")
    print("All v0.01 features are working correctly.")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Personal History v0.01 - Command Line Interface with Time Tracking",
        prog="ph"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new identity")
    init_parser.add_argument("--name", help="Your name (optional)")
    
    # Add command (with smart duration parsing)
    add_parser = subparsers.add_parser("add", help="Add activity to pending")
    add_parser.add_argument("type", help="Activity type (work, family, exercise, etc.)")
    add_parser.add_argument("--duration", help="Duration in minutes or smart format (90, 1h30, 2h, 45m, 1.5h, 1:30)")
    add_parser.add_argument("--date", help="Date (YYYY-MM-DD, defaults to today)")
    add_parser.add_argument("--project", help="Project name (for work activities)")
    add_parser.add_argument("--meal", help="Meal type (for cooking/eating activities)")
    add_parser.add_argument("--distance", type=float, help="Distance in km (for exercise)")
    add_parser.add_argument("--with-people", help="People involved (comma-separated)")
    add_parser.add_argument("--private", action="store_true", help="Mark as private (not shareable)")
    
    # Start command (begin timing an activity)
    start_parser = subparsers.add_parser("start", help="Start timing an activity")
    start_parser.add_argument("activity", help="Activity name to start timing")
    start_parser.add_argument("--type", help="Activity type (defaults to activity name)")
    start_parser.add_argument("--project", help="Project name")
    start_parser.add_argument("--meal", help="Meal type")
    
    # Stop command (stop timing and add to pending)
    stop_parser = subparsers.add_parser("stop", help="Stop timing an activity")
    stop_parser.add_argument("activity", help="Activity name to stop timing")
    stop_parser.add_argument("--auto-add", action="store_true", help="Automatically add to pending without confirmation")
    
    # Tasks command (show active timers and pending)
    subparsers.add_parser("tasks", help="Show active timers and pending activities")
    
    # Pending command
    subparsers.add_parser("pending", help="Show pending activities")
    
    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync pending activities to history file")
    sync_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify Personal History file")
    verify_parser.add_argument("file", type=Path, help=".ph.json file to verify")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze time from Personal History file")
    analyze_parser.add_argument("file", type=Path, nargs="?", default=None, help=".ph.json file to analyze (default: ~/personal_history.ph.json)")
    analyze_parser.add_argument("--export-shareable", action="store_true", help="Export shareable activities")
    
    # Demo command
    subparsers.add_parser("demo", help="Run demonstration of v0.01 features")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    try:
        if args.command == "init":
            init_command(args)
        elif args.command == "add":
            add_command(args)
        elif args.command == "start":
            start_command(args)
        elif args.command == "stop":
            stop_command(args)
        elif args.command == "tasks":
            tasks_command(args)
        elif args.command == "pending":
            pending_command(args)
        elif args.command == "sync":
            sync_command(args)
        elif args.command == "verify":
            verify_command(args)
        elif args.command == "analyze":
            analyze_command(args)
        elif args.command == "demo":
            demo_command(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
