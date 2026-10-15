#!/usr/bin/env python3
"""
Solution script for Ep 05: The Double Agent's Dilemma
Cipher: One-Time Pad Keystream Reuse (Two-Time Pad)
"""

def solve():
    c1_hex = "1d3f2a26322f3d387e7f37783d7b1a227225132f0e4e1e297638675209237d1c361423603e133f2a30532d3d36100c3172397c0d5004507e"
    c2_hex = "112022393235305773103a7724611235705e7f2f7b2d144e7739643c7f237f1353642361341f2a3b31215b353e62133b722613183160217e"

    c1 = bytes.fromhex(c1_hex)
    c2 = bytes.fromhex(c2_hex)

    # Known prefix from prompt
    known_prefix = b"OPERATION CIPHERFALL: "
    partial_key = bytes([c ^ p for c, p in zip(c1[:len(known_prefix)], known_prefix)])
    print(f"[+] Recovered partial key: {partial_key}")

    # Full recovered message 1
    p1 = b"OPERATION CIPHERFALL: AGENT VANCE ESCAPED VIA SECTOR 04!"
    full_keystream = bytes([c ^ p for c, p in zip(c1, p1)])

    # Extract flag (37 characters: 'Roots{tw0_t1m3_p4d_c4n_n3v3r_b3_s4f3}')
    flag = full_keystream[:37].decode("utf-8")
    print(f"[+] Recovered Flag: {flag}")

    # Verify message 2
    p2 = bytes([c ^ k for c, k in zip(c2, full_keystream)])
    print(f"[+] Verified Message 2: {p2.decode('utf-8')}")
    return flag

if __name__ == "__main__":
    solve()
