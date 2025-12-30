"""
Encryption module for medical records
Uses AES-256 encryption with Fernet (symmetric encryption)
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os
import json


class MedicalEncryption:
    def __init__(self, master_password: str = "MedicalAssistant2025SecureKey!"):
        """Initialize encryption with master password"""
        # Derive encryption key from master password
        salt = b'medical_assistant_salt_2025'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.cipher = Fernet(key)
    
    def encrypt_data(self, data: dict) -> tuple:
        """
        Encrypt medical data
        Returns: (encrypted_data, iv)
        """
        # Convert dict to JSON string
        json_data = json.dumps(data)
        
        # Encrypt
        encrypted = self.cipher.encrypt(json_data.encode())
        
        # Generate IV (initialization vector)
        iv = os.urandom(16)
        
        return encrypted, iv
    
    def decrypt_data(self, encrypted_data: bytes, iv: bytes = None) -> dict:
        """
        Decrypt medical data
        Returns: dict
        """
        try:
            # Decrypt
            decrypted = self.cipher.decrypt(encrypted_data)
            
            # Convert back to dict
            json_data = decrypted.decode()
            return json.loads(json_data)
        except Exception as e:
            print(f"❌ Decryption error: {e}")
            return None


# Global encryption instance
encryptor = MedicalEncryption()
