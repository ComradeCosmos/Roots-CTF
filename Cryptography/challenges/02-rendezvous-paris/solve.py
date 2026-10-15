#!/usr/bin/env python3
"""
Solution script for Ep 02: Rendezvous in Paris
Cipher: Autokey Cipher (Primer = "PARIS")
"""

def solve():
    with open("cipher.txt", "r") as f:
        ciphertext = f.readline().strip()
    primer = "PARIS"

    keystream = list(primer.lower())
    plain = []
    k_idx = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('a') if ch.islower() else ord('A')
            c = ord(ch.lower()) - ord('a')
            k = ord(keystream[k_idx]) - ord('a')
            p = (c - k) % 26
            p_char = chr(p + ord('a'))
            keystream.append(p_char)  # Autokey: Plaintext extends keystream!
            plain.append(chr(p + base))
            k_idx += 1
        else:
            plain.append(ch)

    recovered = "".join(plain)
    print(f"[+] Recovered Plaintext: {recovered}")
    return recovered

if __name__ == "__main__":
    solve()
