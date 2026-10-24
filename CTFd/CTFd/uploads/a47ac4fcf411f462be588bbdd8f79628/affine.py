#!/usr/bin/env python3
"""
Droid Modular Transformation Engine
Alphabet: 'abcdefghijklmnopqrstuvwxyz0123456789_' (Length 37 - Prime Modulus!)
Formula: E(x) = (a * x + b) mod 37
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789_"
MODULUS = 37

def encrypt_affine37(text, a, b):
    assert 1 <= a < MODULUS, "a must be in range [1, 36]"
    res = []
    for ch in text:
        is_upper = ch.isupper()
        ch_lower = ch.lower()
        if ch_lower in ALPHABET:
            x = ALPHABET.index(ch_lower)
            enc_ch = ALPHABET[(a * x + b) % MODULUS]
            res.append(enc_ch.upper() if is_upper else enc_ch)
        else:
            res.append(ch)
    return "".join(res)

if __name__ == "__main__":
    print(f"Affine-37 cipher initialized. Modulus = {MODULUS} (Prime).")
