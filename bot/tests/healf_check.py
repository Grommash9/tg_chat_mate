import requests
from os import getenv

DOMAIN = getenv("DOMAIN")

def check_login_page():
    resp = requests.get(f"https://{DOMAIN}/login", verify=False)
    assert resp.status_code == 200

check_login_page()
