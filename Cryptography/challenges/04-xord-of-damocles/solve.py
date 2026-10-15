#!/usr/bin/env python3
"""
Solution script for Ep 04: The XORd of Damocles
Cipher: LCG PRNG Stream Cipher (Brute-force 8-bit seed)
"""

def solve():
    with open("cipher.txt", "r") as f:
        hex_data = f.read().strip()
    cipher_bytes = bytes.fromhex(hex_data)

    A = 137
    C = 73
    MOD = 256

    for guess_seed in range(256):
        state = guess_seed
        plain = bytearray()
        for b in cipher_bytes:
            plain.append(b ^ state)
            state = (A * state + C) % MOD

        if plain.startswith(b"flag{"):
            flag = plain.decode("utf-8")
            print(f"[+] Found Seed: {guess_seed}")
            print(f"[+] Recovered Flag: {flag}")
            return flag

if __name__ == "__main__":
    solve()
