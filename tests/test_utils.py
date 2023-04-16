import json
import os
from unittest.mock import patch

import pytest

from secreta.constants import PASSWORDS_FILE
from secreta.utils import auth_user, decrypt_from_service, encrypt_credentials, get_credentials, input_manager


@pytest.mark.parametrize("mock_data, expected_result", [
    ({"typer": encrypt_credentials("fastapi123", "tiangolo")}, {"username": "tiangolo", "password": "fastapi123"}),
    ({}, {})
], ids=["with_credentials", "without_credentials"])
def test_encryptation_and_decryptation(mock_data, expected_result):
    with patch("secreta.utils.get_credentials", return_value=mock_data):
        decrypted_credentials = decrypt_from_service("typer")

    assert expected_result == decrypted_credentials


@pytest.mark.parametrize("correct_password, input_password, expected_result", [
    ("abc", "abc", True),
    ("abc", "def", False)
], ids=["right_password", "wrong_password"])
def test_auth_user(correct_password, input_password, expected_result):
    with patch("secreta.utils.decrypt_from_service", return_value={"password": correct_password}):
        is_auth_user = auth_user(input_password)

    assert is_auth_user == expected_result


@pytest.mark.parametrize("mock_credentials", [
    {"typer": {"username": "tiangolo", "password": "fastapi123"}}, {}
], ids=["file_exists", "file_does_not_exist"])
def test_get_credentials(mock_credentials):
    if mock_credentials:
        with open(PASSWORDS_FILE, "w") as f:
            json.dump(mock_credentials, f)

    credentials = get_credentials()
    if os.path.exists(PASSWORDS_FILE):
        os.remove(PASSWORDS_FILE)

    assert credentials == mock_credentials


@pytest.mark.parametrize("input_list, is_access_password, expected_result", [
    (["typer", "tiangolo", "fastapi123", "fastapi123"], False, {"service": "typer", "username": "tiangolo", "password": "fastapi123"}),
    (["fastapi123", "django123", "fastapi123"], True, {"password": "fastapi123"}),
    (["fastapi123", "fastapi123"], True, {"password": "fastapi123"}),
])
@patch("typer.prompt")
def test_input_manager(mock_input, input_list, is_access_password, expected_result):
    mock_input.side_effect = input_list

    assert input_manager(access_password=is_access_password) == expected_result
