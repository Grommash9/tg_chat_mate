import time
from os import getenv

import pytest
import requests

DOMAIN = getenv("DOMAIN", "3236-148-252-133-159.ngrok-free.app")
USER_NAME = "root"
PASSWORD = getenv("ROOT_PASSWORD", "root")


# @staticmethod
@pytest.fixture(scope="module")
def access_token():
    auth_endpoint_url = f"https://{DOMAIN}/tg-bot/manager/login"
    payload = {
        "username": USER_NAME,
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
        response = requests.get(url, verify=False, headers=headers)
        assert response.status_code == 200, "Can't find uploaded file!"


class TestLogin:
    def test_check_login_page(self):
        login_url = f"https://{DOMAIN}/login"
        response = requests.get(login_url, verify=False)
        assert response.status_code == 200, "Login page is not accessible"

    def test_try_to_fail_get_token(self):
        auth_endpoint_url = f"https://{DOMAIN}/tg-bot/manager/login"
        payload = {
            "username": USER_NAME,
            "password": PASSWORD + "?>asfl",
        }
        response = requests.post(auth_endpoint_url, json=payload, verify=False)
        assert (
            response.status_code == 401
        ), "Invalid credentials should not be accepted"

    def test_try_to_get_token(self):
        auth_endpoint_url = f"https://{DOMAIN}/tg-bot/manager/login"
        payload = {"username": USER_NAME, "password": PASSWORD}
        response = requests.post(auth_endpoint_url, json=payload, verify=False)
        assert (
            response.status_code == 200
        ), "Valid credentials should be accepted"
        assert "token" in response.json(), "Response should contain a token"

    def test_token_check_logic(self):
        auth_endpoint_url = f"https://{DOMAIN}/tg-bot/manager/login"
        payload = {"username": USER_NAME, "password": PASSWORD}
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
        json_data = {"is_banned": False, "country": "Ukraine"}
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

    def test_user_send_notification_about_manager_activity(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }

        url = f"https://{DOMAIN}/tg-bot/user/72105900/typing"
        response = requests.post(url, headers=headers, verify=False)

        assert response.status_code == 500
        assert (
            response.json().get("result")
            == "cant send notification to user, error "
            "Telegram server says - Bad Request: chat not found"
        )

        response = requests.post(url, headers=headers, verify=False)
        assert response.status_code == 429
        assert (
            response.json().get("result")
            == "notification don`t pass flood check"
        ), "wrong result received in flood error response"
        time.sleep(5)
        response = requests.post(url, headers=headers, verify=False)
        assert response.status_code == 500
        assert (
            response.json().get("result")
            == "cant send notification to user, error "
            "Telegram server says - Bad Request: chat not found"
        )


class TestManager:
    base_url = f"https://{DOMAIN}/tg-bot"

    def test_create_new_duplicate_delete_manager(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }
        url = f"{self.base_url}/manager"
        payload = {
            "username": "random_manager",
            "password": "1238234212341234",
            "full_name": "Random full name",
        }
        self.delete_manager(access_token, payload["username"])

        response = requests.post(
            url, headers=headers, verify=False, json=payload
        )
        assert (
            response.status_code == 201
        ), "Wrong status code on manager creating"
        assert "result" in response.json().keys(), "result is not in response"

        response = requests.post(
            url, headers=headers, verify=False, json=payload
        )
        assert response.status_code == 409, "Wrong status on manager creating"
        assert "result" in response.json().keys(), "result is not in response"

        self.delete_manager(access_token, payload["username"])

    def test_get_managers(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }
        url = f"{self.base_url}/manager"
        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200, "Wrong status on manager getting"
        assert (
            "managers" in response.json().keys()
        ), "managers is not in response"
        manager_active_status = {
            manager["username"]: manager.get("activated")
            for manager in response.json()["managers"]
        }
        assert "root" in manager_active_status.keys()

    def delete_manager(self, token, username: str) -> None:
        headers = {
            "AuthorizationToken": token,
        }
        url = f"{self.base_url}/manager"
        response = requests.delete(
            url, headers=headers, verify=False, json={"username": username}
        )
        assert response.status_code == 204, "Wrong status on manager deleting"

    def manager_get_token(self, username: str, password: str) -> str:
        url = f"{self.base_url}/manager/login"
        payload = {"username": username, "password": password}
        response = requests.post(url, verify=False, json=payload)
        assert response.status_code == 200, "Wrong status on manager get token"
        data = response.json()
        assert "token" in data.keys()
        return data["token"]

    def test_new_manager_change_password(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }
        url = f"{self.base_url}/manager"
        payload = {
            "username": "random_manager2",
            "password": "1238234212341234",
            "full_name": "Random full name",
        }
        self.delete_manager(access_token, payload["username"])
        response = requests.post(
            url, headers=headers, verify=False, json=payload
        )
        assert (
            response.status_code == 201
        ), "Wrong status code on manager creating"

        path_payload = {
            "username": payload["username"],
            "activated": True,  # type: ignore
        }
        response = requests.patch(
            url, headers=headers, verify=False, json=path_payload
        )
        assert response.status_code == 200, "Wrong status on manager update"

        cur_manager_token = self.manager_get_token(
            payload["username"], payload["password"]
        )

        cur_manager_headers = {
            "AuthorizationToken": cur_manager_token,
        }

        change_password_url = f"{self.base_url}/manager/change-password"
        wrong_pass_payload = {
            "new_password": "MyNewPassword01",
            "old_password": payload["password"] + "2",
        }
        response = requests.post(
            change_password_url,
            headers=cur_manager_headers,
            verify=False,
            json=wrong_pass_payload,
        )
        assert (
            response.status_code == 401
        ), "Wrong status code on manager change password error"

        new_pass_payload = {
            "new_password": "MyNewPassword01",
            "old_password": payload["password"],
        }
        response = requests.post(
            change_password_url,
            headers=cur_manager_headers,
            verify=False,
            json=new_pass_payload,
        )
        assert (
            response.status_code == 201
        ), "Wrong status code on manager change password"

        new_manager_token = self.manager_get_token(
            payload["username"], "MyNewPassword01"
        )

        get_me_url = f"{self.base_url}/manager/get-me"
        new_manager_headers = {
            "AuthorizationToken": new_manager_token,
        }
        response = requests.get(
            get_me_url, headers=new_manager_headers, verify=False
        )
        assert (
            response.status_code == 200
        ), "Wrong status code on manager get me method"
        data = response.json()
        assert (
            "manager_info" in data.keys()
        ), "Manager info missing from response"
        assert "random_manager2" == data["manager_info"]["username"]
        self.delete_manager(access_token, payload["username"])

    def test_create_new_patch_get_manager(self, access_token):
        headers = {
            "AuthorizationToken": access_token,
        }
        url = f"{self.base_url}/manager"
        payload = {
            "username": "random_manager",
            "password": "1238234212341234",
            "full_name": "Random full name",
        }
        self.delete_manager(access_token, payload["username"])

        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200, "Wrong status on manager getting"
        assert (
            "managers" in response.json().keys()
        ), "managers is not in response"
        manager_active_status = {
            manager["username"]: manager.get("activated")
            for manager in response.json()["managers"]
        }
        assert "random_manager" not in manager_active_status.keys()

        response = requests.post(
            url, headers=headers, verify=False, json=payload
        )
        assert (
            response.status_code == 201
        ), "Wrong status code on manager creating"

        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200, "Wrong status on manager getting"
        assert (
            "managers" in response.json().keys()
        ), "managers is not in response"
        manager_active_status = {
            manager["username"]: manager.get("activated")
            for manager in response.json()["managers"]
        }
        assert "random_manager" in manager_active_status.keys()
        assert manager_active_status["random_manager"] is None

        payload = {
            "username": "random_manager",
            "activated": True,  # type: ignore
        }
        response = requests.patch(
            url, headers=headers, verify=False, json=payload
        )
        assert response.status_code == 200, "Wrong status on manager update"

        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200, "Wrong status on manager getting"
        assert (
            "managers" in response.json().keys()
        ), "managers is not in response"
        manager_active_status = {
            manager["username"]: manager.get("activated")
            for manager in response.json()["managers"]
        }
        assert "random_manager" in manager_active_status.keys()
        assert manager_active_status["random_manager"] is True
