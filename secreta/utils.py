import json
import os

from cryptography.fernet import Fernet

from secreta.constants import PASSWORDS_FILE


def get_credentials() -> dict:
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as f:
            d = json.load(f)
            return d
    return {}


def encrypt_credentials(password: str, username: str = None) -> dict:
    key = Fernet.generate_key()
    f = Fernet(key)
    data = {}
    data["key"] = key.decode()
    data["password"] = f.encrypt(password.encode()).decode()
    if username:
        data["username"] = f.encrypt(username.encode()).decode()
    return data

def decrypt_from_service(service: str) -> dict:
    d = get_credentials()
    if d == {}:
        return {}
    key = d[service]["key"].encode()
    f = Fernet(key)
    data = {}
    if "username" in d.get(service, {}):
        username = d[service]["username"]
        data["username"] = f.decrypt(username.encode()).decode()
    password = d[service]["password"]
    data["password"] = f.decrypt(password.encode()).decode()
    return data


def auth_user() -> bool:
    access_password = input("Enter your access password: ")
    return access_password == decrypt_from_service("access_password").get("password")
