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
    c = 2144411243654665733738414831591240082934017738363813889430617693508656256982561235483335856372178259455360056694327262562560933227736140964225612522080124

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
