from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from RSA import RSA

app = FastAPI()
rsa = RSA(2048)

# Store received messages and peer's public key
received_messages = []
peer_public_key = {"n": None, "e": None}

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    content: str

class PublicKey(BaseModel):
    n: str
    e: int

@app.post("/exchange_key")
async def exchange_key():
    """Exchange public keys with Alice"""
    try:
        response = requests.post(
            "http://localhost:8000/receive_key",
            json={"n": str(rsa.n), "e": rsa.e}
        )
        if response.status_code == 200:
            key_data = response.json()
            peer_public_key["n"] = int(key_data["n"])
            peer_public_key["e"] = int(key_data["e"])
            return {"status": "Key exchange successful"}
        raise HTTPException(status_code=500, detail="Key exchange failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/receive_key")
async def receive_key(key: PublicKey):
    """Receive public key from Alice"""
    peer_public_key["n"] = int(key.n)
    peer_public_key["e"] = key.e
    return {"n": str(rsa.n), "e": rsa.e}

@app.post("/send")
async def send_message(message: Message):
    try:
        # Ensure we have peer's public key
        if peer_public_key["n"] is None or peer_public_key["e"] is None:
            await exchange_key()

        # Convert message to integer and encrypt using peer's public key
        message_int = rsa.string_to_int(message.content)
        encrypted_message = pow(message_int, peer_public_key["e"], peer_public_key["n"])
        
        # Send to Alice
        response = requests.post(
            "http://localhost:8000/receive",
            json={"content": str(encrypted_message)}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to send message to Alice")
        
        return {"status": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/receive")
async def receive_message(message: Message):
    try:
        if not message.content:  # Handle empty content
            return {"status": "No message to decrypt"}
            
        # Decrypt using our private key
        decrypted_message = rsa.decrypt(int(message.content))
        received_messages.append(decrypted_message)
        return {"status": "Message received"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages")
async def get_messages():
    """Endpoint for clients to poll for new messages"""
    return {"messages": received_messages} 