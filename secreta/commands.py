import json

import typer

from secreta.constants import PASSWORDS_FILE
from secreta.utils import auth_user, decrypt_from_service, encrypt_credentials, get_credentials

app = typer.Typer()

@app.command()
def set():
    """Set your secreta access password"""
    access_password = input("Set your secreta access password: ")
    d = get_credentials()
    encrypted = encrypt_credentials(access_password)
    d["access_password"] = {"password": encrypted["password"], "key": encrypted["key"]}
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(d, f)
    print(typer.style("Access password set successfully!", fg=typer.colors.GREEN))


@app.command()
def new():
    """Add new credentials for a service"""
    if auth_user():
        service = input("Set the service you would like to add: ").lower()
        username = input("Set your service username: ")
        password = input("Set your service password: ")
        encrypted = encrypt_credentials(password, username)
        d = get_credentials()
        d[service] = {"username": encrypted["username"], "password": encrypted["password"], "key": encrypted["key"]}
        with open(PASSWORDS_FILE, "w") as f:
            json.dump(d, f)
        print(typer.style(f"Credentials for {service.capitalize()} set successfully!", fg=typer.colors.GREEN))
    else:
        print(typer.style("Invalid access password!", fg=typer.colors.RED))


@app.command()
def get(service: str):
    """Get credentials for a given service"""
    if auth_user():
        d = get_credentials()
        service = service.lower()
        username = d[service]["username"]
        decrypted = decrypt_from_service(service)
        print(typer.style(f"Username: {decrypted['username']}", fg=typer.colors.YELLOW))
        print(typer.style(f"Password: {decrypted['password']}", fg=typer.colors.YELLOW))
    else:
        print(typer.style("Invalid access password!", fg=typer.colors.RED))


@app.command()
def ls():
    """List all credentials added"""
    if auth_user():
        d = get_credentials()
        keys = d.keys()
        if len(keys) == 1:
            print(typer.style("No credentials added yet!", fg=typer.colors.RED))
        for key in keys:
            if key != "access_password":
                print(typer.style(key.capitalize(), fg=typer.colors.BLUE))
    else:
        print(typer.style("Invalid access password!", fg=typer.colors.RED))


if __name__ == "__main__":
    app()