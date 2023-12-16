from os import getenv

import requests

DOMAIN = getenv("DOMAIN")


def check_login_page():
    login_url = f"https://{DOMAIN}/login"
    resp = requests.get(login_url, verify=False)
    print(resp.text)
    print(resp.status_code)
    assert resp.status_code == 200


check_login_page()
