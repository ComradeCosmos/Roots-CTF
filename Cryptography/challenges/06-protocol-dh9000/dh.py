#!/usr/bin/env python3
"""
Protocol DH-9000 Satellite Key Agreement
"""
import hashlib

def compute_shared(peer_public, my_secret, mod):
    return pow(peer_public, my_secret, mod)

def derive_key(shared_secret):
    return hashlib.sha256(str(shared_secret).encode("utf-8")).digest()

def decrypt_payload(enc_bytes, key_bytes):
    return bytes([c ^ key_bytes[i % len(key_bytes)] for i, c in enumerate(enc_bytes)])

if __name__ == "__main__":
    p = 19997
    g = 5
    A = 2058
    B = 5125
    print("DH-9000 protocol loaded. Public modulus p = 19997.")
