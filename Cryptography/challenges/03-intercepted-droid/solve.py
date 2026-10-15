#!/usr/bin/env python3
"""
Solution script for Ep 03: The Intercepted Droid
Cipher: Affine over Base-37 Alphabet
Keys: a = 11, b = 23, modulus = 37
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789_"
MODULUS = 37

def solve():
    with open("cipher.txt", "r") as f:
        ciphertext = f.read().strip()

    # Brute-force all 36 * 37 = 1332 keys
    for a in range(1, MODULUS):
        a_inv = pow(a, -1, MODULUS)
        for b in range(MODULUS):
            dec = []
            for ch in ciphertext:
                if ch in ALPHABET:
                    y = ALPHABET.index(ch)
                    x = (a_inv * (y - b)) % MODULUS
                    dec.append(ALPHABET[x])
                else:
                    dec.append(ch)
            candidate = "".join(dec)
            if candidate.startswith("flag{") and "m0dul4r" in candidate:
                print(f"[+] Found keys: a = {a}, b = {b}")
                print(f"[+] Recovered Flag: {candidate}")
                return candidate

if __name__ == "__main__":
    solve()
