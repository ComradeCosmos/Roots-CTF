#!/usr/bin/env python3
def solve():
    c1_hex = "293c243527352523355434790f3c743f751e3c785e7f22732b113a1320723c1c27131a2077276338224c372e27413f29382038627f44054c"
    c2_hex = "25232c2a272f284c383b397616267c28776550782b1c28142a10397d56723e1342631a217d2b7629233e41262f332023383f57771e20744c"

    c1 = bytes.fromhex(c1_hex)
    c2 = bytes.fromhex(c2_hex)

    known_prefix = b"OPERATION CIPHERFALL: "
    partial_key = bytes([c ^ p for c, p in zip(c1[:len(known_prefix)], known_prefix)])
    print(f"[+] Recovered partial key: {partial_key}")

    p1 = b"OPERATION CIPHERFALL: AGENT VANCE ESCAPED VIA SECTOR 04!"
    full_keystream = bytes([c ^ p for c, p in zip(c1, p1)])

    flag = full_keystream[:40].decode("utf-8")
    print(f"[+] Recovered Flag: {flag}")
    return flag

if __name__ == "__main__":
    solve()
