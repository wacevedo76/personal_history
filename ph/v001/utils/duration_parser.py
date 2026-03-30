"""
Duration Parser Utility for Personal History v0.01
"""

import re
from typing import Union


def parse_duration(duration_str: Union[str, int, float, None]) -> int:
    """
    Parse duration string into minutes.
    
    Supports formats:
    - "90" (minutes)
    - "1h30" or "1hr30" (1 hour 30 minutes)
    - "2h" (2 hours)
    - "45m" (45 minutes)
    - "1.5h" (1.5 hours)
    - "1:30" (1 hour 30 minutes)
    
    Args:
        duration_str: Duration string, number, or None
        
    Returns:
        Duration in minutes
        
    Raises:
        ValueError: If duration cannot be parsed
    """
    if duration_str is None:
        return 0
    
    # If it's already a number, return it
    if isinstance(duration_str, (int, float)):
        return int(duration_str)
    
    # If it's just a number string, assume minutes
    if duration_str.isdigit():
        return int(duration_str)
    
    # Normalize the string
    duration_str = duration_str.strip().lower()
    duration_str = duration_str.replace('hr', 'h').replace('hour', 'h')
    duration_str = duration_str.replace('min', 'm').replace('minutes', 'm')
    
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
        raise ValueError(
            f"Could not parse duration: {duration_str}. "
            f"Use formats like '90', '1h30', '2h', '45m', '1.5h', or '1:30'"
        )


def format_duration(minutes: int, format: str = "auto") -> str:
    """
    Format duration in minutes to human-readable string.
    
    Args:
        minutes: Duration in minutes
        format: Output format:
            - "auto": Choose best format automatically
            - "hours": Always show as hours (e.g., "2.5h")
            - "minutes": Always show as minutes (e.g., "150m")
            - "detailed": Show hours and minutes (e.g., "2h30")
            
    Returns:
        Formatted duration string
    """
    if format == "minutes":
        return f"{minutes}m"
    
    if format == "hours":
        hours = minutes / 60
        return f"{hours:.1f}h"
    
    if format == "detailed" or (format == "auto" and minutes >= 60):
        hours = minutes // 60
        mins = minutes % 60
        
        if mins == 0:
            return f"{hours}h"
        else:
            return f"{hours}h{mins:02d}"
    
    # Default: minutes for short durations
    return f"{minutes}m"


def parse_time_range(start_time: str, end_time: str) -> int:
    """
    Parse time range into minutes.
    
    Args:
        start_time: Start time in HH:MM or HH:MM:SS format
        end_time: End time in HH:MM or HH:MM:SS format
        
    Returns:
        Duration in minutes
    """
    def parse_time(time_str: str) -> int:
        """Parse time string to minutes since midnight"""
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1]) if len(parts) > 1 else 0
        
        return hours * 60 + minutes
    
    start_minutes = parse_time(start_time)
    end_minutes = parse_time(end_time)
    
    # Handle overnight ranges
    if end_minutes < start_minutes:
        end_minutes += 24 * 60
    
    return end_minutes - start_minutes


def validate_duration(duration: int, min_minutes: int = 0, max_minutes: int = 24*60) -> bool:
    """
    Validate duration is within reasonable bounds.
    
    Args:
        duration: Duration in minutes to validate
        min_minutes: Minimum allowed minutes (default: 0)
        max_minutes: Maximum allowed minutes (default: 24 hours)
        
    Returns:
        True if duration is valid
    """
    return min_minutes <= duration <= max_minutes