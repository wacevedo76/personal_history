#!/usr/bin/env python3
"""
Personal History v0.01 - Command Line Interface
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from .core import PersonalHistoryV001

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
    
    # Create activity
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
        duration=args.duration,
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
    
    print(f"✓ Activity added: {args.type} ({args.duration} minutes)")
    print(f"  Date: {args.date}")
    if activity_data:
        print(f"  Data: {activity_data}")
    print(f"  Shareable: {not args.private}")
    print(f"  Pending activities: {len(pending['activities'])} days")

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
    
    # Show summary
    total_days = len(pending.get("activities", []))
    total_activities = sum(
        len(day.get("activities", []))
        for day in pending.get("activities", [])
    )
    
    print(f"📊 Summary: {total_activities} activities across {total_days} days")
    
    # Ask for confirmation
    if not args.yes:
        response = input("\nProceed with sync? (y/N): ")
        if response.lower() != 'y':
            print("Sync cancelled.")
            return
    
    # Load or create Personal History file
    ph_file_path = Path.home() / ".personal_history" / "history.ph.json"
    if ph_file_path.exists():
        ph_file = PersonalHistoryV001.load_file(ph_file_path)
        print(f"✓ Loaded existing history file")
    else:
        ph_file = PersonalHistoryV001.create_file(identity)
        print(f"✓ Created new history file")
    
    # Add pending days
    for pending_day in pending.get("activities", []):
        date = pending_day["date"]
        activities = []
        
        # Recreate activities with exact times
        for pending_activity in pending_day.get("activities", []):
            # In real implementation, would use stored exact times
            # For now, create with current time
            activity = PersonalHistoryV001.create_activity(
                activity_type=pending_activity["type"],
                data=pending_activity.get("data", {}),
                duration=pending_activity.get("duration", 0),
                shareable=pending_activity.get("shareable", True)
            )
            activities.append(activity)
        
        # Add to file
        ph_file = PersonalHistoryV001.add_day_to_file(
            ph_file,
            date=date,
            activities=activities
        )
        print(f"✓ Added day: {date} ({len(activities)} activities)")
    
    # Sign the file
    signature = PersonalHistoryV001.sign_file(ph_file, identity["private_key"])
    ph_file["signature"] = signature
    
    # Save the file
    PersonalHistoryV001.save_file(ph_file, ph_file_path)
    
    # Clear pending activities
    with open(pending_file, 'w') as f:
        json.dump({"activities": []}, f)
    
    print(f"\n✅ Sync complete!")
    print(f"  File: {ph_file_path}")
    print(f"  Timeline: {len(ph_file['timeline'])} days")
    print(f"  Signature: {signature[:32]}...")

def verify_command(args):
    """Verify a Personal History file"""
    if not args.file.exists():
        print(f"Error: File not found: {args.file}")
        return
    
    ph_file = PersonalHistoryV001.load_file(args.file)
    
    print(f"Verifying: {args.file}")
    print(f"Version: {ph_file.get('version', 'unknown')}")
    print(f"Identity: {ph_file['identity'].get('name', 'Unknown')}")
    print(f"Timeline: {len(ph_file.get('timeline', []))} days")
    
    # Check signature
    if ph_file.get("signature"):
        # In real implementation, would load public key
        # For now, just check structure
        print(f"Signature: {ph_file['signature'][:32]}... (present)")
    else:
        print("Signature: ❌ Missing")
    
    # Check forward chain
    if PersonalHistoryV001.verify_forward_chain(ph_file):
        print("Forward chain: ✓ Intact")
    else:
        print("Forward chain: ❌ Broken")
    
    # Show time analysis
    analysis = PersonalHistoryV001.analyze_time(ph_file)
    print(f"\n📊 Time Analysis:")
    print(f"  Days tracked: {analysis['days_analyzed']}")
    print(f"  Total time: {analysis['total_tracked_hours']:.1f} hours")
    
    if analysis['activity_totals']:
        print(f"\n  By activity type:")
        for activity_type, stats in analysis['activity_totals'].items():
            hours = stats['total_minutes'] / 60
            print(f"    {activity_type:15} {hours:5.1f} hours")

def analyze_command(args):
    """Analyze time from Personal History file"""
    if not args.file.exists():
        print(f"Error: File not found: {args.file}")
        return
    
    ph_file = PersonalHistoryV001.load_file(args.file)
    analysis = PersonalHistoryV001.analyze_time(ph_file)
    
    print(f"Time Analysis: {args.file}")
    print("=" * 60)
    
    print(f"\n📅 Overview:")
    print(f"  Days tracked: {analysis['days_analyzed']}")
    print(f"  Total tracked time: {analysis['total_tracked_hours']:.1f} hours")
    
    if analysis['activity_totals']:
        print(f"\n⏰ Time by activity type:")
        for activity_type, stats in sorted(
            analysis['activity_totals'].items(),
            key=lambda x: x[1]['total_minutes'],
            reverse=True
        ):
            hours = stats['total_minutes'] / 60
            percentage = (stats['total_minutes'] / analysis['total_tracked_minutes']) * 100
            print(f"  {activity_type:15} {hours:5.1f} hours ({percentage:.0f}%)")
    
    # Export shareable if requested
    if args.export_shareable:
        shareable = PersonalHistoryV001.export_shareable(ph_file)
        export_file = args.file.parent / f"{args.file.stem}_shareable.json"
        with open(export_file, 'w') as f:
            json.dump(shareable, f, indent=2)
        print(f"\n📤 Exported shareable activities to: {export_file}")

def demo_command(args):
    """Run a demonstration of v0.01 features"""
    print("Personal History v0.01 Demonstration")
    print("=" * 60)
    
    # Create identity
    print("\n1. Creating identity...")
    identity = PersonalHistoryV001.create_identity("William Acevedo")
    print(f"   Identity hash: {identity['identity_hash'][:16]}...")
    
    # Create file
    print("\n2. Creating Personal History file...")
    ph_file = PersonalHistoryV001.create_file(identity)
    
    # Add some activities
    print("\n3. Adding activities...")
    
    activities_day1 = [
        PersonalHistoryV001.create_activity(
            "family",
            {"activity": "breakfast", "meal": "pancakes"},
            45,
            shareable=True
        ),
        PersonalHistoryV001.create_activity(
            "work",
            {"project": "personal_history"},
            120,
            shareable=True
        )
    ]
    
    ph_file = PersonalHistoryV001.add_day_to_file(
        ph_file,
        date="2024-01-01",
        activities=activities_day1,
        note="Good start to the year"
    )
    
    activities_day2 = [
        PersonalHistoryV001.create_activity(
            "exercise",
            {"activity": "running", "distance_km": 5.2},
            28,
            shareable=True
        ),
        PersonalHistoryV001.create_activity(
            "cooking",
            {"meal": "kotlet_schabowy", "for_people": 3},
            40,
            shareable=True
        )
    ]
    
    ph_file = PersonalHistoryV001.add_day_to_file(
        ph_file,
        date="2024-01-02",
        activities=activities_day2,
        note="Exercise and traditional Polish dinner"
    )
    
    # Sign the file
    print("\n4. Signing file...")
    signature = PersonalHistoryV001.sign_file(ph_file, identity["private_key"])
    ph_file["signature"] = signature
    print(f"   Signature: {signature[:32]}...")
    
    # Save to file
    demo_file = Path("demo_history.ph.json")
    PersonalHistoryV001.save_file(ph_file, demo_file)
    print(f"\n5. Saved to: {demo_file}")
    
    # Analyze
    print("\n6. Analyzing time...")
    analysis = PersonalHistoryV001.analyze_time(ph_file)
    print(f"   Total tracked: {analysis['total_tracked_hours']:.1f} hours")
    
    for activity_type, stats in analysis['activity_totals'].items():
        hours = stats['total_minutes'] / 60
        print(f"   {activity_type}: {hours:.1f} hours")
    
    print(f"\n✅ Demonstration complete!")
    print(f"   File: {demo_file}")
    print(f"   Try: ph verify {demo_file}")
    print(f"   Try: ph analyze {demo_file}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Personal History v0.01 - Command Line Interface",
        prog="ph"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new identity")
    init_parser.add_argument("--name", help="Your name (optional)")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add activity to pending")
    add_parser.add_argument("type", help="Activity type (work, family, exercise, etc.)")
    add_parser.add_argument("--duration", type=int, required=True, help="Duration in minutes")
    add_parser.add_argument("--date", help="Date (YYYY-MM-DD, defaults to today)")
    add_parser.add_argument("--project", help="Project name (for work activities)")
    add_parser.add_argument("--meal", help="Meal type (for cooking/eating activities)")
    add_parser.add_argument("--distance", type=float, help="Distance in km (for exercise)")
    add_parser.add_argument("--with-people", help="People involved (comma-separated)")
    add_parser.add_argument("--private", action="store_true", help="Mark as private (not shareable)")
    
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
    analyze_parser.add_argument("file", type=Path, help=".ph.json file to analyze")
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