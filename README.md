# RSA Chat & Bleichenbacher Demo
> **A FastAPI-powered real-time chat showcasing RSA encryption (PKCS#1 v1.5) — complete with a Bleichenbacher padding oracle attack demonstration.**

## Overview
This repository contains a **fully working simulation** of two parties, **Alice** and **Bob**, securely exchanging messages using **RSA encryption** with PKCS\#1 v1.5 padding.  
A **third component**, the **Eve server**, intercepts communications to demonstrate how **improper RSA implementations** can be vulnerable to **Bleichenbacher’s chosen-ciphertext attack** (CCA).

### Key Highlights
1. **Two RSA Implementations**  
   - A **secure** version (`PKCS1_RSA`) that uses correct PKCS\#1 v1.5 padding checks.  
   - A **vulnerable** version (`PKCS1_RSA_vul`) that shows how weak padding can be exploited.
2. **Alice & Bob**  
   - Each runs a **FastAPI** server (port `8000` and `8001`) with a modern chat interface (HTML/JS) for sending/receiving encrypted messages in **real time** via WebSockets.
3. **Eve**  
   - A separate **FastAPI** server (port `8002`) that **eavesdrops** on ciphertexts and **public key** exchanges, demonstrating how an attacker can **intercept** messages.
4. **Bleichenbacher Attack**  
   - A **toy** `bleichenbacher_attack` function illustrating the basic flow of how an attacker might exploit PKCS\#1 v1.5 padding oracles to eventually recover plaintext **without** the private key.




## How to Run
1. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Alice**  
   ```bash
   python alice_server.py
   ```
   - Accessible at `http://127.0.0.1:8000`.

3. **Start Bob**  
   ```bash
   python bob_server.py
   ```
   - Accessible at `http://127.0.0.1:8001`.

4. **Start Eve (Eavesdropping Server)**  
   ```bash
   python eve_server.py
   ```
   - Runs on `localhost:8002` and logs intercepted keys & ciphertexts.

5. **Open Both Chat Interfaces**  
   - Visit `localhost:8000` in one browser tab (Alice).  
   - Visit `localhost:8001` in another browser tab (Bob).

6. **Send Messages**  
   - Each message is RSA-encrypted using the **recipient’s public key**, posted to the other’s endpoint, **intercepted** by Eve’s server, and finally **decrypted** by the recipient.

## Demonstration of Vulnerability
- The code includes a **toy** `bleichenbacher_attack(C, e, N, bob_oracle)` function, simulating how an attacker with access to a “padding oracle” might **incrementally recover** plaintext from a given RSA ciphertext.
- This is **not** a fully optimized real-world exploit but is enough to **prove** how small mistakes in PKCS\#1 v1.5 handling can compromise security.

## Why This Is Cool
- **Live RSA**: You see **actual RSA** key generation, encryption, and decryption happening.
- **Immediate Feedback**: The chat UI updates in **real time** via WebSockets.
- **Educational Attack**: Eve’s console elegantly logs how she could intercept keys & ciphertexts, demonstrating the risks of an **improper** RSA implementation.

## Important Notes
1. **For Educational Purposes Only**  
   This project **should not** be used as a production security solution. It is **deliberately** simplified and demonstrates vulnerabilities **on purpose**.
2. **Key Exchange**  
   We show a **basic** public key exchange for demonstration. Real-world RSA usage often **relies** on certificate-based PKI or other more sophisticated key-management approaches.
3. **PKCS\#1 v1.5 vs OAEP**  
   The recommended approach is **RSA-OAEP** in modern systems to avoid padding oracle attacks.

## Future Enhancements
- Implement a **complete** Bleichenbacher attack loop to fully recover plaintext.
- Add **stronger** side-channel or timing-based oracles to replicate real-world conditions.
- Add **robust** key Exchange Mechanisms.

 

---
**Enjoy exploring how real-time RSA can be both powerful and perilous when incorrectly implemented!**