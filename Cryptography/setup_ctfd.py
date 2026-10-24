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
        "name": "Civilization: The Firekeeper's Bone",
        "category": "Cryptography",
        "description": (
            "<h3>Historical Story: The Dawn of Writing</h3>"
            "<p>Long before computers, human civilization began around fire. Someone had to stay awake through the cold night to keep the fire burning. That was the first job anyone ever had. Soon after, people started writing things down — a mark on clay, a scratch on bone — so no one had to remember everything alone.</p>"
            "<p>You find an ancient bone carving from an early tribe. Instead of our modern 26-letter alphabet, it uses an alphabet of 37 symbols:<br><code>abcdefghijklmnopqrstuvwxyz0123456789_</code></p>"
            "<p>Each character was shifted forward or backward based on its position number <em>i</em>:</p>"
            "<ul>"
            "<li>For <strong>even</strong> positions <em>i</em> (0, 2, 4...): shift forward by <code>(i + 7) mod 37</code></li>"
            "<li>For <strong>odd</strong> positions <em>i</em> (1, 3, 5...): shift backward by <code>(i * 3 + 5) mod 37</code></li>"
            "</ul>"
            "<p><em>(The brackets <code>{</code> and <code>}</code> are not shifted. Capital letters keep their capital form).</em></p>"
            "<pre>mdj3qryw{hk2axbxihix4f4347wbdcsff}</pre>"
            "<p>Can you reverse the scratches and read the first message?</p>"
            "<hr><strong>Attachment:</strong> Download <code>cipher.txt</code> below."
        ),
        "value": 50,
        "type": "standard",
        "state": "visible",
        "flags": ["flagfall{c43s4r_w0uld_b3_c0nfus3d}"],
        "tags": ["civilization", "ancient-history", "classical-cipher", "base37", "easy"],
        "hints": [
            {"content": "The alphabet has 37 symbols in total: letters a to z, numbers 0 to 9, and the underscore '_'. Braces '{' and '}' stay where they are.", "cost": 0},
            {"content": "To undo the shift at position i: if i is even, subtract (i + 7) mod 37. If i is odd, add (i * 3 + 5) mod 37.", "cost": 10},
            {"content": "In Python: new_idx = (idx - (i + 7)) % 37 if i % 2 == 0 else (idx + (i * 3 + 5)) % 37. Then look up the character in the alphabet.", "cost": 25}
        ],
        "dir": "01-broken-beacon",
        "files": ["cipher.txt"]
    },
    {
        "name": "Civilization: The Diplomat's Oath",
        "category": "Cryptography",
        "description": (
            "<h3>Historical Story: Secret Messengers</h3>"
            "<p>As towns grew into countries, rulers needed to send secret messages across long distances. Simple ciphers that repeated the same secret password were too easy for enemy spies to break.</p>"
            "<p>In 1789, a messenger carried a secret letter to Paris. It was protected by an <strong>Autokey Cipher</strong>:</p>"
            "<ul>"
            "<li>The secret key begins with a starting word: <code>PARIS</code> (5 letters).</li>"
            "<li>After that, the key is made directly from the <strong>hidden message itself</strong>!</li>"
            "</ul>"
            "<p><code>K_i = Primer_i (i &lt; 5), K_i = P_{i-5} (i &gt;= 5)</code></p>"
            "<p>Because the key never repeats, each letter you solve unlocks the key for the next letter.</p>"
            "<pre>ulroxfwl{gztzves_wspiyww_fm_pkgmxizbs}</pre>"
            "<p>Can you decrypt the messenger's letter?</p>"
            "<hr><strong>Attachment:</strong> Download <code>cipher.txt</code> below."
        ),
        "value": 100,
        "type": "standard",
        "state": "visible",
        "flags": ["flagfall{autokey_defeats_ai_prompting}"],
        "tags": ["civilization", "messengers", "autokey", "dynamic-keystream", "easy"],
        "hints": [
            {"content": "The starting word 'PARIS' decrypts the first 5 letters. After that, each letter you uncover is added to the key list to unlock future letters.", "cost": 0},
            {"content": "Characters like '{', '_', and '}' are left alone and skipped by the key. Decrypt one letter at a time from left to right.", "cost": 10},
            {"content": "In Python: keep a list keystream = list('paris'). For each letter: p = (ord(c.lower()) - ord(keystream[k_idx])) % 26, then keystream.append(chr(p + ord('a'))).", "cost": 25}
        ],
        "dir": "02-rendezvous-paris",
        "files": ["cipher.txt"]
    },
    {
        "name": "Civilization: The Granary Ledger",
        "category": "Cryptography",
        "description": (
            "<h3>Historical Story: The First Walled Towns</h3>"
            "<p>People started living together in towns. Towns needed trust — so they built walls, made promises, and kept records of who owed what to whom.</p>"
            "<p>In the ruins of an ancient town's grain storehouse, you find an old tax record carved on a clay tablet. The town accountant scrambled the message using a simple math rule over a 37-symbol alphabet:</p>"
            "<p><code>Alphabet: abcdefghijklmnopqrstuvwxyz0123456789_ (m = 37)</code><br>"
            "<code>E(x) = (a * x + b) mod 37</code></p>"
            "<p>Because 37 is a prime number, every multiplier <code>a</code> from 1 to 36 has an exact reverse match (modular inverse).</p>"
            "<p>There are only <code>36 * 37 = 1,332</code> possible key pairs (a, b). A short Python script can test every single pair in less than a second!</p>"
            "<pre>e7xpex77{hntv7uzmuzyk0hjkyimy_m_vdjzynz}</pre>"
            "<p>Can you find the right keys and read the ledger?</p>"
            "<hr><strong>Attachments:</strong> Download <code>cipher.txt</code> and <code>affine.py</code> below."
        ),
        "value": 100,
        "type": "standard",
        "state": "visible",
        "flags": ["flagfall{m0dul4r_4r1thm3t1c_1s_sup3r10r}"],
        "tags": ["civilization", "ancient-towns", "affine", "base37", "modular-arithmetic", "easy"],
        "hints": [
            {"content": "The alphabet has 37 symbols: letters a-z, numbers 0-9, and the underscore '_'. Braces '{' and '}' are not changed.", "cost": 0},
            {"content": "Because 37 is prime, every number a from 1 to 36 can be inverted with Python: a_inv = pow(a, -1, 37). Loop through all 1,332 combinations of a and b.", "cost": 10},
            {"content": "The accountant's secret keys are a = 11 and b = 23. Invert the affine transformation using pow(11, -1, 37) = 27: x = (27 * (y - 23)) % 37.", "cost": 25}
        ],
        "dir": "03-intercepted-droid",
        "files": ["cipher.txt", "affine.py"]
    },
    {
        "name": "Civilization: The Sentry's Clockwork",
        "category": "Cryptography",
        "description": (
            "<h3>Historical Story: The Imperial Gate</h3>"
            "<p>Towns grew into massive empires — too big for one person to watch alone. Rulers had to trust guards they would never meet, guarding fortress gates they could never personally check.</p>"
            "<p>At an ancient stone fortress, an automated bronze clockwork machine was built to generate daily passcodes for the sentry guards. It used a simple math formula called an LCG:</p>"
            "<p><code>S_{i+1} = (137 * S_i + 73) mod 256</code><br>"
            "<code>C_i = P_i ^ S_i</code></p>"
            "<p>The entire machine was started with a single 8-bit seed number (<code>S_0</code>), which is just an integer between 0 and 255.</p>"
            "<p>Whoever built the machine thought 256 combinations was enough to keep the gates safe. Write a quick Python script to test all 256 starting seeds and unlock the sentry's message!</p>"
            "<pre>Ciphertext (Hex): 4cafc56a5816946da9c7af12b92f52071dcc87a9ba337b8e4b084331061f2f4aa75728c1a3</pre>"
            "<hr><strong>Attachments:</strong> Download <code>cipher.txt</code> and <code>xor.py</code> below."
        ),
        "value": 150,
        "type": "standard",
        "state": "visible",
        "flags": ["flagfall{lcg_prng_st4t3_is_t00_sm4ll}"],
        "tags": ["civilization", "ancient-empires", "symmetric", "prng", "lcg", "brute-force", "easy"],
        "hints": [
            {"content": "The clockwork steps through numbers using S_{i+1} = (137 * S_i + 73) mod 256. The seed S_0 is a single number from 0 to 255.", "cost": 0},
            {"content": "You know the flag starts with 'flagfall{'. Loop through all 256 possible seeds in Python and see which one decrypts to readable text.", "cost": 10},
            {"content": "The starting seed was 42. Generate the key numbers starting from 42 and XOR each byte with the ciphertext bytes.", "cost": 25}
        ],
        "dir": "04-xord-of-damocles",
        "files": ["cipher.txt", "xor.py"]
    },
    {
        "name": "Civilization: The Transatlantic Cable",
        "category": "Cryptography",
        "description": (
            "<h3>Historical Story: The Undersea Cable</h3>"
            "<p>In the late industrial age, long copper cables were laid across the bottom of the ocean to connect continents by telegraph. To send secret dispatches, military stations used a <strong>One-Time Pad</strong> — a stream of random key bytes.</p>"
            "<p>A One-Time Pad is mathematically impossible to break, but only if the key is used <strong>once</strong>. During an emergency, a nervous telegraph operator made a critical mistake: they reused the <strong>exact same key tape</strong> to encrypt two different messages!</p>"
            "<p>When a key is reused:<br><code>C1 ^ C2 = P1 ^ P2</code></p>"
            "<p>Standard operational alerts on this telegraph line always begin with the known header prefix: <code>OPERATION CIPHERFALL: </code></p>"
            "<pre>"
            "Ciphertext 1 (Hex):\n293c243527352523355434790f3c743f751e3c785e7f22732b113a1320723c1c27131a2077276338224c372e27413f29382038627f44054c\n\n"
            "Ciphertext 2 (Hex):\n25232c2a272f284c383b397616267c28776550782b1c28142a10397d56723e1342631a217d2b7629233e41262f332023383f57771e20744c"
            "</pre>"
            "<p>Use XOR with the known starting words to reveal the key and uncover the secret messages!</p>"
            "<hr><strong>Attachments:</strong> Download <code>ciphertexts.txt</code> and <code>encrypt.py</code> below."
        ),
        "value": 150,
        "type": "standard",
        "state": "visible",
        "flags": ["flagfall{tw0_t1m3_p4d_c4n_n3v3r_b3_s4f3}"],
        "tags": ["civilization", "telegraph", "stream-cipher", "otp", "key-reuse", "two-time-pad", "easy"],
        "hints": [
            {"content": "A One-Time Pad is only secure if the key is never reused. When key K is reused: C1 ^ C2 = P1 ^ P2.", "cost": 0},
            {"content": "You know the first 22 characters of Message 1 are 'OPERATION CIPHERFALL: '. XORing this known text with Ciphertext 1 reveals the first 22 bytes of the key!", "cost": 10},
            {"content": "XOR C1[:22] with b'OPERATION CIPHERFALL: ' reveals 'flagfall{tw0_t1m3_p4d_c4'. Complete message 1 is 'OPERATION CIPHERFALL: AGENT VANCE ESCAPED VIA SECTOR 04!'.", "cost": 25}
        ],
        "dir": "05-double-agent-otp",
        "files": ["ciphertexts.txt", "encrypt.py"]
    },
    {
        "name": "Civilization: The Vanguard Satellite",
        "category": "Cryptography",
        "description": (
            "<h3>Historical Story: The Early Space Age</h3>"
            "<p>In the 20th century, civilization reached into space. Two scientific satellites orbiting on opposite sides of Earth needed to agree on a secret key over open radio signals without enemy ground stations stealing it.</p>"
            "<p>They used the <strong>Diffie-Hellman Key Exchange</strong> with small numbers:</p>"
            "<ul>"
            "<li>Prime modulus: <code>p = 19997</code></li>"
            "<li>Base number: <code>g = 5</code></li>"
            "<li>Alice public key: <code>A = 2058</code> (g^a mod p)</li>"
            "<li>Bob public key: <code>B = 5125</code> (g^b mod p)</li>"
            "</ul>"
            "<p>Once Alice found her secret number <em>a</em>, the satellites computed their shared secret number: <code>S = B^a mod p</code></p>"
            "<p>They converted S to text and hashed it with SHA-256 to create the encryption key: <code>Key = SHA256(str(S))</code></p>"
            "<pre>Encrypted Flag (Hex) = dcb3befd9402acd25d8ced090b074a1ca207545c2a9842e98a74b089551a6ba48aadbca9961e</pre>"
            "<p>Because p = 19997 is small, you can find Alice's secret number <em>a</em> with a simple Python loop from 1 to 19997!</p>"
            "<hr><strong>Attachments:</strong> Download <code>params.txt</code> and <code>dh.py</code> below."
        ),
        "value": 200,
        "type": "standard",
        "state": "visible",
        "flags": ["flagfall{dh_d1scr3t3_l0g_brut3_f0rc3d}"],
        "tags": ["civilization", "space-satellites", "asymmetric", "diffie-hellman", "discrete-log", "sha256", "easy"],
        "hints": [
            {"content": "Alice computed A = pow(5, a, 19997) == 2058. Loop through all numbers a from 1 to 19997 in Python until you find the match.", "cost": 0},
            {"content": "Once you find Alice's secret number a, compute the shared secret S = pow(B, a, p). Then compute key = hashlib.sha256(str(S).encode()).digest().", "cost": 10},
            {"content": "Alice's secret is a = 13371, giving S = 18857. XOR the encrypted bytes with hashlib.sha256(b'18857').digest() to get the flag.", "cost": 25}
        ],
        "dir": "06-protocol-dh9000",
        "files": ["params.txt", "dh.py"]
    },
    {
        "name": "Civilization: The Digital Gold Vault",
        "category": "Cryptography",
        "description": (
            "<h3>Historical Story: The Digital Gold Vault</h3>"
            "<p>As civilization moved from gold coins to computers, banks needed a way to lock vaults using math instead of physical keys.</p>"
            "<p>A bank vault is locked with RSA encryption. The lock uses a large public number <code>N = p * q</code>, where <code>p</code> and <code>q</code> are two secret prime numbers. It also uses the public exponent <code>e = 65537</code>. Normally, finding <code>p</code> and <code>q</code> from <code>N</code> takes thousands of years.</p>"
            "<p>However, an engineer made a simple mistake: they wrote down the <strong>sum</strong> of the two secret primes in a maintenance note: <code>S = p + q</code></p>"
            "<p>With simple school algebra, you can find the two primes without breaking a sweat: <code>(p - q)^2 = (p + q)^2 - 4*N = S^2 - 4*N</code></p>"
            "<p>Using Python's <code>math.isqrt()</code>, you can find the difference (p - q), uncover p and q, and unlock the vault!</p>"
            "<hr><strong>Attachments:</strong> Download <code>rsa.txt</code> and <code>encrypt.py</code> below."
        ),
        "value": 200,
        "type": "standard",
        "state": "visible",
        "flags": ["flagfall{qu4dr4t1c_f0rmul4_br34ks_sum_rs4}"],
        "tags": ["civilization", "digital-banking", "asymmetric", "rsa", "quadratic-formula", "easy"],
        "hints": [
            {"content": "The bank thought the lock was unbreakable because N is huge. But knowing the sum S = p + q makes finding the secret primes easy with simple math: (p - q)^2 = S^2 - 4*N.", "cost": 0},
            {"content": "Find the difference between the primes: diff = math.isqrt(S * S - 4 * N). Then p = (S + diff) // 2 and q = S - p.", "cost": 10},
            {"content": "After finding p and q, compute phi = (p - 1) * (q - 1). Then find private key d = pow(e, -1, phi), and decrypt with m = pow(c, d, N). Finally, convert number m to text with bytes.fromhex(hex(m)[2:]).decode().", "cost": 25}
        ],
        "dir": "07-mastermind-vault",
        "files": ["rsa.txt", "encrypt.py"]
    },
    {
        "name": "Civilization: The Connected World",
        "category": "Cryptography",
        "description": (
            "<h3>Historical Story: The Global Internet</h3>"
            "<p>Today, everything in human civilization is connected. Phones, computers, and servers all talk across thousands of miles of glass fiber cables.</p>"
            "<p>To send data quickly, network engineers built an encryption program that scrambles messages in four steps:</p>"
            "<ol>"
            "<li>Add round key 0 (using XOR)</li>"
            "<li>Replace each byte using a lookup table (S-Box)</li>"
            "<li>Swap the first 4 bits and last 4 bits of each byte (nibble swap)</li>"
            "<li>Add round key 1 (using XOR)</li>"
            "</ol>"
            "<p>Real modern ciphers (like AES) repeat these steps 10 or more times to keep data safe. But to make this network run faster, the engineers only ran the steps <strong>one single time</strong>!</p>"
            "<p>Because it only ran once, you can undo each step one by one in reverse order to read the secret message.</p>"
            "<pre>Ciphertext (Hex): 0d1c145bd240431e7e104690697ba290cc1cb7ca11114eaee3a363ee7a4ad4315d1c04cebf</pre>"
            "<hr><strong>Attachments:</strong> Download <code>cipher.txt</code> and <code>chall.py</code> below."
        ),
        "value": 250,
        "type": "standard",
        "state": "visible",
        "flags": ["flagfall{spn_n1bbl3_sw4p_d3f34ts_llm}"],
        "tags": ["civilization", "internet", "block-cipher", "spn", "s-box", "easy"],
        "hints": [
            {"content": "Because the cipher only ran for 1 round, you can decrypt the message by running the 4 steps backwards.", "cost": 0},
            {"content": "Swapping the first and last 4 bits of a byte twice puts it right back to normal. So swapping is its own reverse!", "cost": 10},
            {"content": "Decryption steps: 1) XOR ciphertext with ROUND_KEY_1. 2) Swap nibbles on each byte. 3) Reverse the S-Box lookup: INV_SBOX = {SBOX[i]: i for i in range(256)}. 4) XOR with ROUND_KEY_0.", "cost": 25}
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
