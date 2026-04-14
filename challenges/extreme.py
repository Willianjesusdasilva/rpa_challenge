# /// script
# dependencies = ["httpx", "websockets", "cryptography"]
# ///

import asyncio
import hashlib
import json
import ssl
import os
import threading

import httpx
import websockets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
BASE = "https://localhost:3000"


def solve_pow(prefix, difficulty):
    target = "0" * difficulty
    found = {"nonce": None}
    stop = threading.Event()
    threads = []
    workers = os.cpu_count()

    def worker(start):
        nonce = start
        while not stop.is_set():
            digest = hashlib.sha256(f"{prefix}{nonce}".encode()).hexdigest()
            if digest.startswith(target):
                found["nonce"] = str(nonce)
                stop.set()
                return
            nonce += workers * 4

    for i in range(workers):
        t = threading.Thread(target=worker, args=(i,), daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if found["nonce"] is None:
        raise RuntimeError("Não encontrou nonce válido.")

    return found["nonce"]


def decrypt_payload(session_id: str, encrypted_hex: str) -> dict:
    iv_hex, ciphertext_hex = encrypted_hex.split(":", 1)

    iv = bytes.fromhex(iv_hex)
    ciphertext = bytes.fromhex(ciphertext_hex)

    key = hashlib.sha256(f"{session_id}extreme_secret_key".encode()).digest()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()

    return json.loads(plaintext.decode())


async def main():
    ssl_context = ssl._create_unverified_context()

    async with httpx.AsyncClient(verify=False, timeout=20.0) as client:
        init = await client.post(f"{BASE}/api/extreme/init")
        init.raise_for_status()
        data = init.json()

        print("INIT:", data)

        session_id = data["session_id"]
        ws_ticket = data["ws_ticket"]

        ws_url = f"wss://localhost:3000/ws?ticket={ws_ticket}&session_id={session_id}"

        async with websockets.connect(
            ws_url,
            ssl=ssl_context,
            additional_headers={
                "User-Agent": "Mozilla/5.0",
                "Origin": "https://localhost:3000",
            },
        ) as ws:
            intermediate_token = None

            while True:
                raw = await ws.recv()
                print("WS RAW:", raw)

                msg = json.loads(raw)

                if msg.get("type") == "pow_challenge":
                    prefix = msg["prefix"]
                    difficulty = msg["difficulty"]

                    print("POW:", prefix, difficulty)

                    nonce = solve_pow(prefix, difficulty)
                    print("NONCE:", nonce)

                    await ws.send(json.dumps({"nonce": nonce}))
                    continue

                if msg.get("type") == "pow_result" and msg.get("success"):
                    intermediate_token = msg["intermediate_token"]
                    print("TOKEN:", intermediate_token)
                    break

                if msg.get("error"):
                    raise RuntimeError(f"Erro no WS: {msg['error']}")

            if not intermediate_token:
                raise RuntimeError("Não foi possível obter intermediate_token.")

        verify = await client.post(
            f"{BASE}/api/extreme/verify-token",
            json={
                "session_id": session_id,
                "intermediate_token": intermediate_token,
            },
        )
        verify.raise_for_status()
        verify_data = verify.json()

        print("VERIFY:", verify_data)

        encrypted_payload = verify_data["encrypted_payload"]
        decrypted = decrypt_payload(session_id, encrypted_payload)

        print("DECRYPTED:", decrypted)

        otp = decrypted["otp"]
        print("OTP:", otp)

        final = await client.post(
            f"{BASE}/api/extreme/complete",
            json={
                "session_id": session_id,
                "otp": otp,
                "username": "root",
                "password": "h4ck3r@Pr00f!"
            }
        )

        print("FINAL STATUS:", final.status_code)
        print("FINAL BODY:", final.text)
        final.raise_for_status()


if __name__ == "__main__":
    asyncio.run(main())