from fastapi import FastAPI, Request
from pydantic import BaseModel
import time

app = FastAPI()

class InterceptedMessage(BaseModel):
    content: str
    sender: str

class PublicKeyExchange(BaseModel):
    n: str
    e: int
    sender: str

# Store intercepted data
intercepted_messages = []
intercepted_keys = []

@app.post("/intercept_key_exchange")
async def intercept_key_exchange(key_data: PublicKeyExchange):
    """Intercept public key exchanges"""
    key_details = {
        "timestamp": time.time(),
        "sender": key_data.sender,
        "public_key": {"n": key_data.n, "e": key_data.e}
    }
    intercepted_keys.append(key_details)
    print(f"Intercepted key exchange from {key_data.sender}: n={key_data.n}, e={key_data.e}")
    return {"status": "Key exchange intercepted"}

@app.post("/intercept")
async def intercept_message(msg: InterceptedMessage):
    """Receive intercepted encrypted messages"""
    message_details = {
        "timestamp": time.time(),
        "sender": msg.sender,
        "ciphertext": msg.content
    }
    intercepted_messages.append(message_details)
    print(f"Intercepted message from {msg.sender}: Cipher={msg.content}")
    return {"status": "Message intercepted"}

if __name__ == "__main__":
    import uvicorn
    print("[Eve] Starting eavesdropping server...")
    uvicorn.run(app, host="127.0.0.1", port=8002)