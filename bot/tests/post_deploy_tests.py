from os import getenv

import pytest
import requests

DOMAIN = getenv("DOMAIN", "eeea-85-198-141-215.ngrok-free.app")
USER_NAME = "root"
PASSWORD = getenv("ROOT_PASSWORD", "root_strong_password")


# @staticmethod
@pytest.fixture(scope="module")
def access_token():
    auth_endpoint_url = f"https://{DOMAIN}/tg-bot/manager/login"
    payload = {
        "user_name": USER_NAME,
        "password": PASSWORD,
    }
    response = requests.post(auth_endpoint_url, json=payload, verify=False)
    assert response.status_code == 200, "Valid credentials should be accepted"
    token = response.json()["token"]
    return token


class TestFileStoring:
    def test_upload_file_to_db_without_duplicate(self, access_token):
        with open("tests/test_data/api-svgrepo-com.svg", "rb") as f:
            file_data = f.read()

        headers = {
            "Content-Type": "application/octet-stream",
            "X-Filename": "api-svgrepo-com.svg",
            "AuthorizationToken": access_token,
        }

        url = f"https://{DOMAIN}/tg-bot/file_upload"
        response = requests.post(
            url, headers=headers, data=file_data, verify=False
        )
        assert response.status_code == 201, "Wrong status code on file upload"
        assert (
            "file_id" in response.json().keys()
        ), "file_id is not in response"
        file_id = response.json()["file_id"]

        # Trying to upload same file again to get same id
        response = requests.post(
            url, headers=headers, data=file_data, verify=False
        )
        assert response.status_code == 201, "Wrong status code on file upload"
        assert (
            "file_id" in response.json().keys()
        ), "file_id is not in response"
        assert (
            file_id == response.json()["file_id"]
        ), "file_id changed for same file"

        # Checking what file exists
        url = f"https://{DOMAIN}/tg-bot/file?file_uuid={file_id}"
        response = requests.get(url, verify=False)
        assert response.status_code == 200, "Can't find uploaded file!"


class TestLogin:
    def test_check_login_page(self):
        login_url = f"https://{DOMAIN}/login"
        response = requests.get(login_url, verify=False)
        assert response.status_code == 200, "Login page is not accessible"

    def test_try_to_fail_get_token(self):
        auth_endpoint_url = f"https://{DOMAIN}/tg-bot/manager/login"
        payload = {
            "user_name": USER_NAME,
            "password": PASSWORD + "?>asfl",
        }
        response = requests.post(auth_endpoint_url, json=payload, verify=False)
        assert (
            response.status_code == 401
        ), "Invalid credentials should not be accepted"

    def test_try_to_get_token(self):
        auth_endpoint_url = f"https://{DOMAIN}/tg-bot/manager/login"
        payload = {"user_name": USER_NAME, "password": PASSWORD}
        response = requests.post(auth_endpoint_url, json=payload, verify=False)
        assert (
            response.status_code == 200
        ), "Valid credentials should be accepted"
        assert "token" in response.json(), "Response should contain a token"

    def test_token_check_logic(self):
        auth_endpoint_url = f"https://{DOMAIN}/tg-bot/manager/login"
        payload = {"user_name": USER_NAME, "password": PASSWORD}
        response = requests.post(auth_endpoint_url, json=payload, verify=False)
        assert (
            response.status_code == 200
        ), "Valid credentials should be accepted"
        token = response.json()["token"]

        check_token_endpoint = f"https://{DOMAIN}/tg-bot/manager/check_token"
        check_token_payload = {"token": token}
        response = requests.post(
            check_token_endpoint, json=check_token_payload, verify=False
        )
        assert (
            response.status_code == 200
        ), "Valid credentials should be accepted"
        assert response.json().get("manager") == USER_NAME

    def test_wrong_token_check_logic(self):
        wrong_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

        check_token_endpoint = f"https://{DOMAIN}/tg-bot/manager/check_token"
        check_token_payload = {"token": wrong_token}
        response = requests.post(
            check_token_endpoint, json=check_token_payload, verify=False
        )
        assert (
            response.status_code == 401
        ), "Valid credentials should be accepted"


class TestUser:
    def test_get_existing_user(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }
        url = f"https://{DOMAIN}/tg-bot/user/721058"
        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200, "Wrong status code on user getting"
        assert "_id" in response.json().keys(), "file_id is not in response"

    def test_not_existing_user(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }
        url = f"https://{DOMAIN}/tg-bot/user/72105900"
        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 404, "Wrong status code on user getting"
        assert (
            response.json().get("result") == "User not found"
        ), "founded user not existing"

    def test_update_user_info(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }
        json_data = {"is_banned": True, "country": "Ukraine"}

        url = f"https://{DOMAIN}/tg-bot/user/859203"
        response = requests.patch(
            url, headers=headers, json=json_data, verify=False
        )
        assert (
            response.status_code == 200
        ), "Wrong status code on update user information"

    def test_user_for_update_not_existing(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }
        json_data = {"is_banned": "true", "country": "Ukraine"}

        url = f"https://{DOMAIN}/tg-bot/user/72105900"
        response = requests.patch(
            url, headers=headers, json=json_data, verify=False
        )
        assert (
            response.status_code == 404
        ), "Wrong status code on update user information"
