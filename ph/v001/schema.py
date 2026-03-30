"""
JSON Schema validation for Personal History Format v0.01.
Complements the core.py implementation.
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass


class PHValidationError(ValueError):
    """Raised when PH file validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        self.message = message
        super().__init__(f"{field + ': ' if field else ''}{message}")


@dataclass
class ValidationResult:
    """Result of PH file validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]


class PHSchemaValidator:
    """Validator for Personal History Format v0.01."""
    
    # Constants from specification
    VERSION = "0.01.0"
    HASH_PATTERN = re.compile(r"^[a-f0-9]{64}$")
    SIGNATURE_PATTERN = re.compile(r"^[a-f0-9]{128}$")
    DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    
    # Allowed activity types from v0.01 spec
    ALLOWED_ACTIVITY_TYPES = {
        "family", "planning", "learning", "work", "health", "social"
    }
    
    def validate(self, ph_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate a Personal History file.
        
        Args:
            ph_data: Dictionary containing PH file data
            
        Returns:
            ValidationResult with validation status and messages
        """
        errors = []
        warnings = []
        
        try:
            # Check required top-level fields
            self._validate_required_fields(ph_data, errors)
            
            if errors:
                return ValidationResult(valid=False, errors=errors, warnings=warnings)
            
            # Validate individual fields
            self._validate_version(ph_data["version"], errors)
            self._validate_identity(ph_data["identity"], errors)
            self._validate_timeline(ph_data["timeline"], errors, warnings)
            self._validate_signature(ph_data["signature"], errors)
            
        except (KeyError, TypeError) as e:
            errors.append(f"Invalid data structure: {e}")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_required_fields(self, ph_data: Dict[str, Any], errors: List[str]):
        """Validate that all required fields are present."""
        required_fields = ["version", "identity", "timeline", "signature"]
        
        for field in required_fields:
            if field not in ph_data:
                errors.append(f"Missing required field: '{field}'")
    
    def _validate_version(self, version: str, errors: List[str]):
        """Validate version field."""
        if version != self.VERSION:
            errors.append(
                f"Invalid version: expected '{self.VERSION}', got '{version}'"
            )
    
    def _validate_identity(self, identity: Dict[str, Any], errors: List[str]):
        """Validate identity field."""
        if "hash" not in identity:
            errors.append("Identity missing required 'hash' field")
            return
        
        hash_value = identity["hash"]
        if not self.HASH_PATTERN.match(hash_value):
            errors.append(
                f"Invalid identity hash: must be 64 hex characters, got '{hash_value[:20]}...'"
            )
        
        # Name is optional, but if present should be a string
        if "name" in identity and not isinstance(identity["name"], str):
            errors.append("Identity 'name' must be a string")
    
    def _validate_timeline(self, timeline: List[Dict[str, Any]], 
                          errors: List[str], warnings: List[str]):
        """Validate timeline array."""
        if not isinstance(timeline, list):
            errors.append("Timeline must be an array")
            return
        
        seen_dates = set()
        previous_date = None
        
        for i, day in enumerate(timeline):
            day_errors = self._validate_day(day, i)
            errors.extend(day_errors)
            
            # Check for duplicate dates
            date = day.get("date")
            if date:
                if date in seen_dates:
                    errors.append(f"Duplicate date in timeline: {date}")
                seen_dates.add(date)
                
                # Check chronological order
                if previous_date and date < previous_date:
                    warnings.append(
                        f"Timeline not in chronological order: {date} comes after {previous_date}"
                    )
                previous_date = date
        
        # Check for gaps in timeline (warning only)
        if len(timeline) > 1:
            self._check_timeline_gaps(timeline, warnings)
    
    def _validate_day(self, day: Dict[str, Any], day_index: int) -> List[str]:
        """Validate a single day in the timeline."""
        errors = []
        
        # Required fields
        required_fields = ["date", "activities", "hash"]
        for field in required_fields:
            if field not in day:
                errors.append(f"Day {day_index}: missing required field '{field}'")
        
        if errors:
            return errors
        
        # Validate date format
        date = day["date"]
        if not self.DATE_PATTERN.match(date):
            errors.append(f"Day {day_index}: invalid date format '{date}', expected YYYY-MM-DD")
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                errors.append(f"Day {day_index}: invalid date '{date}'")
        
        # Validate hash
        day_hash = day["hash"]
        if not self.HASH_PATTERN.match(day_hash):
            errors.append(
                f"Day {day_index}: invalid day hash, must be 64 hex characters"
            )
        
        # Validate activities
        activities = day["activities"]
        if not isinstance(activities, list):
            errors.append(f"Day {day_index}: 'activities' must be an array")
        else:
            for j, activity in enumerate(activities):
                activity_errors = self._validate_activity(activity, day_index, j)
                errors.extend(activity_errors)
        
        # Validate timestamp commitment (optional)
        if "timestamp" in day:
            timestamp_errors = self._validate_timestamp(day["timestamp"], day_index)
            errors.extend(timestamp_errors)
        
        # Validate note (optional)
        if "note" in day and not isinstance(day["note"], str):
            errors.append(f"Day {day_index}: 'note' must be a string")
        
        return errors
    
    def _validate_activity(self, activity: Dict[str, Any], 
                          day_index: int, activity_index: int) -> List[str]:
        """Validate a single activity."""
        errors = []
        
        # Required fields
        required_fields = ["type", "data", "duration", "hash"]
        for field in required_fields:
            if field not in activity:
                errors.append(
                    f"Day {day_index}, activity {activity_index}: missing required field '{field}'"
                )
        
        if errors:
            return errors
        
        # Validate type
        activity_type = activity["type"]
        if activity_type not in self.ALLOWED_ACTIVITY_TYPES:
            errors.append(
                f"Day {day_index}, activity {activity_index}: "
                f"invalid activity type '{activity_type}', "
                f"must be one of {sorted(self.ALLOWED_ACTIVITY_TYPES)}"
            )
        
        # Validate data (must be an object/dict)
        data = activity["data"]
        if not isinstance(data, dict):
            errors.append(
                f"Day {day_index}, activity {activity_index}: 'data' must be an object"
            )
        
        # Validate duration (must be positive number)
        duration = activity["duration"]
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(
                f"Day {day_index}, activity {activity_index}: "
                f"'duration' must be a positive number, got {duration}"
            )
        
        # Validate hash
        activity_hash = activity["hash"]
        if not self.HASH_PATTERN.match(activity_hash):
            errors.append(
                f"Day {day_index}, activity {activity_index}: "
                "invalid activity hash, must be 64 hex characters"
            )
        
        # Validate shareable flag (optional, defaults to True)
        if "shareable" in activity and not isinstance(activity["shareable"], bool):
            errors.append(
                f"Day {day_index}, activity {activity_index}: 'shareable' must be boolean"
            )
        
        return errors
    
    def _validate_timestamp(self, timestamp: Dict[str, Any], day_index: int) -> List[str]:
        """Validate timestamp commitment."""
        errors = []
        
        if "commitment" not in timestamp:
            errors.append(f"Day {day_index}: timestamp missing 'commitment' field")
            return errors
        
        commitment = timestamp["commitment"]
        if not self.HASH_PATTERN.match(commitment):
            errors.append(
                f"Day {day_index}: invalid timestamp commitment, "
                "must be 64 hex characters"
            )
        
        return errors
    
    def _validate_signature(self, signature: str, errors: List[str]):
        """Validate signature field."""
        if not self.SIGNATURE_PATTERN.match(signature):
            errors.append(
                f"Invalid signature: must be 128 hex characters, got '{signature[:20]}...'"
            )
    
    def _check_timeline_gaps(self, timeline: List[Dict[str, Any]], warnings: List[str]):
        """Check for gaps in the timeline (warning only)."""
        try:
            dates = [datetime.strptime(day["date"], "%Y-%m-%d") for day in timeline]
            dates.sort()
            
            for i in range(1, len(dates)):
                days_diff = (dates[i] - dates[i-1]).days
                if days_diff > 1:
                    warnings.append(
                        f"Gap in timeline: {dates[i-1].date()} to {dates[i].date()} "
                        f"({days_diff - 1} missing days)"
                    )
        except (KeyError, ValueError):
            # If dates are invalid, this will be caught by other validators
            pass


# Convenience functions
def validate_ph_file(ph_data: Dict[str, Any]) -> bool:
    """
    Validate a Personal History file.
    
    Args:
        ph_data: Dictionary containing PH file data
        
    Returns:
        True if valid, raises PHValidationError if invalid
    """
    validator = PHSchemaValidator()
    result = validator.validate(ph_data)
    
    if not result.valid:
        # Join all error messages
        error_msg = "\n".join(result.errors)
        raise PHValidationError(error_msg)
    
    return True


def validate_ph_file_with_warnings(ph_data: Dict[str, Any]) -> ValidationResult:
    """
    Validate a Personal History file with warnings.
    
    Args:
        ph_data: Dictionary containing PH file data
        
    Returns:
        ValidationResult with validation status, errors, and warnings
    """
    validator = PHSchemaValidator()
    return validator.validate(ph_data)