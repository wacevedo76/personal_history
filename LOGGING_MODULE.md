# PH Command Logging Module

## Overview

This logging module provides comprehensive logging for all Personal History (PH) command operations. It logs command execution, operations, errors, performance metrics, and user interactions.

## Features

### 1. **Multi-level Logging**
- **Command logging**: Which commands are executed with what arguments
- **Operation logging**: What the command actually does (adds activity, starts timer, etc.)
- **Error logging**: Exceptions and failures with full context
- **Performance logging**: How long operations take
- **User interaction logging**: Prompts, confirmations, and user responses

### 2. **Multiple Output Formats**
- **Human-readable logs**: Easy to read console and file output
- **Structured JSON logs**: Machine-readable for analysis and monitoring
- **Separate log files**: Organized by component and time period

### 3. **Easy Integration**
- **Decorators**: Simple `@log_command_execution` and `@log_operation` decorators
- **Context managers**: `LoggingContext` for timing and logging blocks of code
- **Wrapper classes**: Pre-built wrappers for existing controllers and views

## Installation

The logging module is part of the PH command system. No additional installation is required.

## Quick Start

### Basic Usage

```python
from ph.logging_module import get_logger

# Get the global logger
logger = get_logger()

# Log a command
logger.log_command("add", {"type": "work", "duration": "60"}, user="william")

# Log an operation
logger.log_operation("activity_created", {
    "type": "work", 
    "duration": 60,
    "shareable": True
}, success=True)

# Log an error
logger.log_error("ValidationError", "Invalid duration format", {
    "input": "1 hour",
    "expected_format": "minutes or HH:MM"
})
```

### Using Decorators

```python
from ph.logging_module import log_command_execution, log_operation

@log_command_execution(get_logger())
def handle_add_command(args):
    """Handle add command with automatic logging"""
    # Your command logic here
    pass

@log_operation("create_activity", get_logger())
def create_activity(activity_type, data, duration):
    """Create activity with automatic logging"""
    # Your activity creation logic here
    pass
```

### Using Context Managers

```python
from ph.logging_module import LoggingContext

with LoggingContext("sync_operations", logger, {"file": "history.ph.json"}):
    # All operations in this block are logged and timed
    load_data()
    process_activities()
    save_to_file()
```

## Integration with Existing PH Command

### Option 1: Use Wrapper Classes (Recommended)

```python
from ph.logging_integration import create_logging_integrated_cli

# Create a fully logged CLI
cli = create_logging_integrated_cli()
cli.run()
```

### Option 2: Patch Existing CLI

```python
from ph.logging_integration import patch_existing_cli
from ph.v001.views.cli_view import CLIView, main

# Patch the existing CLIView class
patch_existing_cli()

# Now all CLI operations are logged
main()
```

### Option 3: Create Custom Entry Point

```python
from ph.logging_integration import LoggingCLIEntryPoint

if __name__ == "__main__":
    LoggingCLIEntryPoint.main()
```

## Configuration

### Log Directory
By default, logs are stored in `~/.personal_history/logs/`. You can customize this:

```python
from pathlib import Path
from ph.logging_module import setup_logging

# Custom log directory
log_dir = Path("/var/log/personal_history")
logger = setup_logging(log_dir=log_dir, level="INFO")
```

### Log Levels
- `DEBUG`: Detailed information, typically useful only for debugging
- `INFO`: Confirmation that things are working as expected
- `WARNING`: Something unexpected happened, but the software is still working
- `ERROR`: A more serious problem, some function failed
- `CRITICAL`: A serious error, the program itself may be unable to continue

```python
# Set log level
logger = get_logger(level="DEBUG")  # Most verbose
logger = get_logger(level="INFO")   # Default
logger = get_logger(level="ERROR")  # Only errors
```

## Log Files Structure

```
~/.personal_history/logs/
├── ph_202403.log              # Human-readable logs (monthly rotation)
├── ph_structured_202403.log   # JSON structured logs (monthly rotation)
└── ph_202404.log              # Next month's logs
```

### JSON Log Format Example

```json
{
  "timestamp": "2024-03-31T07:17:00.123456",
  "logger": "ph.command",
  "level": "INFO",
  "message": "Command executed: add",
  "module": "cli_view",
  "function": "_handle_add",
  "line": 123,
  "command": "add",
  "args": {"type": "work", "duration": "60"},
  "user": "william"
}
```

## Log Analysis

### Get Log Summary

```python
from ph.logging_integration import analyze_logs

# Analyze last 7 days of logs
analysis = analyze_logs(7)
print(f"Total commands: {analysis['summary']['total_commands']}")
print(f"Success rate: {analysis['summary']['success_rate']:.1%}")
```

### Export Logs

```python
from ph.logging_integration import export_logs
from pathlib import Path

# Export as JSON
json_data = export_logs("json")
print(json_data)

# Export as CSV
csv_file = export_logs("csv", Path.home() / "ph_logs.csv")
print(f"Exported to: {csv_file}")
```

## Testing

Run the test suite to verify the logging module works correctly:

```bash
cd /home/openclaw/.openclaw/workspace/personal_history
python test_logging.py
```

## Best Practices

### 1. **Log Meaningful Context**
```python
# Good: Log with context
logger.log_operation("activity_added", {
    "type": activity.type,
    "duration": activity.duration,
    "date": date,
    "user": get_current_user()
})

# Bad: Log without context
logger.log_operation("activity_added", {})
```

### 2. **Use Appropriate Log Levels**
- Use `DEBUG` for development and troubleshooting
- Use `INFO` for normal operations
- Use `WARNING` for recoverable issues
- Use `ERROR` for failures that need attention
- Use `CRITICAL` for system-level failures

### 3. **Don't Log Sensitive Information**
```python
# Good: Log metadata, not sensitive data
logger.log_command("login", {"username": "william", "success": True})

# Bad: Log sensitive data
logger.log_command("login", {"username": "william", "password": "secret123"})
```

### 4. **Use Structured Logging for Analysis**
Always use the `extra` parameter for structured data that can be analyzed later.

## Troubleshooting

### Logs Not Appearing
1. Check log level: `DEBUG` shows more than `INFO`
2. Check log directory permissions
3. Verify the logger is initialized before use

### Performance Issues
1. Use `level="INFO"` or higher in production
2. Consider async logging for high-volume applications
3. Regularly rotate and archive old log files

### JSON Logs Not Parsing
1. Ensure each log entry is a valid JSON object on one line
2. Check for encoding issues (UTF-8 is default)
3. Verify the JSON formatter is properly configured

## Advanced Usage

### Custom Log Handlers
```python
import logging
from ph.logging_module import PHLogger

class CustomHandler(logging.Handler):
    def emit(self, record):
        # Custom handling logic
        pass

logger = PHLogger()
logger.addHandler(CustomHandler())
```

### Log Filtering
```python
import logging

class CommandFilter(logging.Filter):
    def filter(self, record):
        # Only log commands from specific users
        return hasattr(record, 'user') and record.user == 'william'

logger = get_logger()
logger.addFilter(CommandFilter())
```

### Integration with Monitoring Systems
The JSON structured logs can be easily ingested by:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **Datadog**
- **Prometheus** (with appropriate exporters)

## Support

For issues or questions:
1. Check the log files for error details
2. Review the test suite for usage examples
3. Consult the PH command documentation

---

*Last updated: March 31, 2026*