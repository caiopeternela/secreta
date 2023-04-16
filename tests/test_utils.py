from unittest.mock import patch

import pytest

from secreta.utils import auth_user, decrypt_from_service, encrypt_credentials


@pytest.mark.parametrize("mock_data, expected_result", [
    ({"typer": encrypt_credentials("fastapi123", "tiangolo")}, {"username": "tiangolo", "password": "fastapi123"}),
    ({}, {})
], ids=["with_credentials", "without_credentials"])
def test_encryptation_and_decryptation(mock_data, expected_result):
    with patch("secreta.utils.get_credentials", return_value=mock_data):
        decrypted_credentials = decrypt_from_service("typer")

    assert expected_result == decrypted_credentials


@pytest.mark.parametrize("correct_password, input_password, expected_output", [
    ("abc", "abc", True),
    ("abc", "def", False)
], ids=["right_password", "wrong_password"])
def test_auth_user(correct_password, input_password, expected_output):
    with patch("secreta.utils.decrypt_from_service", return_value={"password": correct_password}):
        is_auth_user = auth_user(input_password)

    assert is_auth_user == expected_output
