#!/usr/bin/env python3
"""
Solution script for Ep 07: The Mastermind's Vault
Primitive: RSA Factorization via Prime Sum S = p + q
"""
import math

def solve():
    N = 4500791071531510688079140697614838981415165766485854432963406849723114644459783150792858825530803956365710192774976102022390436576313738093223835732784243
    S = 135378724644682718325503445810179552201556084300084253944571735035268611080004
    e = 65537
    c = 255609630350012896743516777521495731567826834863239616980530916043169342788192254069697171902711823261215211589441479109075860650849157841568981281543382

    # 1. Quadratic discriminant: (p - q)^2 = S^2 - 4N
    delta = S * S - 4 * N
    diff = math.isqrt(delta)
    assert diff * diff == delta, "Discriminant is not a perfect square!"

    # 2. Recover primes p and q
    p = (S + diff) // 2
    q = S - p
    assert p * q == N, "Prime factorization check failed!"

    print(f"[+] Recovered prime p: {p}")
    print(f"[+] Recovered prime q: {q}")

    # 3. Decrypt RSA
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, N)

    byte_len = (m.bit_length() + 7) // 8
    flag = m.to_bytes(byte_len, "big").decode("utf-8")
    print(f"[+] Recovered Flag: {flag}")
    return flag

if __name__ == "__main__":
    solve()
