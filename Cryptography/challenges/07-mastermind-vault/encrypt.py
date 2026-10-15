#!/usr/bin/env python3
"""
Syndicate Core Server Cryptosystem (RSA-512)
"""

def encrypt_rsa(message_bytes, e, n):
    m = int.from_bytes(message_bytes, 'big')
    return pow(m, e, n)

if __name__ == "__main__":
    print("RSA-512 Server Encryption Subsystem loaded.")
