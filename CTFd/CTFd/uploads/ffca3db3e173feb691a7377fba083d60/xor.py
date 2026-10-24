#!/usr/bin/env python3
"""
Sentry Guard Dynamic Keystream Engine
PRNG: Linear Congruential Generator (LCG)
State Equation: S_{i+1} = (137 * S_i + 73) mod 256
"""

A = 137
C = 73
MOD = 256

def generate_keystream(seed, length):
    stream = []
    state = seed
    for _ in range(length):
        stream.append(state)
        state = (A * state + C) % MOD
    return bytes(stream)

def encrypt(plaintext_bytes, seed):
    keystream = generate_keystream(seed, len(plaintext_bytes))
    return bytes([p ^ k for p, k in zip(plaintext_bytes, keystream)])

if __name__ == "__main__":
    print("LCG Stream Cipher Engine ready. Seed space: 0..255.")
