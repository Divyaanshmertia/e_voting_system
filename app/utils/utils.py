# utils.py
from cryptography.fernet import Fernet

# Function to generate a key. Call this once and store the key securely.
def generate_key():
    return Fernet.generate_key()

# Encrypt data
def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)
    return encrypted_data

# Decrypt data
def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data
def load_key():
    # Load your Fernet key from a file or environment variable
    return open("/home/divyaansh/Documents/M.TECH Studies/II SEM/Security/Project/e_voting_system/app/utils/a.key", "rb").read()


key = generate_key()
with open("/home/divyaansh/Documents/M.TECH Studies/II SEM/Security/Project/e_voting_system/app/utils/a.key", "wb") as key_file:
    key_file.write(key)

