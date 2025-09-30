from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os

def decrypt_aes_gcm(ciphertext_b64, iv_b64, key_b64):
    """Decrypt AES-GCM encrypted data"""
    try:
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)
        key = base64.b64decode(key_b64)
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(iv, ciphertext, None)
        return plaintext.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return None
