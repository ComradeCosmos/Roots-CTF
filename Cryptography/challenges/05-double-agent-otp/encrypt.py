#!/usr/bin/env python3
"""
Syndicate Tactical Communications Relay
CRITICAL WARNING: The keystream must NEVER be reused across multiple messages!
"""

def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

# Intercepted syndicate emergency alerts:
# Message 1: Begins with standard protocol prefix "OPERATION CIPHERFALL: "
# Message 2: Lockdown directive to security forces
# Both messages were masked with the identical One-Time Pad key!
