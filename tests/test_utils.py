from unittest.mock import patch

import pytest
from faker import Faker
from typer.testing import CliRunner

from secreta.utils import auth_user, decrypt_from_service, encrypt_credentials

fake = Faker()
runner = CliRunner()

def test_encryptation_and_decryptation():
    service, username, password = fake.company(), fake.name(), fake.password()

    mock_data = {service: encrypt_credentials(password, username)}
    with patch("secreta.utils.get_credentials", return_value=mock_data):
        decrypted_credentials = decrypt_from_service(service)

    expected_credentials = {"username": username, "password": password}
    assert expected_credentials == decrypted_credentials


@pytest.mark.parametrize("correct_password, input_password, expected_output", [
    ("abc", "abc", True),
    ("abc", "def", False)
], ids=["right_password", "wrong_password"])
def test_auth_user(correct_password, input_password, expected_output):
    with patch("secreta.utils.decrypt_from_service", return_value={"password": correct_password}):
        is_auth_user = auth_user(input_password)

    assert is_auth_user == expected_output
