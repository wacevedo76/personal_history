#!/usr/bin/env python3
"""
Test script for PH Command Logging Module

This script demonstrates how the logging module works and tests its functionality.
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Add the project to the path
sys.path.insert(0, str(Path(__file__).parent))

from ph.logging_module import PHLogger, log_command_execution, log_operation, LoggingContext
from ph.logging_integration import LoggingHistoryController, LoggingCLIView


def test_basic_logging():
    """Test basic logging functionality"""
    print("Testing basic logging functionality...")
    
    # Create a temporary directory for logs
    temp_dir = Path(tempfile.mkdtemp())
    print(f"Using temp directory: {temp_dir}")
    
    # Create logger
    logger = PHLogger(temp_dir, level="DEBUG")
    
    # Test different log types
    logger.log_command("test_command", {"arg1": "value1", "arg2": 123}, user="test_user")
    logger.log_operation("test_operation", {"details": "operation details"}, success=True)
    logger.log_operation("failed_operation", {"details": "something went wrong"}, success=False)
    logger.log_error("TestError", "This is a test error", {"context": "test_context"})
    logger.log_performance("test_performance", 123.45, {"iterations": 100})
    logger.log_user_interaction("prompt", {"question": "Continue?", "response": "yes"})
    
    # Test decorators
    @log_command_execution(logger)
    def test_function(arg1, arg2):
        """Test function for decorator"""
        logger.log_operation("inside_function", {"arg1": arg1, "arg2": arg2})
        return arg1 + arg2
    
    result = test_function(10, 20)
    print(f"Test function result: {result}")
    
    # Test context manager
    with LoggingContext("test_context_operation", logger, {"param": "value"}):
        logger.log_operation("inside_context", {"step": "processing"})
        # Simulate work
        import time
        time.sleep(0.1)
    
    # Get log summary
    summary = logger.get_log_summary()
    print(f"\nLog summary: {summary}")
    
    # Clean up
    shutil.rmtree(temp_dir)
    print("✓ Basic logging tests passed")


def test_integration():
    """Test integration with PH components"""
    print("\nTesting integration with PH components...")
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    
    # Mock controller for testing
    class MockController:
        def __init__(self):
            self.data_dir = temp_dir
        
        def create_identity(self, name=None):
            class MockIdentity:
                def __init__(self):
                    self.identity_hash = "test_hash_1234567890"
                    self.name = name or "anonymous"
            return MockIdentity()
        
        def save_identity(self, identity):
            pass
        
        def create_activity(self, activity_type, data, duration, shareable=True):
            class MockActivity:
                def __init__(self):
                    self.type = activity_type
                    self.id = "activity_1234567890"
            return MockActivity()
        
        def add_to_pending(self, activity, date=None):
            pass
        
        def sync_to_file(self):
            class MockFile:
                def __init__(self):
                    self.timeline = ["day1", "day2"]
                
                def get_activity_count(self):
                    return 5
            return MockFile()
    
    # Create logger
    logger = PHLogger(temp_dir, level="INFO")
    
    # Create logging controller
    mock_controller = MockController()
    logging_controller = LoggingHistoryController(mock_controller, logger)
    
    # Test controller methods
    identity = logging_controller.create_identity("Test User")
    print(f"Created identity: {identity.name}")
    
    logging_controller.save_identity(identity)
    print("Saved identity")
    
    activity = logging_controller.create_activity("work", {"project": "test"}, 60)
    print(f"Created activity: {activity.type}")
    
    logging_controller.add_to_pending(activity, "2024-01-01")
    print("Added activity to pending")
    
    result = logging_controller.sync_to_file()
    print(f"Synced file with {len(result.timeline)} days")
    
    # Clean up
    shutil.rmtree(temp_dir)
    print("✓ Integration tests passed")


def test_cli_integration():
    """Test CLI integration"""
    print("\nTesting CLI integration...")
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    
    # Mock CLI view for testing
    class MockCLIView:
        def run(self, args=None):
            print(f"Mock CLI run with args: {args}")
            return "success"
        
        def _execute_command(self, args):
            print(f"Mock execute command: {args.command}")
            return "executed"
        
        def _handle_init(self, args):
            print(f"Mock handle init: {args.name}")
            return "init handled"
    
    # Create logger
    logger = PHLogger(temp_dir, level="INFO")
    
    # Create logging CLI view
    mock_view = MockCLIView()
    logging_view = LoggingCLIView(mock_view, logger)
    
    # Test CLI methods
    result = logging_view.run(["init", "--name", "Test"])
    print(f"CLI run result: {result}")
    
    # Clean up
    shutil.rmtree(temp_dir)
    print("✓ CLI integration tests passed")


def demonstrate_log_analysis():
    """Demonstrate log analysis capabilities"""
    print("\nDemonstrating log analysis...")
    
    from ph.logging_integration import analyze_logs, export_logs
    
    # Analyze logs
    analysis = analyze_logs(7)
    print(f"Log analysis (7 days):")
    print(f"  Total commands: {analysis['summary'].get('total_commands', 'N/A')}")
    print(f"  Error count: {analysis['summary'].get('error_count', 'N/A')}")
    print(f"  Success rate: {analysis['summary'].get('success_rate', 'N/A'):.1%}")
    
    # Show recommendations
    if analysis['recommendations']:
        print("\nRecommendations:")
        for rec in analysis['recommendations']:
            print(f"  • {rec}")
    
    # Show insights
    if analysis['insights']:
        print("\nInsights:")
        for insight in analysis['insights']:
            print(f"  • {insight}")
    
    print("✓ Log analysis demonstration complete")


def main():
    """Run all tests"""
    print("=" * 60)
    print("PH Command Logging Module Test Suite")
    print("=" * 60)
    
    try:
        test_basic_logging()
        test_integration()
        test_cli_integration()
        demonstrate_log_analysis()
        
        print("\n" + "=" * 60)
        print("All tests passed successfully! 🎉")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())