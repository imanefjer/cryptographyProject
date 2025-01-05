from utils import mod_inverse, generate_prime

class RSA:
    def __init__(self, key_size=2048, generate_keys=True):
        """Generate RSA keys."""
        self.key_size = key_size
        if generate_keys:
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

    def string_to_int(self, message: str) -> int:
        """Convert a string message to an integer."""
        return int.from_bytes(message.encode('utf-8'), byteorder='big')

    def int_to_string(self, message_int: int) -> str:
        """Convert an integer back to a string message."""
        return message_int.to_bytes((message_int.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

    def encrypt(self, message: str) -> int:
        """Encrypt a string message (ENC algorithm)."""
        message_int = self.string_to_int(message)
        if not 0 <= message_int < self.n:
            raise ValueError("Message must be within range [0, n-1]")
        return pow(message_int, self.e, self.n)

    def decrypt(self, ciphertext: int) -> str:
        """Decrypt a ciphertext and return the original string message (DEC algorithm)."""
        if not 0 <= ciphertext < self.n:
            raise ValueError("Ciphertext must be within range [0, n-1]")
        message_int = pow(ciphertext, self.d, self.n)
        return self.int_to_string(message_int)


if __name__ == "__main__":
    # Create an RSA instance with a larger key size
    rsa = RSA(2048)  
    
    # Example message (must be a string)
    message = "this is cryptography"
    
    # Encrypt the message
    ciphertext = rsa.encrypt(message)
    print(f"Original message: {message}")
    print(f"Encrypted message: {ciphertext}")
    
    # Decrypt the ciphertext
    decrypted = rsa.decrypt(ciphertext)
    print(f"Decrypted message: {decrypted}")
