"""
Logging Integration for Personal History PH Command

This module shows how to integrate the logging module with the existing PH command structure.
It provides patched versions of controllers and views with logging enabled.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Import the logging module
from .logging_module import get_logger, log_command_execution, log_operation, LoggingContext


class LoggingHistoryController:
    """
    History Controller with integrated logging.
    This wraps the original HistoryController and adds logging to all operations.
    """
    
    def __init__(self, original_controller, logger=None):
        self.controller = original_controller
        self.logger = logger or get_logger()
        
        # Log controller initialization
        self.logger.log_operation("HistoryController initialized", {
            "data_dir": str(self.controller.data_dir)
        })
    
    @log_operation("create_identity", get_logger())
    def create_identity(self, name: Optional[str] = None):
        """Create a new identity with logging"""
        with LoggingContext("create_identity", self.logger, {"name": name}):
            result = self.controller.create_identity(name)
            self.logger.log_operation("identity_created", {
                "identity_hash": result.identity_hash[:16] + "...",
                "name": name or "anonymous"
            })
            return result
    
    @log_operation("save_identity", get_logger())
    def save_identity(self, identity):
        """Save identity with logging"""
        with LoggingContext("save_identity", self.logger, {
            "identity_hash": identity.identity_hash[:16] + "..."
        }):
            self.controller.save_identity(identity)
            self.logger.log_operation("identity_saved", {
                "file": str(self.controller.data_dir / "identity.json")
            })
    
    @log_operation("create_activity", get_logger())
    def create_activity(self, activity_type: str, data: Dict, duration: int, shareable: bool = True):
        """Create activity with logging"""
        with LoggingContext("create_activity", self.logger, {
            "type": activity_type,
            "duration": duration,
            "shareable": shareable
        }):
            result = self.controller.create_activity(activity_type, data, duration, shareable)
            self.logger.log_operation("activity_created", {
                "activity_id": result.id[:16] + "..." if hasattr(result, 'id') else "unknown",
                "type": activity_type,
                "duration": duration
            })
            return result
    
    @log_operation("add_to_pending", get_logger())
    def add_to_pending(self, activity, date: Optional[str] = None):
        """Add activity to pending with logging"""
        date_str = date or datetime.now().strftime("%Y-%m-%d")
        with LoggingContext("add_to_pending", self.logger, {
            "date": date_str,
            "activity_type": activity.type if hasattr(activity, 'type') else "unknown"
        }):
            self.controller.add_to_pending(activity, date)
            self.logger.log_operation("activity_added_to_pending", {
                "date": date_str,
                "activity_type": activity.type if hasattr(activity, 'type') else "unknown"
            })
    
    @log_operation("sync_to_file", get_logger())
    def sync_to_file(self):
        """Sync pending activities to file with logging"""
        with LoggingContext("sync_to_file", self.logger, {}):
            result = self.controller.sync_to_file()
            
            # Log sync results
            if hasattr(result, 'timeline'):
                self.logger.log_operation("sync_completed", {
                    "days": len(result.timeline),
                    "activities": result.get_activity_count() if hasattr(result, 'get_activity_count') else "unknown",
                    "file_path": str(Path.home() / "personal_history.ph.json")
                })
            else:
                self.logger.log_operation("sync_completed", {
                    "result_type": type(result).__name__
                })
            
            return result
    
    # Delegate other methods to the original controller
    def __getattr__(self, name):
        """Delegate unknown attributes to the original controller"""
        return getattr(self.controller, name)


class LoggingCLIView:
    """
    CLI View with integrated logging.
    This wraps the original CLIView and adds logging to command execution.
    """
    
    def __init__(self, original_view=None, logger=None):
        self.view = original_view
        self.logger = logger or get_logger()
        
        # Log view initialization
        self.logger.log_operation("CLIView initialized", {})
    
    @log_command_execution(get_logger())
    def run(self, args=None):
        """Run CLI with logging"""
        # Parse arguments to get command name
        import argparse
        
        # Create a temporary parser to get the command
        temp_parser = self._create_temp_parser()
        try:
            parsed_args = temp_parser.parse_known_args(args)[0]
            command = parsed_args.command
        except:
            command = "unknown"
        
        # Log command execution
        self.logger.log_command("ph", {
            "command": command,
            "args": args or sys.argv[1:],
            "full_command": "ph " + " ".join(args) if args else " ".join(sys.argv[1:])
        })
        
        # Execute the command
        return self.view.run(args)
    
    def _create_temp_parser(self):
        """Create a temporary parser to extract command name"""
        import argparse
        parser = argparse.ArgumentParser(add_help=False)
        subparsers = parser.add_subparsers(dest="command")
        
        # Add all known commands
        for cmd in ["init", "add", "start", "stop", "tasks", "pending", 
                   "sync", "verify", "analyze", "timestamps", "demo"]:
            subparsers.add_parser(cmd)
        
        return parser
    
    @log_command_execution(get_logger())
    def _execute_command(self, args):
        """Execute command with logging"""
        # Log the specific command being executed
        self.logger.log_operation(f"execute_command_{args.command}", {
            "command": args.command,
            "args": vars(args)
        })
        
        return self.view._execute_command(args)
    
    # Wrap individual command handlers with logging
    @log_operation("handle_init", get_logger())
    def _handle_init(self, args):
        self.logger.log_user_interaction("init_command", {"name": args.name})
        return self.view._handle_init(args)
    
    @log_operation("handle_add", get_logger())
    def _handle_add(self, args):
        self.logger.log_user_interaction("add_command", {
            "type": args.type,
            "duration": args.duration,
            "date": args.date,
            "project": args.project
        })
        return self.view._handle_add(args)
    
    @log_operation("handle_start", get_logger())
    def _handle_start(self, args):
        self.logger.log_user_interaction("start_command", {
            "activity": args.activity,
            "type": args.type,
            "project": args.project
        })
        return self.view._handle_start(args)
    
    @log_operation("handle_stop", get_logger())
    def _handle_stop(self, args):
        self.logger.log_user_interaction("stop_command", {
            "activity": args.activity,
            "auto_add": args.auto_add
        })
        return self.view._handle_stop(args)
    
    @log_operation("handle_sync", get_logger())
    def _handle_sync(self, args):
        self.logger.log_user_interaction("sync_command", {"skip_confirmation": args.yes})
        return self.view._handle_sync(args)
    
    # Delegate other methods
    def __getattr__(self, name):
        """Delegate unknown attributes to the original view"""
        return getattr(self.view, name)


def create_logging_integrated_cli():
    """
    Create a fully logging-integrated CLI view.
    This is the main entry point for using logging with PH command.
    """
    from .v001.views.cli_view import CLIView
    from .v001.controllers.history_controller import HistoryController
    
    # Set up logging
    logger = get_logger()
    
    # Create original components
    original_view = CLIView()
    
    # Wrap with logging
    logging_view = LoggingCLIView(original_view, logger)
    
    # Also wrap the controller inside the view
    if hasattr(original_view, 'history_controller'):
        original_view.history_controller = LoggingHistoryController(
            original_view.history_controller, logger
        )
    
    return logging_view


def patch_existing_cli():
    """
    Patch the existing CLI view to add logging.
    This modifies the existing CLIView class in-place.
    """
    from .v001.views.cli_view import CLIView
    
    # Store original methods
    original_run = CLIView.run
    original_execute_command = CLIView._execute_command
    
    # Get logger
    logger = get_logger()
    
    # Create patched run method
    @log_command_execution(logger)
    def patched_run(self, args=None):
        # Log command execution
        import sys
        cmd_args = args or sys.argv[1:]
        logger.log_command("ph", {
            "args": cmd_args,
            "full_command": "ph " + " ".join(cmd_args) if cmd_args else "ph"
        })
        
        # Call original method
        return original_run(self, args)
    
    # Create patched execute_command method
    def patched_execute_command(self, args):
        # Log command execution
        logger.log_operation(f"execute_command_{args.command}", {
            "command": args.command,
            "args": vars(args)
        })
        
        # Call original method
        return original_execute_command(self, args)
    
    # Apply patches
    CLIView.run = patched_run
    CLIView._execute_command = patched_execute_command
    
    logger.log_operation("cli_patched", {"status": "success"})
    
    return CLIView


class LoggingCLIEntryPoint:
    """
    Alternative entry point that creates a fully logged CLI.
    Use this as your main CLI entry point instead of the original.
    """
    
    @staticmethod
    def main():
        """Main entry point with logging"""
        # Set up logging
        logger = get_logger()
        
        try:
            # Create logging-integrated CLI
            cli = create_logging_integrated_cli()
            
            # Run with arguments
            cli.run()
            
            # Log successful completion
            logger.log_operation("cli_completed", {"status": "success"})
            
        except Exception as e:
            # Log error
            logger.log_error("cli_error", str(e), {
                "exception_type": type(e).__name__
            })
            raise


# Utility functions for log analysis

def analyze_logs(days: int = 7) -> Dict[str, Any]:
    """Analyze recent logs and generate a report"""
    logger = get_logger()
    
    # Get log summary from logger
    summary = logger.get_log_summary(days)
    
    # Add analysis
    analysis = {
        "summary": summary,
        "recommendations": [],
        "insights": []
    }
    
    # Example insights (would be populated from actual log analysis)
    if summary.get("error_count", 0) > 0:
        analysis["recommendations"].append(
            "Review error logs to identify common failure patterns"
        )
    
    if summary.get("total_commands", 0) < 10:
        analysis["insights"].append(
            "Low command usage - consider adding more automation or reminders"
        )
    
    return analysis


def export_logs(output_format: str = "json", output_file: Optional[Path] = None):
    """Export logs in specified format"""
    logger = get_logger()
    
    if output_format == "json":
        # Export as JSON
        summary = logger.get_log_summary(30)  # Last 30 days
        
        if output_file:
            import json
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=2)
            return output_file
        else:
            return summary
    
    elif output_format == "csv":
        # Export as CSV (simplified)
        import csv
        output_file = output_file or Path.home() / "ph_logs_export.csv"
        
        # This would read actual log files and export to CSV
        # For now, create a sample CSV
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "command", "operation", "status", "duration_ms"])
            writer.writerow([datetime.now().isoformat(), "export", "log_export", "success", "0"])
        
        return output_file
    
    else:
        raise ValueError(f"Unsupported output format: {output_format}")