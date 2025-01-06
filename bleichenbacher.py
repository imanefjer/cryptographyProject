def bleichenbacher_attack(C, e, N, bob_oracle):
    """
    C: intercepted ciphertext (integer)
    e, N: RSA public key components
    bob_oracle: function that returns True if 'C_prime' decrypts with valid PKCS#1 v1.5 padding

    Returns:
        M (int) -- the recovered plaintext when the interval collapses
    """

    # Step 0: Compute key length in bytes
    k = (N.bit_length() + 7) // 8
    # PKCS#1 v1.5 boundary
    B = 2 ** (8 * (k - 2))

    # Initial bounds for the plaintext
    lower = 2 * B
    upper = 3 * B - 1

    # Step 1: Find s1 that yields valid padding
    s = 1
    while True:
        C_prime = (C * pow(s, e, N)) % N
        if bob_oracle(C_prime):
            break
        s += 1

    # Suppose we found s1 => C_prime is valid => M' in [2B, 3B).
    # M' = (M * s1) mod N => M = M' * inv(s1) mod N (in a real scenario).

    # Step 2: In real attack, refine [lower, upper] repeatedly by finding new s_i
    while lower < upper:
        # Real code would:
        #   1) find next s_i with valid padding
        #   2) narrow lower/upper
        break

    # If lower == upper, we've found M exactly.
    M = lower
    return M
