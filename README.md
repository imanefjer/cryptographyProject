# RSA Chat Simulation

A real-time chat application demonstrating RSA encryption between two parties (Alice and Bob) with a modern, secure interface built using FastAPI, WebSocket, and TailwindCSS.

## Overview

This project simulates secure communication between two parties using RSA encryption. Each party (Alice and Bob) has their own:
- Public/Private key pair
- Web interface for sending/receiving messages
- WebSocket connection for real-time updates
- Server handling encryption/decryption

## Features

- **Real-time Communication**: Using WebSocket connections for instant message delivery
- **RSA Encryption**: Implementation of PKCS#1 v1.5 padding scheme
- **Modern UI**: Clean and responsive interface using TailwindCSS
- **Secure Key Exchange**: Automatic public key exchange between parties
- **Message Privacy**: All messages are encrypted before transmission

## Technical Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, JavaScript, TailwindCSS
- **Encryption**: Custom RSA implementation with PKCS#1 v1.5 padding
- **Real-time**: WebSocket protocol
- **Dependencies**: See requirements.txt

## How It Works

1. **Key Generation**:
   - Both Alice and Bob generate their RSA key pairs on server start
   - Keys are generated using the PKCS1_RSA class with 2048-bit key size

2. **Key Exchange**:
   - Public keys are automatically exchanged when sending the first message
   - Each party stores the other's public key for encryption

3. **Message Flow**:
   - User types a message in their interface
   - Message is encrypted using recipient's public key
   - Encrypted message is sent to recipient's server
   - Recipient's server decrypts using private key
   - Decrypted message is displayed in recipient's UI

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start Alice's server:
   ```bash
   python alice_server.py
   ```

3. Start Bob's server:
   ```bash
   python bob_server.py
   ```


4. Open Alice's interface: `http://localhost:8000`
5. Open Bob's interface: `http://localhost:8001`

## Security Notes

- This is a simulation for educational purposes
- Uses 2048-bit RSA keys for secure encryption
- Implements PKCS#1 v1.5 padding for additional security
- Real-world applications should use established cryptographic libraries

## Code Structure

- `alice_server.py`/`bob_server.py`: Server implementations
- `PKCS1_RSA.py`: RSA implementation with padding
- `utils.py`: Cryptographic utility functions
- Frontend templates: Modern UI implementations with TailwindCSS

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License