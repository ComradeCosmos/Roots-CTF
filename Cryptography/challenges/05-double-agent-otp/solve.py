#!/usr/bin/env python3
"""
Solution script for Ep 05: The Double Agent's Dilemma
Cipher: One-Time Pad Keystream Reuse (Two-Time Pad)
"""

def solve():
    c1_hex = "293c24353a203e7f1154722463173566221e2f78547f2f74337d267f347211307146762e252d31223f5421791e546228700b3f66446f5715"
    c2_hex = "25232c2a3a3a33101c3b7f2b7a0d3d7120654378211c2513327c25114272133f1436762f2f2124333e26577116267d2270145073250b2615"

    c1 = bytes.fromhex(c1_hex)
    c2 = bytes.fromhex(c2_hex)

    # Known prefix from prompt
    known_prefix = b"OPERATION CIPHERFALL: "
    partial_key = bytes([c ^ p for c, p in zip(c1[:len(known_prefix)], known_prefix)])
    print(f"[+] Recovered partial key: {partial_key}")

    # Full recovered message 1
    p1 = b"OPERATION CIPHERFALL: AGENT VANCE ESCAPED VIA SECTOR 04!"
    full_keystream = bytes([c ^ p for c, p in zip(c1, p1)])

    # Extract flag (36 characters: 'flag{tw0_t1m3_p4d_c4n_n3v3r_b3_s4f3}')
    flag = full_keystream[:36].decode("utf-8")
    print(f"[+] Recovered Flag: {flag}")

    # Verify message 2
    p2 = bytes([c ^ k for c, k in zip(c2, full_keystream)])
    print(f"[+] Verified Message 2: {p2.decode('utf-8')}")
    return flag

if __name__ == "__main__":
    solve()
