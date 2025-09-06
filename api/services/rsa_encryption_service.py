import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class RSAEncryption:
    def __init__(self):
        self.private_key = self.load_private_key()
        self.public_key = self.load_public_key()
        
    def load_private_key(self):
        # Load private key from environment variable
        private_key = os.getenv("RSA_PRIVATE_KEY")
        if private_key:
            return serialization.load_pem_private_key(private_key.encode('utf-8'), password=None, backend=default_backend())
        else:
            return None
        
    def load_public_key(self):
        # Load public key from environment variable
        public_key = os.getenv("RSA_PUBLIC_KEY")
        if public_key:
            return serialization.load_pem_public_key(public_key.encode('utf-8'), backend=default_backend())
        else:
            return None
    
    def encrypt(self, plaintext):
        if self.public_key:
            try:
                ciphertext = self.public_key.encrypt(
                    plaintext.encode('utf-8'),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                return base64.b64encode(ciphertext).decode('utf-8')  # return Base64
            except Exception as e:
                print(f"[RSAEncryption][encrypt] >> Error encrypting data: {e}")
                return None
        else:
            raise ValueError("Public key not loaded")
        
    def decrypt(self, ciphertext_b64):
        if self.private_key:
            try:
                ciphertext = base64.b64decode(ciphertext_b64)  # decode from base64
                plaintext = self.private_key.decrypt(
                    ciphertext,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                return plaintext.decode('utf-8')
            except Exception as e:
                print(f"[RSAEncryption][decrypt] >> Error decrypting data: {e}")
                return None
        else:
            raise ValueError("Private key not loaded")
        
    