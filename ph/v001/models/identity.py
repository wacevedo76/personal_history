"""
Identity Model for Personal History v0.01
"""

import hashlib
import secrets
import base64
from typing import Dict, Optional
from datetime import datetime


class Identity:
    """Represents a Personal History identity"""
    
    def __init__(self, name: Optional[str] = None):
        self.name = name
        self.private_key = None
        self.public_key = None
        self.identity_hash = None
        self.salt = None
        self.created_at = datetime.now().isoformat()
        
    def generate(self) -> 'Identity':
        """Generate cryptographic identity"""
        # Generate salt
        self.salt = secrets.token_hex(16)  # 16 bytes = 32 hex chars
        
        # Generate key pair using cryptography library
        # This is now required, not optional
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        
        # Generate Ed25519 key pair
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # Serialize keys
        self.private_key = base64.b64encode(
            private_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
        ).decode()
        
        self.public_key = base64.b64encode(
            public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
        ).decode()
        
        # Calculate identity hash
        identity_data = f"{self.public_key}{self.salt}"
        if self.name:
            identity_data += self.name
        
        self.identity_hash = hashlib.sha256(identity_data.encode()).hexdigest()
        
        return self
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "private_key": self.private_key,
            "public_key": self.public_key,
            "identity_hash": self.identity_hash,
            "salt": self.salt,
            "name": self.name,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Identity':
        """Create Identity from dictionary"""
        identity = cls(name=data.get("name"))
        identity.private_key = data.get("private_key")
        identity.public_key = data.get("public_key")
        identity.identity_hash = data.get("identity_hash")
        identity.salt = data.get("salt")
        identity.created_at = data.get("created_at", datetime.now().isoformat())
        return identity
    
    def verify(self) -> bool:
        """Verify identity integrity"""
        if not all([self.private_key, self.public_key, self.identity_hash, self.salt]):
            return False
        
        # Recalculate identity hash
        identity_data = f"{self.public_key}{self.salt}"
        if self.name:
            identity_data += self.name
        
        calculated_hash = hashlib.sha256(identity_data.encode()).hexdigest()
        
        return calculated_hash == self.identity_hash