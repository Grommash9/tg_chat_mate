from os import getenv

import requests

DOMAIN = getenv("DOMAIN")


def check_login_page():
    resp = requests.get(f"https://{DOMAIN}/login2", verify=False)
    assert resp.status_code == 200


check_login_page()
