from utils import mod_inverse, generate_prime
import secrets

class PKCS1_RSA:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.generate_keys()

    def generate_keys(self):
        """Generate public and private keys (GEN algorithm)."""
        # Generate two distinct primes
        p = generate_prime(self.key_size // 2)
        q = generate_prime(self.key_size // 2)
        while p == q:
            q = generate_prime(self.key_size // 2)

        # Calculate n and phi
        self.n = p * q
        phi = (p - 1) * (q - 1)

        # Commonly used value for e
        self.e = 65537 
        # Calculate private exponent d
        self.d = mod_inverse(self.e, phi)
        
        
    def pad(self, message: bytes) -> bytes:
        """PKCS#1 v1.5 padding."""
        max_length = (self.key_size // 8) - 11
        if len(message) > max_length:
            raise ValueError("Message too long.")
        
        # Calculate padding length to reach key size
        padding_length = (self.key_size // 8) - len(message) - 3  
        
        # Generate random non-zero padding bytes
        padding_bytes = bytes(secrets.choice(range(1, 256)) for _ in range(padding_length))

        # Format: 00 || 02 || PS || 00 || M
        padded_message = b'\x00\x02' + padding_bytes + b'\x00' + message
        return padded_message

    def unpad(self, padded_message: bytes) -> bytes:
        """Remove PKCS#1 v1.5 padding."""
        # Ensure minimum length and correct format
        if len(padded_message) != self.key_size // 8:
            padded_message = b'\x00' * ((self.key_size // 8) - len(padded_message)) + padded_message
            
        if padded_message[0] != 0 or padded_message[1] != 2:
            raise ValueError("Invalid padding format")
            
        # Find separator
        separator_index = padded_message.find(b'\x00', 2)
        if separator_index < 10:  # Minimum padding length for security
            raise ValueError("Invalid padding length")
            
        # Extract message
        return padded_message[separator_index + 1:]

    def encrypt(self, message: str) -> int:
        """Encrypt a string message."""
        message_bytes = message.encode('utf-8')
        padded_message = self.pad(message_bytes)
        message_int = int.from_bytes(padded_message, byteorder='big')
        return pow(message_int, self.e, self.n)

    def decrypt(self, ciphertext: int) -> str:
        """Decrypt a ciphertext back to string."""
        # Ensure the decrypted message has the correct length
        byte_length = self.key_size // 8
        message_int = pow(ciphertext, self.d, self.n)
        padded_message = message_int.to_bytes(byte_length, byteorder='big')
        
        message_bytes = self.unpad(padded_message)
        return message_bytes.decode('utf-8')

if __name__ == "__main__":
    rsa = PKCS1_RSA(2048)
    message = "this is cryptography"
    ciphertext = rsa.encrypt(message)
    print(f"Original message: {message}")
    print(f"Encrypted message: {ciphertext}")
    decrypted = rsa.decrypt(ciphertext)
    print(f"Decrypted message: {decrypted}")
   