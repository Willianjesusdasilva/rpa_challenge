# /// script
# dependencies = ["httpx"]
# ///

import httpx

with httpx.Client(verify=False) as client:
    login = client.post(
        "https://localhost:3000/api/easy/login",
        json={"username": "admin", "password": "rpa@2026!"}
    )

    print("LOGIN:", login.status_code)
    print(login.text)
