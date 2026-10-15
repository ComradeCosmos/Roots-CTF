#!/usr/bin/env python3
"""
Solution script for Ep 06: Protocol DH-9000
Primitive: Diffie-Hellman Key Exchange with SHA-256 Key Derivation
"""
import hashlib

def solve():
    p = 19997
    g = 5
    A = 2058
    B = 5125
    enc_hex = "e8b0b0ee8118a4d6798cb4250c440a0be36b4c5f12ab10fca062f1a3471946a189bba2"
    enc_bytes = bytes.fromhex(enc_hex)

    # 1. Solve discrete log for a
    alice_secret = None
    for a in range(1, p):
        if pow(g, a, p) == A:
            alice_secret = a
            break

    print(f"[+] Found Alice secret exponent: a = {alice_secret}")

    # 2. Compute shared secret
    shared_secret = pow(B, alice_secret, p)
    print(f"[+] Shared Secret: S = {shared_secret}")

    # 3. Derive key via SHA-256
    key = hashlib.sha256(str(shared_secret).encode("utf-8")).digest()

    # 4. Decrypt payload
    flag_bytes = bytes([c ^ key[i % len(key)] for i, c in enumerate(enc_bytes)])
    flag = flag_bytes.decode("utf-8")
    print(f"[+] Recovered Flag: {flag}")
    return flag

if __name__ == "__main__":
    solve()
