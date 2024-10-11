from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import os

SECRET_KEY = b'secret_key_16_by'

def encrypt_data(data: str) -> str:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return base64.urlsafe_b64encode(iv + encrypted).decode('utf-8')

def decrypt_data(encrypted_data: str) -> str:
    encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data)
    iv = encrypted_data_bytes[:16]
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(encrypted_data_bytes[16:]) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted.decode('utf-8')

def parse_serial_number(serial_number: str):
    decrypted_data = decrypt_data(serial_number)
    
    company_id, warehouse_id, item_id = decrypted_data.split('-')
    return {
        'company_id': int(company_id),
        'warehouse_id': int(warehouse_id),
        'item_id': int(item_id)
    }