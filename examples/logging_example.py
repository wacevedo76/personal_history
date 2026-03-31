#!/usr/bin/env python3
"""
Example: Using the Personal History Logging Module

This script demonstrates how to use the logging module in different ways.
"""

import sys
from pathlib import Path

# Add the project to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ph.logging_module import get_logger, log_command_execution, log_operation, LoggingContext


def example_basic_logging():
    """Example 1: Basic logging usage"""
    print("=" * 60)
    print("Example 1: Basic Logging Usage")
    print("=" * 60)
    
    # Get the logger
    logger = get_logger(level="INFO")
    
    # Log different types of events
    logger.log_command("test_command", {"arg1": "value1", "arg2": 123}, user="example_user")
    logger.log_operation("data_processing", {"records": 100, "source": "database"}, success=True)
    logger.log_error("ConnectionError", "Failed to connect to database", {"host": "localhost", "port": 5432})
    logger.log_performance("api_call", 245.67, {"endpoint": "/users", "method": "GET"})
    logger.log_user_interaction("confirmation", {"question": "Delete file?", "response": "yes"})
    
    print("✓ Basic logging examples completed")
    print("Check ~/.personal_history/logs/ for log files")


def example_decorators():
    """Example 2: Using decorators"""
    print("\n" + "=" * 60)
    print("Example 2: Using Decorators")
    print("=" * 60)
    
    logger = get_logger()
    
    @log_command_execution(logger)
    def process_data(data_size, algorithm="default"):
        """Example function with command logging"""
        logger.log_operation("data_processing", {"size": data_size, "algorithm": algorithm})
        # Simulate work
        import time
        time.sleep(0.1)
        return f"Processed {data_size} records"
    
    @log_operation("complex_calculation", logger)
    def calculate_statistics(numbers):
        """Example function with operation logging"""
        total = sum(numbers)
        average = total / len(numbers) if numbers else 0
        return {"total": total, "average": average}
    
    # Use the decorated functions
    result1 = process_data(1000, "fast")
    print(f"Process data result: {result1}")
    
    result2 = calculate_statistics([1, 2, 3, 4, 5])
    print(f"Statistics result: {result2}")
    
    print("✓ Decorator examples completed")


def example_context_manager():
    """Example 3: Using context manager"""
    print("\n" + "=" * 60)
    print("Example 3: Using Context Manager")
    print("=" * 60)
    
    logger = get_logger()
    
    # Use context manager for timing and logging
    with LoggingContext("database_operations", logger, {"database": "users_db"}):
        logger.log_operation("connect", {"host": "localhost"})
        
        # Simulate database operations
        import time
        time.sleep(0.05)
        
        logger.log_operation("query", {"table": "users", "condition": "active=true"})
        time.sleep(0.1)
        
        logger.log_operation("disconnect", {})
    
    print("✓ Context manager example completed")


def example_integration():
    """Example 4: Integration with PH components"""
    print("\n" + "=" * 60)
    print("Example 4: Integration with PH Components")
    print("=" * 60)
    
    try:
        from ph.logging_integration import create_logging_integrated_cli
        
        print("Creating logging-integrated CLI...")
        cli = create_logging_integrated_cli()
        print("✓ Logging-integrated CLI created")
        print("Use: cli.run() to run with logging")
        
    except ImportError as e:
        print(f"Note: Could not import integration module: {e}")
        print("Make sure you're in the project directory")


def example_log_analysis():
    """Example 5: Log analysis"""
    print("\n" + "=" * 60)
    print("Example 5: Log Analysis")
    print("=" * 60)
    
    try:
        from ph.logging_integration import analyze_logs, export_logs
        
        # Analyze recent logs
        analysis = analyze_logs(1)  # Last 1 day
        print(f"Log analysis for last day:")
        print(f"  Total commands: {analysis['summary'].get('total_commands', 'N/A')}")
        print(f"  Error count: {analysis['summary'].get('error_count', 'N/A')}")
        
        # Export logs
        print("\nExporting logs...")
        summary = export_logs("json")
        print(f"✓ Log summary exported (JSON format)")
        
        if analysis['recommendations']:
            print("\nRecommendations:")
            for rec in analysis['recommendations']:
                print(f"  • {rec}")
        
    except ImportError as e:
        print(f"Note: Could not import analysis module: {e}")


def main():
    """Run all examples"""
    print("Personal History Logging Module - Examples")
    print("=" * 60)
    
    try:
        example_basic_logging()
        example_decorators()
        example_context_manager()
        example_integration()
        example_log_analysis()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Check ~/.personal_history/logs/ for generated log files")
        print("2. Read LOGGING_MODULE.md for detailed documentation")
        print("3. Read IMPLEMENTATION_GUIDE.md for integration guide")
        print("4. Run test_logging.py for comprehensive tests")
        
    except Exception as e:
        print(f"\n❌ Error in example: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())