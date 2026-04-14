# /// script
# dependencies = ["httpx"]
# ///

import httpx
import time

start = time.perf_counter()
with httpx.Client(verify=False) as client:
    login = client.post(
        "https://localhost:3000/api/easy/login",
        json={"username": "admin", "password": "rpa@2026!"}
    )

    print("LOGIN:", login.status_code)
    print(login.text)
elapsed = time.perf_counter() - start
print(f"[EASY] Tempo total: {elapsed:.3f}s")