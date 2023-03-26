import json
import os

from cryptography.fernet import Fernet

from secreta.constants import PASSWORDS_FILE


def get_passwords():
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as f:
            d = json.load(f)
            return d
    return {}


def encrypt_password(password: str):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return {"password": encrypted_password.decode(), "key": key.decode()}

def decrypt_from_service(service: str):
    d = get_passwords()
    if d == {}:
        return False
    key = d[service]["key"].encode()
    f = Fernet(key)
    password = d[service]["password"]
    decrypted_password = f.decrypt(password.encode()).decode()
    return decrypted_password


def auth_user():
    access_password = input("Enter your access password: ")
    return access_password == decrypt_from_service("access_password")