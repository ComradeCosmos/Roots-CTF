#!/usr/bin/env python3
"""
Solution script for Ep 01: The Quantum Beacon
Cipher: Alternating Positional Shift over Base-37 Alphabet
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789_"

def solve():
    with open("cipher.txt", "r") as f:
        ciphertext = f.read().strip()

    plaintext = []
    for i, ch in enumerate(ciphertext):
        if ch in ALPHABET:
            idx = ALPHABET.index(ch)
            if i % 2 == 0:
                new_idx = (idx - (i + 7)) % 37
            else:
                new_idx = (idx + (i * 3 + 5)) % 37
            plaintext.append(ALPHABET[new_idx])
        else:
            plaintext.append(ch)

    recovered = "".join(plaintext)
    print(f"[+] Recovered Plaintext: {recovered}")
    return recovered

if __name__ == "__main__":
    solve()
