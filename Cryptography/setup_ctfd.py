#!/usr/bin/env python3
"""
Automated CTFd Challenge Importer & Provisioning Script
Deploys all 8 AI-Resistant Operation Cipherfall Cryptography challenges to a live CTFd instance.

Usage:
    python setup_ctfd.py --url http://localhost:8000 --token <CTFD_ADMIN_API_TOKEN>
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import mimetypes

CHALLENGES = [
    {
        "name": "Operation Cipherfall - Ep 01: The Quantum Beacon",
        "category": "Cryptography",
        "description": (
            "<h3>Mission Intelligence</h3>"
            "<p>We intercepted an emergency beacon transmitted from Vance's comm-link across a quantum-fluctuating channel.</p>"
            "<p>The transmission officer noted that the beacon does not use standard 26-letter Caesar rotation. "
            "Instead, it utilizes an extended <strong>Base-37 alphabet</strong> (<code>abcdefghijklmnopqrstuvwxyz0123456789_</code>) with <strong>alternating positional shifts</strong>:</p>"
            "<ul>"
            "<li>For <strong>even</strong> indices <em>i</em>: shift forward by <code>(i + 7) mod 37</code></li>"
            "<li>For <strong>odd</strong> indices <em>i</em>: shift backward by <code>(i * 3 + 5) mod 37</code></li>"
            "</ul>"
            "<p><em>(Braces <code>{</code> and <code>}</code> are unshifted delimiters).</em></p>"
            "<pre>mdj3{tgd7989ete90r0e0isn_oorb}</pre>"
            "<hr><strong>Attachment:</strong> Download <code>cipher.txt</code> below."
        ),
        "value": 50,
        "type": "standard",
        "state": "visible",
        "flags": ["flag{c43s4r_w0uld_b3_c0nfus3d}"],
        "tags": ["crypto", "classical", "alternating-caesar", "base37", "easy", "ai-resistant"],
        "hints": [
            {"content": "The alphabet has 37 characters: 'abcdefghijklmnopqrstuvwxyz0123456789_'. Braces '{' and '}' are delimiters and not shifted.", "cost": 0},
            {"content": "To invert the encryption at index i: if i is even, subtract (i + 7) mod 37. If i is odd, add (i * 3 + 5) mod 37.", "cost": 10},
            {"content": "In Python: new_idx = (idx - (i + 7)) % 37 if i % 2 == 0 else (idx + (i * 3 + 5)) % 37. Then map back to the alphabet.", "cost": 25}
        ],
        "dir": "01-broken-beacon",
        "files": ["cipher.txt"]
    },
    {
        "name": "Operation Cipherfall - Ep 02: Rendezvous in Paris",
        "category": "Cryptography",
        "description": (
            "<h3>Mission Intelligence</h3>"
            "<p>Operatives recovered an encrypted dispatch in Paris. The note bears a primer keyword: <code>PARIS</code>.</p>"
            "<p>Unlike standard Vigenère ciphers (which repeat the keyword endlessly and are easily cracked by statistical tools or AI), this dispatch was encrypted using the <strong>Autokey Cipher</strong>:</p>"
            "<ul>"
            "<li>The keystream begins with the primer: <code>P A R I S</code></li>"
            "<li>After the primer, the keystream is dynamically fed by the <strong>decrypted plaintext letters themselves</strong>!</li>"
            "</ul>"
            "<p><code>K_i = Primer_i (i &lt; 5), K_i = P_{i-5} (i &gt;= 5)</code></p>"
            "<pre>ulro{szeoqes_wspiyww_fm_pkgmxizbs}</pre>"
            "<hr><strong>Attachment:</strong> Download <code>cipher.txt</code> below."
        ),
        "value": 100,
        "type": "standard",
        "state": "visible",
        "flags": ["flag{autokey_defeats_ai_prompting}"],
        "tags": ["crypto", "classical", "autokey", "dynamic-keystream", "easy", "ai-resistant"],
        "hints": [
            {"content": "In an Autokey cipher, the key doesn't repeat. Instead, the plaintext characters are appended to the primer word to form the ongoing keystream.", "cost": 0},
            {"content": "Non-alphabetic characters (such as '{', '_', '}') are preserved and ignored in the key schedule. Decrypt letter by letter sequentially.", "cost": 10},
            {"content": "In Python: keep a list keystream = list('paris'). For each letter, p = (c - ord(keystream[k_idx]) + ord('a')) % 26, then keystream.append(chr(p + ord('a'))).", "cost": 25}
        ],
        "dir": "02-rendezvous-paris",
        "files": ["cipher.txt"]
    },
    {
        "name": "Operation Cipherfall - Ep 03: The Intercepted Droid",
        "category": "Cryptography",
        "description": (
            "<h3>Mission Intelligence</h3>"
            "<p>We recovered telemetry logs from a downed recon droid. "
            "The droid protected its message using an Affine Cipher, but with a twist that blinds standard AI decoders: "
            "It operates over a <strong>prime modulus of 37</strong>!</p>"
            "<p><code>Alphabet: abcdefghijklmnopqrstuvwxyz0123456789_ (m = 37)</code><br>"
            "<code>E(x) = (a * x + b) mod 37</code></p>"
            "<p>Because 37 is a prime number, <strong>every single non-zero integer</strong> <code>a in [1, 36]</code> has a valid modular inverse!</p>"
            "<pre>e7xp{hntv7uzmuzyk0hjkyimy_m_vdjzynz}</pre>"
            "<hr><strong>Attachments:</strong> Download <code>cipher.txt</code> and <code>affine.py</code> below."
        ),
        "value": 100,
        "type": "standard",
        "state": "visible",
        "flags": ["flag{m0dul4r_4r1thm3t1c_1s_sup3r10r}"],
        "tags": ["crypto", "affine", "base37", "modular-arithmetic", "easy", "ai-resistant"],
        "hints": [
            {"content": "The alphabet has 37 symbols (letters a-z, digits 0-9, and underscore). The delimiters '{' and '}' are unshifted.", "cost": 0},
            {"content": "Since 37 is prime, every a from 1 to 36 has a modular inverse: a_inv = pow(a, -1, 37). There are only 36 * 37 = 1332 total key pairs.", "cost": 10},
            {"content": "Test all pairs (a, b) in Python. The correct keys are a = 11, b = 23, with modular inverse pow(11, -1, 37) = 27.", "cost": 25}
        ],
        "dir": "03-intercepted-droid",
        "files": ["cipher.txt", "affine.py"]
    },
    {
        "name": "Operation Cipherfall - Ep 04: The XORd of Damocles",
        "category": "Cryptography",
        "description": (
            "<h3>Mission Intelligence</h3>"
            "<p>We intercepted an encrypted directive issued to the syndicate's perimeter security sentries. "
            "Rather than using a static repeating key (which standard statistical tools or AI decoders can easily solve), the sentries use a <strong>Linear Congruential Generator (LCG)</strong> to produce a dynamic byte-stream:</p>"
            "<p><code>S_{i+1} = (137 * S_i + 73) mod 256</code><br>"
            "<code>C_i = P_i ^ S_i</code></p>"
            "<p>The secret seed <code>S_0</code> is only a <strong>single 8-bit integer</strong> (<code>0 &lt;= S_0 &lt;= 255</code>)!</p>"
            "<pre>Ciphertext (Hex): 4cafc56a451b9b668ddbbe1b8100531d4ee7c782e73417a5124b43365b1b1c55b7</pre>"
            "<hr><strong>Attachments:</strong> Download <code>cipher.txt</code> and <code>xor.py</code> below."
        ),
        "value": 150,
        "type": "standard",
        "state": "visible",
        "flags": ["flag{lcg_prng_st4t3_is_t00_sm4ll}"],
        "tags": ["crypto", "symmetric", "prng", "lcg", "brute-force", "easy", "ai-resistant"],
        "hints": [
            {"content": "The keystream is generated by S_{i+1} = (137 * S_i + 73) mod 256. The seed S_0 is between 0 and 255.", "cost": 0},
            {"content": "You know the flag starts with 'flag{'. Write a Python script to iterate through all 256 possible seeds.", "cost": 10},
            {"content": "Seed 42 is the secret seed! Generate the keystream starting from 42 and XOR with the ciphertext bytes.", "cost": 25}
        ],
        "dir": "04-xord-of-damocles",
        "files": ["cipher.txt", "xor.py"]
    },
    {
        "name": "Operation Cipherfall - Ep 05: The Double Agent's Dilemma",
        "category": "Cryptography",
        "description": (
            "<h3>Mission Intelligence</h3>"
            "<p>Two corrupt syndicate dispatchers were intercepted relaying emergency evacuation alerts across an encrypted frequency. "
            "They encrypted both transmissions using a One-Time Pad scheme. However, in their panic, they reused the <strong>exact same keystream</strong> for both messages!</p>"
            "<p>Our signals analyst confirmed that all standard operational alerts on this frequency begin with the known header prefix: "
            "<code>OPERATION CIPHERFALL: </code></p>"
            "<pre>"
            "Ciphertext 1 (Hex):\n293c24353a203e7f1154722463173566221e2f78547f2f74337d267f347211307146762e252d31223f5421791e546228700b3f66446f5715\n\n"
            "Ciphertext 2 (Hex):\n25232c2a3a3a33101c3b7f2b7a0d3d7120654378211c2513327c25114272133f1436762f2f2124333e26577116267d2270145073250b2615"
            "</pre>"
            "<hr><strong>Attachments:</strong> Download <code>ciphertexts.txt</code> and <code>encrypt.py</code> below."
        ),
        "value": 150,
        "type": "standard",
        "state": "visible",
        "flags": ["flag{tw0_t1m3_p4d_c4n_n3v3r_b3_s4f3}"],
        "tags": ["crypto", "stream-cipher", "otp", "key-reuse", "two-time-pad", "easy", "ai-resistant"],
        "hints": [
            {"content": "A One-Time Pad is only secure if the key is used once. When key K is reused: C1 ^ C2 = P1 ^ P2.", "cost": 0},
            {"content": "You know the first 22 bytes of Message 1: 'OPERATION CIPHERFALL: '. XORing these known bytes with Ciphertext 1 immediately gives you the first 22 bytes of the flag!", "cost": 10},
            {"content": "XOR C1[:22] with b'OPERATION CIPHERFALL: ' reveals 'flag{tw0_t1m3_p4d_c4n_'. Complete message 1 is 'OPERATION CIPHERFALL: AGENT VANCE ESCAPED VIA SECTOR 04!'.", "cost": 25}
        ],
        "dir": "05-double-agent-otp",
        "files": ["ciphertexts.txt", "encrypt.py"]
    },
    {
        "name": "Operation Cipherfall - Ep 06: Protocol DH-9000",
        "category": "Cryptography",
        "description": (
            "<h3>Mission Intelligence</h3>"
            "<p>The syndicate's primary command satellite synchronizes session keys using a protocol designated <code>DH-9000</code>.</p>"
            "<p>Public parameters: <code>p = 19997, g = 5, A = 2058, B = 5125</code>.</p>"
            "<p>Once the shared secret <code>S = B^a mod p</code> was computed, the satellite encrypted the directive using: "
            "<code>Key = SHA256(str(S))</code></p>"
            "<pre>Encrypted Flag (Hex) = dcb3befd8907a8e142d9f6351d054d4c8f5810082a9600fba1259d9a115b57f1dea2</pre>"
            "<hr><strong>Attachments:</strong> Download <code>params.txt</code> and <code>dh.py</code> below."
        ),
        "value": 200,
        "type": "standard",
        "state": "visible",
        "flags": ["flag{dh_d1scr3t3_l0g_brut3_f0rc3d}"],
        "tags": ["crypto", "asymmetric", "diffie-hellman", "discrete-log", "sha256", "easy", "ai-resistant"],
        "hints": [
            {"content": "Alice computed A = pow(g, a, p). Find Alice's secret 'a' by looping from 1 to 19997 and checking if pow(5, a, 19997) == 2058.", "cost": 0},
            {"content": "Once 'a' is found, compute the shared secret S = pow(B, a, p). Derive the AES/XOR key using hashlib.sha256(str(S).encode()).digest().", "cost": 10},
            {"content": "Alice's secret is a = 13371, giving S = 18857. XOR the encrypted bytes with hashlib.sha256(b'18857').digest().", "cost": 25}
        ],
        "dir": "06-protocol-dh9000",
        "files": ["params.txt", "dh.py"]
    },
    {
        "name": "Operation Cipherfall - Ep 07: The Mastermind's Vault",
        "category": "Cryptography",
        "description": (
            "<h3>Mission Intelligence</h3>"
            "<p>The syndicate server key is protected by RSA-512 with modulus <code>N = p * q</code>.</p>"
            "<p>During forensic extraction of the server logs, we recovered the combined prime sum: <code>S = p + q</code>.</p>"
            "<p>In algebra, <code>(p - q)^2 = (p + q)^2 - 4*N</code>. Calculate the prime factors, find private key <code>d</code>, and decrypt the vault!</p>"
            "<hr><strong>Attachments:</strong> Download <code>rsa.txt</code> and <code>encrypt.py</code> below."
        ),
        "value": 200,
        "type": "standard",
        "state": "visible",
        "flags": ["flag{qu4dr4t1c_f0rmul4_br34ks_sum_rs4}"],
        "tags": ["crypto", "asymmetric", "rsa", "quadratic-formula", "easy", "ai-resistant"],
        "hints": [
            {"content": "You know N = p * q and S = p + q. In algebra, (p - q)^2 = (p + q)^2 - 4*N.", "cost": 0},
            {"content": "Use Python's built-in math.isqrt(S * S - 4 * N) to compute the exact difference: diff = p - q. Then p = (S + diff) // 2 and q = S - p.", "cost": 10},
            {"content": "Once p and q are separated: phi = (p - 1)*(q - 1), d = pow(e, -1, phi), and m = pow(c, d, N). Convert m to ASCII.", "cost": 25}
        ],
        "dir": "07-mastermind-vault",
        "files": ["rsa.txt", "encrypt.py"]
    },
    {
        "name": "Operation Cipherfall - Ep 08: Baby One-Round",
        "category": "Cryptography",
        "description": (
            "<h3>Mission Intelligence</h3>"
            "<p><em>(Inspired by ECSC 2024 / CryptoHack: 'It\\'s just one round of encryption. How hard can it be?')</em></p>"
            "<p>The syndicate developed a custom block cipher using AES S-Box, bitwise nibble permutations, and two round keys—limited to <strong>just one round</strong>.</p>"
            "<pre>Ciphertext (Hex): 0d1c145b4209c604e3d68f393de1d20ebe1598a36ddb48cf56795f1369e1c1a352</pre>"
            "<p>Trace the cipher in reverse and unlock their evacuation route!</p>"
            "<hr><strong>Attachments:</strong> Download <code>cipher.txt</code> and <code>chall.py</code> below."
        ),
        "value": 250,
        "type": "standard",
        "state": "visible",
        "flags": ["flag{spn_n1bbl3_sw4p_d3f34ts_llm}"],
        "tags": ["crypto", "block-cipher", "spn", "s-box", "nibble-swap", "easy", "ai-resistant"],
        "hints": [
            {"content": "A Substitution-Permutation Network (SPN) round consists of AddRoundKey, SubBytes, and Permutation. Decryption applies each inverse in reverse order.", "cost": 0},
            {"content": "Notice that swapping the high and low 4 bits (nibble swap) twice returns the original byte: swap_nibbles(swap_nibbles(b)) == b!", "cost": 10},
            {"content": "Decryption steps: 1) XOR ciphertext with ROUND_KEY_1. 2) Apply swap_nibbles. 3) Map through INV_SBOX = {SBOX[i]: i for i in range(256)}. 4) XOR with ROUND_KEY_0.", "cost": 25}
        ],
        "dir": "08-baby-one-round",
        "files": ["cipher.txt", "chall.py"]
    }
]

def make_request(url, token, method="GET", data=None, content_type="application/json"):
    headers = {
        "Authorization": f"Token {token}",
        "User-Agent": "CTFd-AutoDeployer/1.0"
    }
    if content_type:
        headers["Content-Type"] = content_type

    req_data = None
    if data is not None:
        if isinstance(data, dict):
            req_data = json.dumps(data).encode("utf-8")
        else:
            req_data = data

    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"[-] HTTP Error {e.code} on {url}: {error_body}")
        return None
    except Exception as e:
        print(f"[-] Network Error: {e}")
        return None

def upload_file(ctfd_url, token, challenge_id, filepath):
    filename = os.path.basename(filepath)
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    with open(filepath, "rb") as f:
        file_bytes = f.read()

    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(b'Content-Disposition: form-data; name="challenge_id"\r\n\r\n')
    body.extend(f"{challenge_id}\r\n".encode())
    
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(b'Content-Disposition: form-data; name="type"\r\n\r\n')
    body.extend(b"challenge\r\n")

    mime_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode())
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode())
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())

    url = f"{ctfd_url.rstrip('/')}/api/v1/files"
    res = make_request(url, token, method="POST", data=bytes(body), content_type=f"multipart/form-data; boundary={boundary}")
    return res

def deploy(ctfd_url, token):
    print(f"[*] Starting CTFd deployment to: {ctfd_url}")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    challenges_dir = os.path.join(script_dir, "challenges")

    for chall in CHALLENGES:
        print(f"\n[+] Deploying Challenge: {chall['name']}")
        payload = {
            "name": chall["name"],
            "category": chall["category"],
            "description": chall["description"],
            "value": chall["value"],
            "type": chall["type"],
            "state": chall["state"]
        }
        create_res = make_request(f"{ctfd_url.rstrip('/')}/api/v1/challenges", token, method="POST", data=payload)
        if not create_res or not create_res.get("success"):
            print(f"[-] Failed to create challenge: {chall['name']}")
            continue

        chall_id = create_res["data"]["id"]
        print(f"    Created challenge with ID: {chall_id}")

        for fl in chall["flags"]:
            flag_payload = {
                "challenge_id": chall_id,
                "content": fl,
                "type": "static",
                "data": ""
            }
            make_request(f"{ctfd_url.rstrip('/')}/api/v1/flags", token, method="POST", data=flag_payload)
            print(f"    Added Flag: {fl}")

        for tag in chall["tags"]:
            tag_payload = {"challenge_id": chall_id, "value": tag}
            make_request(f"{ctfd_url.rstrip('/')}/api/v1/tags", token, method="POST", data=tag_payload)

        for h in chall["hints"]:
            hint_payload = {
                "challenge_id": chall_id,
                "content": h["content"],
                "cost": h["cost"]
            }
            make_request(f"{ctfd_url.rstrip('/')}/api/v1/hints", token, method="POST", data=hint_payload)
            print(f"    Added Hint (Cost: {h['cost']} pts)")

        c_folder = os.path.join(challenges_dir, chall["dir"])
        for f in chall["files"]:
            f_path = os.path.join(c_folder, f)
            if os.path.exists(f_path):
                upload_file(ctfd_url, token, chall_id, f_path)
                print(f"    Uploaded File: {f}")
            else:
                print(f"    [!] Warning: File {f_path} not found.")

    print("\n[✔] All Operation Cipherfall AI-Resistant challenges successfully deployed to CTFd!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CTFd Automated Challenge Importer")
    parser.add_argument("--url", default="http://localhost:8000", help="CTFd URL (e.g. http://localhost:8000)")
    parser.add_argument("--token", required=True, help="CTFd Admin API Token (from Settings > Access Tokens)")
    args = parser.parse_args()
    deploy(args.url, args.token)
