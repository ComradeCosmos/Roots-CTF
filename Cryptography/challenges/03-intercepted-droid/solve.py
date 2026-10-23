#!/usr/bin/env python3
ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789_"
MODULUS = 37

def solve():
    with open("cipher.txt", "r") as f:
        ciphertext = f.read().strip()

    for a in range(1, MODULUS):
        a_inv = pow(a, -1, MODULUS)
        for b in range(MODULUS):
            dec = []
            for ch in ciphertext:
                is_upper = ch.isupper()
                ch_lower = ch.lower()
                if ch_lower in ALPHABET:
                    y = ALPHABET.index(ch_lower)
                    x = (a_inv * (y - b)) % MODULUS
                    dec_ch = ALPHABET[x]
                    dec.append(dec_ch.upper() if is_upper else dec_ch)
                else:
                    dec.append(ch)
            candidate = "".join(dec)
            if candidate.startswith("flagfall{") and "m0dul4r" in candidate:
                print(f"[+] Found keys: a = {a}, b = {b}")
                print(f"[+] Recovered Flag: {candidate}")
                return candidate

if __name__ == "__main__":
    solve()
