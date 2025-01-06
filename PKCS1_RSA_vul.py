from utils import mod_inverse, generate_prime
import secrets



class PKCS1_RSA:
    def __init__(self, key_size=64, generate_keys=True):
        self.key_size = key_size
        if generate_keys:
            self.generate_keys()

    def generate_keys(self):
        p = generate_prime(self.key_size // 2)
        q = generate_prime(self.key_size // 2)
        while p == q:
            q = generate_prime(self.key_size // 2)
        self.n = p * q
        phi = (p - 1) * (q - 1)
        self.e = 65537
        self.d = mod_inverse(self.e, phi)

    def pad(self, message: bytes) -> bytes:
        max_len = (self.key_size // 8) - 4  # Account for padding
        if len(message) > max_len:
            message = message[:max_len]  # Truncate if too long
        return b'\x00\x02\x01\x00' + message

    def unpad(self, padded_message: bytes) -> bytes:
        if padded_message[0] != 0 or padded_message[1] != 2:
            raise ValueError("Invalid padding format")
        return padded_message[4:]

    def encrypt(self, message: str) -> int:
        message_bytes = message.encode('utf-8')
        padded_message = self.pad(message_bytes)
        message_int = int.from_bytes(padded_message, byteorder='big')
        return pow(message_int, self.e, self.n)

    def decrypt(self, ciphertext: int) -> str:
        byte_length = (self.key_size + 7) // 8
        message_int = pow(ciphertext, self.d, self.n)
        padded_message = message_int.to_bytes(byte_length, byteorder='big')
        message_bytes = self.unpad(padded_message)
        return message_bytes.decode('utf-8')