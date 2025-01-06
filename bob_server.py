from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from PKCS1_RSA import PKCS1_RSA
from typing import List
from fastapi.responses import FileResponse
import requests


app = FastAPI()
rsa = PKCS1_RSA(2048)

# Store received messages and peer's public key
received_messages = []
peer_public_key = {"n": None, "e": None}
active_connections: List[WebSocket] = []

@app.get("/")
async def serve_bob_html():
    return FileResponse("bob.html")

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

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except:
        manager.disconnect(websocket)

@app.post("/exchange_key")
async def exchange_key():
    """Exchange public keys with Alice"""
    try:
        response = requests.post(
            "http://localhost:8000/receive_key",
            json={"n": str(rsa.n), "e": rsa.e}
        )
        # Notify Eve
        requests.post(
            "http://localhost:8002/intercept_key_exchange",
            json={"n": str(rsa.n), "e": rsa.e, "sender": "Bob"}
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

        # Create temporary RSA instance with peer's public key
        peer_rsa = PKCS1_RSA(2048, generate_keys=False)
        peer_rsa.n = peer_public_key["n"]
        peer_rsa.e = peer_public_key["e"]
        
        # Encrypt message using peer's public key
        encrypted_message = peer_rsa.encrypt(message.content)
        
        # Send to Alice
        response = requests.post(
            "http://localhost:8000/receive",
            json={"content": str(encrypted_message)}
        )
        # Forward encrypted message to Eve
        requests.post(
    "http://localhost:8002/intercept",
    json={"content": str(encrypted_message), "sender": "Bob"}
)

        # here we are just making eve eavsdropping "man in the middle" wihtout going through proxy
        
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
        
        # Broadcast the new message to all connected WebSocket clients
        await manager.broadcast(decrypted_message)
        
        return {"status": "Message received"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001) 