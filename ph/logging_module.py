"""
Logging Module for Personal History (PH) Command

This module provides comprehensive logging for all PH command operations.
It logs command execution, operations, errors, performance, and user interactions.
"""

import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from functools import wraps
import inspect


class PHLogger:
    """Personal History Logger - Central logging system for PH command"""
    
    def __init__(self, log_dir: Optional[Path] = None, level: str = "INFO"):
        """
        Initialize the PH logger.
        
        Args:
            log_dir: Directory to store log files (default: ~/.personal_history/logs)
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = log_dir or Path.home() / ".personal_history" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging configuration
        self._setup_logging(level)
        
        # Create separate loggers for different components
        self.command_logger = logging.getLogger("ph.command")
        self.operation_logger = logging.getLogger("ph.operation")
        self.error_logger = logging.getLogger("ph.error")
        self.performance_logger = logging.getLogger("ph.performance")
        self.user_logger = logging.getLogger("ph.user")
        
        # Log initialization
        self.command_logger.info("PH Logger initialized")
        self.command_logger.info(f"Log directory: {self.log_dir}")
    
    def _setup_logging(self, level: str):
        """Configure logging handlers and formats"""
        # Main log file
        main_log_file = self.log_dir / f"ph_{datetime.now().strftime('%Y%m')}.log"
        
        # JSON log file for structured logging
        json_log_file = self.log_dir / f"ph_structured_{datetime.now().strftime('%Y%m')}.log"
        
        # Set log level
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                # Console handler (only errors and above)
                logging.StreamHandler(),
                # Main log file handler
                logging.FileHandler(main_log_file, encoding='utf-8'),
                # JSON structured log handler
                self._create_json_handler(json_log_file)
            ]
        )
    
    def _create_json_handler(self, log_file: Path) -> logging.Handler:
        """Create a JSON log handler for structured logging"""
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                    "logger": record.name,
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "module": record.module,
                    "function": record.funcName,
                    "line": record.lineno,
                }
                
                # Add extra fields if present
                if hasattr(record, 'extra'):
                    log_entry.update(record.extra)
                
                # Add exception info if present
                if record.exc_info:
                    log_entry["exception"] = self.formatException(record.exc_info)
                
                return json.dumps(log_entry)
        
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.setFormatter(JSONFormatter())
        return handler
    
    def log_command(self, command: str, arguments: Dict[str, Any], user: Optional[str] = None):
        """Log command execution"""
        extra = {
            "command": command,
            "cmd_args": arguments,  # Changed from 'args' to avoid conflict
            "user": user or "unknown",
            "timestamp": datetime.now().isoformat()
        }
        self.command_logger.info(f"Command executed: {command}", extra=extra)
    
    def log_operation(self, operation: str, details: Dict[str, Any], success: bool = True):
        """Log an operation (add, start, stop, sync, etc.)"""
        level = "INFO" if success else "WARNING"
        extra = {
            "operation": operation,
            "details": details,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        if success:
            self.operation_logger.info(f"Operation: {operation}", extra=extra)
        else:
            self.operation_logger.warning(f"Operation failed: {operation}", extra=extra)
    
    def log_error(self, error_type: str, error_message: str, context: Dict[str, Any] = None):
        """Log an error"""
        extra = {
            "error_type": error_type,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
        self.error_logger.error(f"{error_type}: {error_message}", extra=extra)
    
    def log_performance(self, operation: str, duration_ms: float, details: Dict[str, Any] = None):
        """Log performance metrics"""
        extra = {
            "operation": operation,
            "duration_ms": duration_ms,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        self.performance_logger.info(f"Performance: {operation} took {duration_ms:.2f}ms", extra=extra)
    
    def log_user_interaction(self, interaction_type: str, details: Dict[str, Any]):
        """Log user interactions (prompts, confirmations, etc.)"""
        extra = {
            "interaction_type": interaction_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.user_logger.info(f"User interaction: {interaction_type}", extra=extra)
    
    def get_log_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get a summary of recent logs"""
        # This would read and analyze log files
        # For now, return a placeholder structure
        return {
            "period_days": days,
            "total_commands": 0,  # Would be calculated from logs
            "success_rate": 1.0,  # Would be calculated from logs
            "common_operations": [],  # Would be calculated from logs
            "error_count": 0,  # Would be calculated from logs
            "timestamp": datetime.now().isoformat()
        }


# Decorators for easy logging integration

def log_command_execution(logger: PHLogger):
    """Decorator to log command execution with timing"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract command name from function
            command_name = func.__name__
            
            # Extract arguments
            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            
            # Start timing
            start_time = time.time()
            
            try:
                # Log command start
                logger.log_command(command_name, func_args)
                
                # Execute function
                result = func(*args, **kwargs)
                
                # Log success
                duration_ms = (time.time() - start_time) * 1000
                logger.log_performance(command_name, duration_ms, {"status": "success"})
                
                return result
                
            except Exception as e:
                # Log error
                duration_ms = (time.time() - start_time) * 1000
                logger.log_error(type(e).__name__, str(e), {
                    "command": command_name,
                    "args": func_args,
                    "duration_ms": duration_ms
                })
                logger.log_performance(command_name, duration_ms, {"status": "error"})
                raise
        
        return wrapper
    return decorator


def log_operation(operation_name: str, logger: PHLogger):
    """Decorator to log specific operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                # Execute function
                result = func(*args, **kwargs)
                
                # Log operation success
                duration_ms = (time.time() - start_time) * 1000
                logger.log_operation(operation_name, {
                    "function": func.__name__,
                    "duration_ms": duration_ms,
                    "result_type": type(result).__name__
                }, success=True)
                logger.log_performance(operation_name, duration_ms)
                
                return result
                
            except Exception as e:
                # Log operation failure
                duration_ms = (time.time() - start_time) * 1000
                logger.log_operation(operation_name, {
                    "function": func.__name__,
                    "duration_ms": duration_ms,
                    "error": str(e)
                }, success=False)
                logger.log_performance(operation_name, duration_ms, {"status": "error"})
                raise
        
        return wrapper
    return decorator


class LoggingContext:
    """Context manager for logging operations with timing"""
    
    def __init__(self, operation_name: str, logger: PHLogger, details: Dict[str, Any] = None):
        self.operation_name = operation_name
        self.logger = logger
        self.details = details or {}
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.log_operation(f"START: {self.operation_name}", self.details)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000
        
        if exc_type is None:
            # Operation succeeded
            self.logger.log_operation(f"END: {self.operation_name}", {
                **self.details,
                "duration_ms": duration_ms,
                "status": "success"
            }, success=True)
        else:
            # Operation failed
            self.logger.log_operation(f"END: {self.operation_name}", {
                **self.details,
                "duration_ms": duration_ms,
                "status": "error",
                "error_type": exc_type.__name__,
                "error_message": str(exc_val)
            }, success=False)
            self.logger.log_error(exc_type.__name__, str(exc_val), self.details)
        
        self.logger.log_performance(self.operation_name, duration_ms, {
            "status": "error" if exc_type else "success"
        })


# Global logger instance (singleton pattern)
_global_logger = None

def get_logger(log_dir: Optional[Path] = None, level: str = "INFO") -> PHLogger:
    """Get or create the global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = PHLogger(log_dir, level)
    return _global_logger


def setup_logging(log_dir: Optional[Path] = None, level: str = "INFO") -> PHLogger:
    """Set up logging and return the logger instance"""
    return get_logger(log_dir, level)