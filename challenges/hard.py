# /// script
# dependencies = ["httpx", "cryptography"]
# ///

import httpx, hashlib, time, random, string, os, tempfile
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
import time

start = time.perf_counter()
BASE = "https://localhost:3000"
LOGIN = f"{BASE}/api/hard/login"

PFX = "client.pfx"
PFX_PASS = b"test123"


def nonce():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))


def challenge(ts, n):
    return hashlib.sha256((ts + n + "rpa_hard_challenge_2026").encode()).hexdigest()


def pfx_to_pem(pfx_path):
    pfx = open(pfx_path, "rb").read()
    key, cert, _ = pkcs12.load_key_and_certificates(pfx, PFX_PASS)

    kf = tempfile.NamedTemporaryFile(delete=False)
    cf = tempfile.NamedTemporaryFile(delete=False)

    kf.write(key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()))
    cf.write(cert.public_bytes(Encoding.PEM))

    kf.close()
    cf.close()

    return cf.name, kf.name


with httpx.Client(verify=False) as c:

    open(PFX, "wb").write(c.get(f"{BASE}/download/certs/client.pfx").content)
    ts = str(int(time.time() * 1000))
    n = nonce()

    r = c.post(LOGIN, json={
        "username": "operator",
        "password": "cert#Secure2026",
        "challenge": challenge(ts, n),
        "timestamp": ts,
        "nonce": n
    })

    data = r.json()
    assert data["success"], "Login falhou"

    redirect = data["redirect"]

    cookies = c.cookies


cert, key = pfx_to_pem(PFX)

with httpx.Client(
    verify=False,
    cert=(cert, key),
    cookies=cookies
) as c:

    final = c.get(redirect)
    
    print(f"Status code: {final.status_code}")
    print(f"Headers: {final.headers}")
    print(f"HTML: {final.text}")

os.unlink(cert)
os.unlink(key)
elapsed = time.perf_counter() - start
print(f"[HARD] Tempo total: {elapsed:.3f}s")