#!/usr/bin/env python3
import hashlib

def solve():
    p = 19997
    g = 5
    A = 2058
    B = 5125
    enc_hex = "dcb3befd9402acd25d8ced090b074a1ca207545c2a9842e98a74b089551a6ba48aadbca9961e"
    enc_bytes = bytes.fromhex(enc_hex)

    alice_secret = None
    for a in range(1, p):
        if pow(g, a, p) == A:
            alice_secret = a
            break

    print(f"[+] Found Alice secret exponent: a = {alice_secret}")
    shared_secret = pow(B, alice_secret, p)
    print(f"[+] Shared Secret: S = {shared_secret}")

    key = hashlib.sha256(str(shared_secret).encode("utf-8")).digest()
    flag_bytes = bytes([c ^ key[i % len(key)] for i, c in enumerate(enc_bytes)])
    flag = flag_bytes.decode("utf-8")
    print(f"[+] Recovered Flag: {flag}")
    return flag

if __name__ == "__main__":
    solve()
