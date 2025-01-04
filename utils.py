import secrets

def is_prime(n, k=128):
    """Miller-Rabin primality test."""
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = secrets.randbelow(n - 2) + 2 
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def mod_inverse(e, phi):
    """Calculate the modular multiplicative inverse."""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

def generate_prime(bits):
    """Generate a prime number with the specified number of bits."""
    while True:
        num = secrets.randbits(bits)
        num |= 1
        if is_prime(num):
            return num
