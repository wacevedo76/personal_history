"""
Activity Model for Personal History v0.01
"""

import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional


class Activity:
    """Represents a Personal History activity"""
    
    def __init__(
        self,
        activity_type: str,
        data: Dict,
        duration: int,
        exact_start: Optional[str] = None,
        exact_end: Optional[str] = None,
        shareable: bool = True
    ):
        self.type = activity_type
        self.data = data
        self.duration = duration
        self.shareable = shareable
        
        # Set default times if not provided
        if exact_start is None:
            exact_start = datetime.now().isoformat() + "Z"
        
        if exact_end is None:
            end_time = datetime.fromisoformat(exact_start.replace('Z', '+00:00'))
            end_time = end_time + timedelta(minutes=duration)
            exact_end = end_time.isoformat() + "Z"
        
        self.exact_start = exact_start
        self.exact_end = exact_end
        
        # Generate commitment and hash
        self._generate_commitment()
        self._calculate_hash()
    
    def _generate_commitment(self):
        """Generate timestamp commitment hiding exact times"""
        nonce = secrets.token_hex(32)  # 32 bytes = 64 hex chars
        commitment_input = self.exact_start + self.exact_end + nonce
        commitment = hashlib.sha256(commitment_input.encode()).hexdigest()
        
        self.commitment = commitment
        self._private_nonce = nonce
    
    def _calculate_hash(self):
        """Calculate activity hash"""
        data_str = json.dumps(self.data, sort_keys=True)
        hash_input = f"{self.type}{data_str}{self.duration}{self.exact_start}{self.exact_end}"
        
        if not self.shareable:
            hash_input += "private"
        
        self.hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    def to_dict(self, include_private: bool = False) -> Dict:
        """Convert to dictionary for JSON serialization"""
        result = {
            "type": self.type,
            "data": self.data,
            "duration": self.duration,
            "timestamp": {
                "commitment": self.commitment
            },
            "shareable": self.shareable,
            "hash": self.hash
        }
        
        if include_private:
            result["_private"] = {
                "nonce": self._private_nonce,
                "exact_start": self.exact_start,
                "exact_end": self.exact_end
            }
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Activity':
        """Create Activity from dictionary"""
        # Extract private data if available
        private_data = data.get("_private", {})
        exact_start = private_data.get("exact_start")
        exact_end = private_data.get("exact_end")
        
        # Create activity
        activity = cls(
            activity_type=data["type"],
            data=data.get("data", {}),
            duration=data.get("duration", 0),
            exact_start=exact_start,
            exact_end=exact_end,
            shareable=data.get("shareable", True)
        )
        
        # Override calculated values with stored ones
        activity.commitment = data.get("timestamp", {}).get("commitment", "")
        activity.hash = data.get("hash", "")
        
        if "_private" in data:
            activity._private_nonce = data["_private"].get("nonce", "")
        
        return activity
    
    def verify(self) -> bool:
        """Verify activity integrity"""
        # Recalculate commitment
        commitment_input = self.exact_start + self.exact_end + self._private_nonce
        calculated_commitment = hashlib.sha256(commitment_input.encode()).hexdigest()
        
        if calculated_commitment != self.commitment:
            return False
        
        # Recalculate hash
        data_str = json.dumps(self.data, sort_keys=True)
        hash_input = f"{self.type}{data_str}{self.duration}{self.exact_start}{self.exact_end}"
        
        if not self.shareable:
            hash_input += "private"
        
        calculated_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        return calculated_hash == self.hash
    
    def get_shareable_version(self) -> Dict:
        """Get shareable version (without private data)"""
        return {
            "type": self.type,
            "data": self.data,
            "duration": self.duration,
            "timestamp": {
                "commitment": self.commitment
            },
            "shareable": self.shareable,
            "hash": self.hash
        }