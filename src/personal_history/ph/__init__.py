"""
Personal History Package

Main package entry point. Exports v001 as the primary implementation.
"""

# Import v001 as the main implementation
from .v001 import *

# Version information
__version__ = "0.01.0"
__author__ = "William Acevedo"

# Re-export useful utilities
from .logging_module import PHLogger, get_logger, log_command_execution, log_operation