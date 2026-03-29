"""
Personal History Format v0.01 - Core Implementation
"""

import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import base64

# Try to import cryptography libraries
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Warning: cryptography library not available. Install with: pip install cryptography")
    print("Using simulated cryptography for demonstration.")

class PersonalHistoryV001:
    """Core implementation of Personal History Format v0.01"""
    
    VERSION = "0.01.0"
    
    @staticmethod
    def hash_data(data: str) -> str:
        """SHA-256 hash helper"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def hash_bytes(data: bytes) -> str:
        """SHA-256 hash for bytes"""
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def create_timestamp_commitment(exact_start: str, exact_end: str) -> Dict:
        """
        Create a timestamp commitment hiding exact times
        
        Args:
            exact_start: ISO 8601 timestamp with milliseconds
            exact_end: ISO 8601 timestamp with milliseconds
            
        Returns:
            Dictionary with commitment and private data
        """
        nonce = secrets.token_hex(32)  # 32 bytes = 64 hex chars
        commitment_input = exact_start + exact_end + nonce
        commitment = PersonalHistoryV001.hash_data(commitment_input)
        
        return {
            "commitment": commitment,
            "_private": {
                "nonce": nonce,
                "exact_start": exact_start,
                "exact_end": exact_end
            }
        }
    
    @staticmethod
    def create_activity(
        activity_type: str,
        data: Dict,
        duration: int,
        exact_start: Optional[str] = None,
        exact_end: Optional[str] = None,
        shareable: bool = True
    ) -> Dict:
        """
        Create an activity with hidden exact times
        
        Args:
            activity_type: Type of activity (work, family, exercise, etc.)
            data: Activity-specific data
            duration: Duration in minutes
            exact_start: Optional exact start time (ISO 8601)
            exact_end: Optional exact end time (ISO 8601)
            shareable: Whether activity can be shared publicly
            
        Returns:
            Activity dictionary with hidden exact times
        """
        # Set default times if not provided
        if exact_start is None:
            exact_start = datetime.now().isoformat() + "Z"
        
        if exact_end is None:
            end_time = datetime.fromisoformat(exact_start.replace('Z', '+00:00'))
            end_time = end_time + timedelta(minutes=duration)
            exact_end = end_time.isoformat() + "Z"
        
        # Create timestamp commitment (hides exact times)
        commitment_data = PersonalHistoryV001.create_timestamp_commitment(
            exact_start, exact_end
        )
        
        # Create activity hash (includes exact times)
        data_str = json.dumps(data, sort_keys=True)
        hash_input = (
            activity_type +
            data_str +
            str(duration) +
            exact_start +
            exact_end +
            commitment_data["commitment"]
        )
        activity_hash = PersonalHistoryV001.hash_data(hash_input)
        
        # Build activity (public view)
        activity = {
            "type": activity_type,
            "data": data,
            "duration": duration,
            "timestamp": {
                "commitment": commitment_data["commitment"]
            },
            "shareable": shareable,
            "hash": activity_hash
        }
        
        # Store private data separately (not in final file)
        activity["_private"] = commitment_data["_private"]
        
        return activity
    
    @staticmethod
    def create_day(
        date: str,
        activities: List[Dict],
        previous_day_hash: Optional[str] = None,
        note: Optional[str] = None
    ) -> Dict:
        """
        Create a forward-secure day entry
        
        Args:
            date: Date in YYYY-MM-DD format
            activities: List of activity dictionaries
            previous_day_hash: Hash of previous day (None for first day)
            note: Optional daily note
            
        Returns:
            Day dictionary with forward-secure hash
        """
        if previous_day_hash is None:
            previous_day_hash = "0" * 64
        
        # Sort activities by hash for deterministic ordering
        activity_hashes = sorted([a["hash"] for a in activities])
        activities_hash = PersonalHistoryV001.hash_data("".join(activity_hashes))
        
        # Hash note (or use zero hash)
        note_hash = PersonalHistoryV001.hash_data(note) if note else "0" * 64
        
        # Get timestamp commitment from first activity (or create dummy)
        timestamp_commitment = activities[0]["timestamp"]["commitment"] if activities else "0" * 64
        
        # Create day hash (forward-secure)
        hash_input = (
            previous_day_hash +
            date +
            timestamp_commitment +
            activities_hash +
            note_hash
        )
        day_hash = PersonalHistoryV001.hash_data(hash_input)
        
        # Build day entry
        day = {
            "date": date,
            "timestamp": {
                "commitment": timestamp_commitment
            },
            "activities": activities,
            "hash": day_hash
        }
        
        if note:
            day["note"] = note
        
        return day
    
    @staticmethod
    def create_identity(name: Optional[str] = None) -> Dict:
        """
        Create a new identity (Ed25519 keypair)
        
        Args:
            name: Optional human-readable name
            
        Returns:
            Identity dictionary with keys and hash
        """
        if CRYPTO_AVAILABLE:
            # Generate Ed25519 keypair
            private_key = ed25519.Ed25519PrivateKey.generate()
            public_key = private_key.public_key()
            
            # Serialize keys
            private_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
            public_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            
            # Create identity hash (public key + salt)
            salt = secrets.token_hex(16)
            identity_hash = PersonalHistoryV001.hash_data(
                public_bytes.hex() + salt
            )
            
            return {
                "private_key": base64.b64encode(private_bytes).decode(),
                "public_key": base64.b64encode(public_bytes).decode(),
                "identity_hash": identity_hash,
                "salt": salt,
                "name": name
            }
        else:
            # Simulated identity for demonstration
            print("Warning: Using simulated identity (cryptography library not available)")
            identity_hash = PersonalHistoryV001.hash_data(
                secrets.token_hex(32) + secrets.token_hex(16)
            )
            return {
                "private_key": "simulated_" + secrets.token_hex(32),
                "public_key": "simulated_" + secrets.token_hex(32),
                "identity_hash": identity_hash,
                "salt": secrets.token_hex(16),
                "name": name
            }
    
    @staticmethod
    def create_file(identity: Dict, timeline: Optional[List[Dict]] = None) -> Dict:
        """
        Create a new Personal History file
        
        Args:
            identity: Identity dictionary from create_identity()
            timeline: Optional list of day entries
            
        Returns:
            Personal History file dictionary
        """
        return {
            "version": PersonalHistoryV001.VERSION,
            "identity": {
                "hash": identity["identity_hash"],
                "name": identity.get("name")
            },
            "timeline": timeline or [],
            "signature": None  # Will be added after signing
        }
    
    @staticmethod
    def add_day_to_file(
        ph_file: Dict,
        date: str,
        activities: List[Dict],
        note: Optional[str] = None
    ) -> Dict:
        """
        Add a day to a Personal History file
        
        Args:
            ph_file: Personal History file dictionary
            date: Date in YYYY-MM-DD format
            activities: List of activity dictionaries
            note: Optional daily note
            
        Returns:
            Updated Personal History file
        """
        # Get previous day hash
        previous_day_hash = "0" * 64
        if ph_file["timeline"]:
            previous_day_hash = ph_file["timeline"][-1]["hash"]
        
        # Create day entry
        day = PersonalHistoryV001.create_day(
            date=date,
            activities=activities,
            previous_day_hash=previous_day_hash,
            note=note
        )
        
        # Add to timeline
        ph_file["timeline"].append(day)
        
        return ph_file
    
    @staticmethod
    def sign_file(ph_file: Dict, private_key: str) -> str:
        """
        Sign a Personal History file
        
        Args:
            ph_file: Personal History file dictionary
            private_key: Base64-encoded private key
            
        Returns:
            Signature (hex encoded)
        """
        # Create file hash (identity + timeline)
        identity_hash = ph_file["identity"]["hash"]
        timeline_str = json.dumps(ph_file["timeline"], sort_keys=True)
        file_hash_input = identity_hash + timeline_str
        file_hash = PersonalHistoryV001.hash_data(file_hash_input)
        
        if CRYPTO_AVAILABLE:
            # Load private key
            private_bytes = base64.b64decode(private_key)
            signing_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)
            
            # Sign
            signature = signing_key.sign(file_hash.encode())
            return signature.hex()
        else:
            # Simulated signature for demonstration
            print("Warning: Using simulated signature")
            return "simulated_" + PersonalHistoryV001.hash_data(file_hash)[:112]
    
    @staticmethod
    def verify_file(ph_file: Dict, public_key: str) -> bool:
        """
        Verify a Personal History file signature
        
        Args:
            ph_file: Personal History file dictionary
            public_key: Base64-encoded public key
            
        Returns:
            True if signature is valid
        """
        if ph_file.get("signature") is None:
            return False
        
        # Recreate file hash
        identity_hash = ph_file["identity"]["hash"]
        timeline_str = json.dumps(ph_file["timeline"], sort_keys=True)
        file_hash_input = identity_hash + timeline_str
        file_hash = PersonalHistoryV001.hash_data(file_hash_input)
        
        if CRYPTO_AVAILABLE:
            try:
                # Load public key
                public_bytes = base64.b64decode(public_key)
                verifying_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
                
                # Verify signature
                signature = bytes.fromhex(ph_file["signature"])
                verifying_key.verify(signature, file_hash.encode())
                return True
            except Exception:
                return False
        else:
            # Simulated verification for demonstration
            print("Warning: Using simulated verification")
            expected_sig = "simulated_" + PersonalHistoryV001.hash_data(file_hash)[:112]
            return ph_file["signature"] == expected_sig
    
    @staticmethod
    def verify_forward_chain(ph_file: Dict) -> bool:
        """
        Verify the forward-secure hash chain
        
        Args:
            ph_file: Personal History file dictionary
            
        Returns:
            True if chain is intact
        """
        previous_hash = "0" * 64
        
        for day in ph_file["timeline"]:
            # In a full implementation, would recreate and compare day hash
            # For now, just check structure
            if not day.get("hash") or len(day["hash"]) != 64:
                return False
            
            # Check activities have hashes
            for activity in day.get("activities", []):
                if not activity.get("hash") or len(activity["hash"]) != 64:
                    return False
            
            previous_hash = day["hash"]
        
        return True
    
    @staticmethod
    def save_file(ph_file: Dict, filepath: str) -> None:
        """
        Save Personal History file to disk
        
        Args:
            ph_file: Personal History file dictionary
            filepath: Path to save file
        """
        # Create clean copy without private data
        clean_file = json.loads(json.dumps(ph_file))
        
        # Remove private fields from days and activities
        for day in clean_file["timeline"]:
            day.pop("_private", None)
            for activity in day.get("activities", []):
                activity.pop("_private", None)
        
        # Write to file
        with open(filepath, 'w') as f:
            json.dump(clean_file, f, indent=2)
    
    @staticmethod
    def load_file(filepath: str) -> Dict:
        """
        Load Personal History file from disk
        
        Args:
            filepath: Path to load file from
            
        Returns:
            Personal History file dictionary
        """
        with open(filepath, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def analyze_time(ph_file: Dict) -> Dict:
        """
        Analyze time distribution from Personal History file
        
        Args:
            ph_file: Personal History file dictionary
            
        Returns:
            Dictionary with time analysis
        """
        activity_totals = {}
        day_count = 0
        total_tracked_minutes = 0
        
        for day in ph_file["timeline"]:
            day_count += 1
            
            for activity in day.get("activities", []):
                activity_type = activity["type"]
                duration = activity.get("duration", 0)
                
                if activity_type not in activity_totals:
                    activity_totals[activity_type] = {
                        "count": 0,
                        "total_minutes": 0,
                        "shareable_count": 0
                    }
                
                activity_totals[activity_type]["count"] += 1
                activity_totals[activity_type]["total_minutes"] += duration
                total_tracked_minutes += duration
                
                if activity.get("shareable", True):
                    activity_totals[activity_type]["shareable_count"] += 1
        
        return {
            "days_analyzed": day_count,
            "total_tracked_minutes": total_tracked_minutes,
            "total_tracked_hours": total_tracked_minutes / 60,
            "activity_totals": activity_totals
        }
    
    @staticmethod
    def export_shareable(ph_file: Dict) -> List[Dict]:
        """
        Export only shareable activities
        
        Args:
            ph_file: Personal History file dictionary
            
        Returns:
            List of days with only shareable activities
        """
        shareable_days = []
        
        for day in ph_file["timeline"]:
            shareable_activities = [
                activity for activity in day.get("activities", [])
                if activity.get("shareable", True)
            ]
            
            if shareable_activities:
                shareable_day = {
                    "date": day["date"],
                    "activities": shareable_activities
                }
                if "note" in day:
                    shareable_day["note"] = day["note"]
                shareable_days.append(shareable_day)
        
        return shareable_days
    
    @staticmethod
    def reveal_times(activity: Dict, nonce: str) -> Dict:
        """
        Reveal exact times for an activity (selective disclosure)
        
        Args:
            activity: Activity dictionary
            nonce: Nonce used in timestamp commitment
            
        Returns:
            Dictionary with revealed times and verification data
        """
        if "_private" not in activity:
            raise ValueError("Activity does not have private time data")
        
        exact_start = activity["_private"]["exact_start"]
        exact_end = activity["_private"]["exact_end"]
        commitment = activity["timestamp"]["commitment"]
        
        # Verify the commitment matches
        commitment_input = exact_start + exact_end + nonce
        calculated_commitment = PersonalHistoryV001.hash_data(commitment_input)
        
        if calculated_commitment != commitment:
            raise ValueError("Nonce does not match commitment")
        
        return {
            "activity_type": activity["type"],
            "duration": activity["duration"],
            "data": activity["data"],
            "exact_start": exact_start,
            "exact_end": exact_end,
            "commitment": commitment,
            "nonce": nonce,
            "verified": True
        }