"""
CLI View for Personal History v0.01
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from ..controllers.history_controller import HistoryController
from ..controllers.time_tracking_controller import TimeTrackingController
from ..controllers.validation_controller import ValidationController
from ..utils.duration_parser import parse_duration


class CLIView:
    """Command Line Interface View for Personal History"""
    
    def __init__(self):
        self.history_controller = HistoryController()
        self.time_controller = TimeTrackingController()
        self.validation_controller = ValidationController()
    
    def run(self, args=None):
        """Run CLI with given arguments"""
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return
        
        try:
            self._execute_command(parsed_args)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            description="Personal History v0.01 - Command Line Interface with Time Tracking",
            prog="ph"
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Command to execute")
        
        # Init command
        init_parser = subparsers.add_parser("init", help="Initialize new identity")
        init_parser.add_argument("--name", help="Your name (optional)")
        
        # Add command
        add_parser = subparsers.add_parser("add", help="Add activity to pending")
        add_parser.add_argument("type", help="Activity type (work, family, exercise, etc.)")
        add_parser.add_argument("--duration", help="Duration in minutes or smart format")
        add_parser.add_argument("--date", help="Date (YYYY-MM-DD, defaults to today)")
        add_parser.add_argument("--project", help="Project name")
        add_parser.add_argument("--meal", help="Meal type")
        add_parser.add_argument("--distance", type=float, help="Distance in km")
        add_parser.add_argument("--with-people", help="People involved (comma-separated)")
        add_parser.add_argument("--private", action="store_true", help="Mark as private")
        
        # Start command
        start_parser = subparsers.add_parser("start", help="Start timing an activity")
        start_parser.add_argument("activity", help="Activity name to start timing")
        start_parser.add_argument("--type", help="Activity type (defaults to activity name)")
        start_parser.add_argument("--project", help="Project name")
        start_parser.add_argument("--meal", help="Meal type")
        
        # Stop command
        stop_parser = subparsers.add_parser("stop", help="Stop timing an activity")
        stop_parser.add_argument("activity", help="Activity name to stop timing")
        stop_parser.add_argument("--auto-add", action="store_true", help="Auto-add to pending")
        
        # Tasks command
        subparsers.add_parser("tasks", help="Show active timers and pending activities")
        
        # Pending command
        subparsers.add_parser("pending", help="Show pending activities")
        
        # Sync command
        sync_parser = subparsers.add_parser("sync", help="Sync pending to history file")
        sync_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
        
        # Verify command
        verify_parser = subparsers.add_parser("verify", help="Verify Personal History file")
        verify_parser.add_argument("file", type=Path, help=".ph.json file to verify")
        
        # Analyze command
        analyze_parser = subparsers.add_parser("analyze", help="Analyze time from file")
        analyze_parser.add_argument("file", type=Path, nargs="?", default=None, 
                                   help=".ph.json file (default: ~/personal_history.ph.json)")
        analyze_parser.add_argument("--export-shareable", action="store_true", 
                                   help="Export shareable activities")
        
        # Timestamps command
        timestamps_parser = subparsers.add_parser("timestamps", help="Extract and analyze timestamps")
        timestamps_parser.add_argument("file", type=Path, nargs="?", default=None,
                                      help=".ph.json file (default: ~/personal_history.ph.json)")
        timestamps_parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
        timestamps_parser.add_argument("--analyze", action="store_true", help="Analyze time patterns")
        timestamps_parser.add_argument("--summary", action="store_true", help="Print summary")
        
        # Demo command
        subparsers.add_parser("demo", help="Run demonstration")
        
        return parser
    
    def _execute_command(self, args):
        """Execute the parsed command"""
        command_methods = {
            "init": self._handle_init,
            "add": self._handle_add,
            "start": self._handle_start,
            "stop": self._handle_stop,
            "tasks": self._handle_tasks,
            "pending": self._handle_pending,
            "sync": self._handle_sync,
            "verify": self._handle_verify,
            "analyze": self._handle_analyze,
            "timestamps": self._handle_timestamps,
            "demo": self._handle_demo,
        }
        
        if args.command in command_methods:
            command_methods[args.command](args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    
    def _handle_init(self, args):
        """Handle init command"""
        print("Initializing Personal History identity...")
        
        identity = self.history_controller.create_identity(args.name)
        self.history_controller.save_identity(identity)
        
        print(f"✓ Identity created: {identity.identity_hash[:16]}...")
        if args.name:
            print(f"  Name: {args.name}")
        print(f"  Identity saved to: {self.history_controller.data_dir}/identity.json")
        print("\n⚠️  IMPORTANT: Backup your identity file securely!")
    
    def _handle_add(self, args):
        """Handle add command"""
        # Parse duration
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
        
        # Create activity
        activity = self.history_controller.create_activity(
            activity_type=args.type,
            data=activity_data,
            duration=duration_minutes,
            shareable=not args.private
        )
        
        # Add to pending
        date = args.date or datetime.now().strftime("%Y-%m-%d")
        self.history_controller.add_to_pending(activity, date)
        
        print(f"✓ Activity added: {args.type}")
        if duration_minutes > 0:
            print(f"  Duration: {duration_minutes} minutes")
        print(f"  Date: {date}")
        if activity_data:
            print(f"  Data: {activity_data}")
        print(f"  Shareable: {not args.private}")
    
    def _handle_start(self, args):
        """Handle start command"""
        # Prepare activity data
        activity_data = {}
        if args.project:
            activity_data["project"] = args.project
        if args.meal:
            activity_data["meal"] = args.meal
        
        try:
            self.time_controller.start_timer(
                activity_name=args.activity,
                activity_type=args.type or args.activity,
                data=activity_data
            )
            
            print(f"⏱️  Started timing: {args.activity}")
            print(f"  Started at: {datetime.now().strftime('%H:%M:%S')}")
            if args.type:
                print(f"  Type: {args.type}")
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def _handle_stop(self, args):
        """Handle stop command"""
        try:
            # Stop timer
            timer_result = self.time_controller.stop_timer(args.activity)
            
            print(f"⏱️  Stopped timing: {args.activity}")
            print(f"  Duration: {timer_result['duration_minutes']} minutes "
                  f"({timer_result['duration_seconds']/3600:.2f} hours)")
            print(f"  Time range: {timer_result['start_time'].strftime('%H:%M')} - "
                  f"{timer_result['end_time'].strftime('%H:%M')}")
            
            # Ask if user wants to add to pending
            if args.auto_add or input("\nAdd to pending activities? (y/N): ").lower() == 'y':
                activity = self.time_controller.create_activity_from_timer(timer_result)
                self.history_controller.add_to_pending(activity)
                print("✓ Activity added to pending")
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def _handle_tasks(self, args):
        """Handle tasks command"""
        # Get active timers
        timer_summary = self.time_controller.get_timer_summary()
        
        # Get pending activities
        pending = self.history_controller.get_pending_activities()
        total_pending = sum(
            len(day.get("activities", []))
            for day in pending.get("activities", [])
        )
        
        print("📋 Personal History Tasks")
        print("=" * 60)
        
        # Show active timers
        if timer_summary["active_timers"] > 0:
            print("\n⏱️  ACTIVE TIMERS:")
            for timer in timer_summary["timers"]:
                print(f"  • {timer['activity_name']}")
                print(f"    Type: {timer['activity_type']}")
                print(f"    Started: {timer['start_time'].strftime('%H:%M:%S')}")
                print(f"    Elapsed: {timer['elapsed_minutes']} minutes "
                      f"({timer['elapsed_hours']:.2f} hours)")
                if timer["data"]:
                    print(f"    Data: {timer['data']}")
                print()
        else:
            print("\n⏱️  No active timers")
            print("   Use: ph start <activity>")
        
        # Show pending activities
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
    
    def _handle_pending(self, args):
        """Handle pending command"""
        pending = self.history_controller.get_pending_activities()
        
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
    
    def _handle_sync(self, args):
        """Handle sync command"""
        print("Syncing activities...")
        print("=" * 60)
        
        try:
            ph_file = self.history_controller.sync_to_file()
            print(f"✓ Synced to: {Path.home() / 'personal_history.ph.json'}")
            print(f"  Days: {len(ph_file.timeline)}")
            print(f"  Activities: {ph_file.get_activity_count()}")
            print(f"  Total time: {ph_file.get_total_duration()} minutes")
            print("✓ Pending activities cleared")
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def _handle_verify(self, args):
        """Handle verify command"""
        result = self.validation_controller.validate_file(args.file)
        report = self.validation_controller.generate_validation_report(result)
        print(report)
        
        if not result["valid"]:
            sys.exit(1)
    
    def _handle_analyze(self, args):
        """Handle analyze command"""
        # Use default file if not specified
        filepath = args.file
        if filepath is None:
            filepath = Path.home() / "personal_history.ph.json"
            if not filepath.exists():
                print(f"Error: Default file not found: {filepath}")
                print("Run 'ph sync' first to create a history file, or specify a file.")
                sys.exit(1)
            print(f"Using default file: {filepath}")
        
        analysis = self.history_controller.analyze_file(filepath)
        
        print(f"Analyzing: {filepath}")
        print("=" * 60)
        print(f"Total days: {analysis['total_days']}")
        print(f"Total activities: {analysis['total_activities']}")
        print(f"Total time: {analysis['total_duration_minutes']} minutes "
              f"({analysis['total_duration_hours']:.1f} hours)")
        
        if analysis.get('signature_valid') is not None:
            if analysis['signature_valid']:
                print("Signature: ✅ valid")
            else:
                print("Signature: ❌ invalid")
        
        if analysis['file_valid']:
            print("File integrity: ✅ verified")
        else:
            print("File integrity: ❌ failed")
    
    def _handle_timestamps(self, args):
        """Handle timestamps command"""
        from ..timestamps import (
            extract_timestamps,
            analyze_time_patterns,
            export_timestamps_csv,
            print_timestamp_summary
        )
        
        # Use default file if not specified
        filepath = args.file
        if filepath is None:
            filepath = Path.home() / "personal_history.ph.json"
            if not filepath.exists():
                print(f"Error: Default file not found: {filepath}")
                print("Run 'ph sync' first to create a history file, or specify a file.")
                sys.exit(1)
            print(f"Using default file: {filepath}")
        
        if args.summary:
            print_timestamp_summary(filepath)
        elif args.analyze:
            analysis = analyze_time_patterns(filepath)
            import json
            print(json.dumps(analysis, indent=2))
        elif args.export_csv:
            output_file = export_timestamps_csv(filepath)
            print(f"✓ Timestamps exported to: {output_file}")
        else:
            timestamps = extract_timestamps(filepath)
            import json
            print(json.dumps(timestamps, indent=2))
    
    def _handle_demo(self, args):
        """Handle demo command"""
        print("Personal History v0.01 - Demonstration")
        print("=" * 60)
        
        # This would demonstrate all features
        print("1. Creating identity...")
        identity = self.history_controller.create_identity("Demo User")
        print(f"   Identity created: {identity.identity_hash[:16]}...")
        
        print("2. Creating activity...")
        activity = self.history_controller.create_activity(
            "work", {"project": "demo"}, 120
        )
        print(f"   Activity created: {activity.type}")
        
        print("3. Creating day...")
        day = self.history_controller.create_day("2024-01-01", [activity])
        print(f"   Day created: {day.date} with {len(day.activities)} activities")
        
        print("4. Creating file...")
        ph_file = self.history_controller.create_file(identity, [day])
        print(f"   File created with version: {ph_file.VERSION}")
        
        print("\n🎉 Demonstration complete!")
        print("All v0.01 features are working correctly.")


def main():
    """Main CLI entry point"""
    cli = CLIView()
    cli.run()


if __name__ == "__main__":
    main()