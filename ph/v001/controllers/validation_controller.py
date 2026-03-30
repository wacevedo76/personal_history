"""
Validation Controller for Personal History v0.01
"""

import json
from pathlib import Path
from typing import Dict, List
from ..models.file import PersonalHistoryFile
from ..schema import validate_ph_file


class ValidationController:
    """Controller for validation operations"""
    
    def validate_file(self, filepath: Path) -> Dict:
        """Validate Personal History file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Validate against schema
            validate_ph_file(data)
            
            # Load and verify file structure
            ph_file = PersonalHistoryFile.from_dict(data)
            
            return {
                "valid": True,
                "file": str(filepath),
                "version": data.get("version"),
                "signature_present": "signature" in data,
                "signature_valid": ph_file.verify_signature() if ph_file.signature else None,
                "file_integrity": ph_file.verify(),
                "total_days": len(data.get("timeline", [])),
                "total_activities": sum(
                    len(day.get("activities", []))
                    for day in data.get("timeline", [])
                )
            }
            
        except Exception as e:
            return {
                "valid": False,
                "file": str(filepath),
                "error": str(e)
            }
    
    def validate_activity(self, activity_data: Dict) -> Dict:
        """Validate activity data"""
        required_fields = ["type", "duration", "timestamp", "hash"]
        optional_fields = ["data", "shareable"]
        
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required fields
        for field in required_fields:
            if field not in activity_data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")
        
        # Check timestamp structure
        if "timestamp" in activity_data:
            timestamp = activity_data["timestamp"]
            if not isinstance(timestamp, dict) or "commitment" not in timestamp:
                result["valid"] = False
                result["errors"].append("Invalid timestamp structure")
        
        # Check data types
        if "duration" in activity_data and not isinstance(activity_data["duration"], int):
            result["valid"] = False
            result["errors"].append("Duration must be an integer")
        
        if "shareable" in activity_data and not isinstance(activity_data["shareable"], bool):
            result["warnings"].append("Shareable should be a boolean")
        
        return result
    
    def validate_day(self, day_data: Dict) -> Dict:
        """Validate day data"""
        required_fields = ["date", "timestamp", "activities", "hash"]
        
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required fields
        for field in required_fields:
            if field not in day_data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")
        
        # Check date format (simple check)
        if "date" in day_data:
            date_str = day_data["date"]
            if len(date_str) != 10 or date_str[4] != "-" or date_str[7] != "-":
                result["warnings"].append(f"Date format may be invalid: {date_str}")
        
        # Validate activities
        if "activities" in day_data:
            activities = day_data["activities"]
            if not isinstance(activities, list):
                result["valid"] = False
                result["errors"].append("Activities must be a list")
            else:
                for i, activity_data in enumerate(activities):
                    activity_result = self.validate_activity(activity_data)
                    if not activity_result["valid"]:
                        result["valid"] = False
                        result["errors"].append(f"Activity {i}: {', '.join(activity_result['errors'])}")
        
        return result
    
    def batch_validate_files(self, filepaths: List[Path]) -> Dict:
        """Validate multiple files"""
        results = []
        valid_count = 0
        
        for filepath in filepaths:
            result = self.validate_file(filepath)
            results.append(result)
            if result["valid"]:
                valid_count += 1
        
        return {
            "total_files": len(filepaths),
            "valid_files": valid_count,
            "invalid_files": len(filepaths) - valid_count,
            "results": results
        }
    
    def generate_validation_report(self, validation_result: Dict) -> str:
        """Generate human-readable validation report"""
        if validation_result["valid"]:
            report = f"✅ {validation_result['file']} is valid\n"
            report += f"   Version: {validation_result.get('version', 'unknown')}\n"
            report += f"   Days: {validation_result.get('total_days', 0)}\n"
            report += f"   Activities: {validation_result.get('total_activities', 0)}\n"
            
            if validation_result.get('signature_present'):
                if validation_result.get('signature_valid'):
                    report += "   Signature: ✅ valid\n"
                else:
                    report += "   Signature: ❌ invalid\n"
            else:
                report += "   Signature: ⚠️  not present\n"
            
            if validation_result.get('file_integrity'):
                report += "   Integrity: ✅ verified\n"
            else:
                report += "   Integrity: ❌ failed\n"
        
        else:
            report = f"❌ {validation_result['file']} is invalid\n"
            report += f"   Error: {validation_result.get('error', 'Unknown error')}\n"
        
        return report