"""
RSA encryption/decryption with PKCS#1 OAEP padding using SHA-256.
Supports arbitrary-length messages through block-based processing.
"""

import os
import hashlib
import math
from typing import Tuple


def _is_prime(n: int, k: int = 5) -> bool:
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = 2 + os.urandom(1)[0] % (n - 3)
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


def _generate_prime(bit_size: int) -> int:
    """Generate a random prime number of specified bit size."""
    while True:
        # Generate random odd number
        num = os.urandom(bit_size // 8)
        num = int.from_bytes(num, 'big')
        # Set MSB and LSB to ensure correct bit size and odd number
        num |= (1 << (bit_size - 1)) | 1
        
        if _is_prime(num):
            return num


def _extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean Algorithm. Returns (gcd, x, y) where ax + by = gcd."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = _extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def _mod_inverse(a: int, m: int) -> int:
    """Compute modular multiplicative inverse of a modulo m."""
    gcd, x, _ = _extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m


def generate_keypair(bit_size: int = 2048) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generate RSA keypair.
    
    Args:
        bit_size: Size of the modulus in bits (default 2048)
    
    Returns:
        ((e, n), (d, n)): Public key and private key as tuples
    """
    # Generate two distinct primes
    p = _generate_prime(bit_size // 2)
    q = _generate_prime(bit_size // 2)
    while p == q:
        q = _generate_prime(bit_size // 2)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e = 65537 (common choice)
    e = 65537
    
    # Compute d = e^(-1) mod phi
    d = _mod_inverse(e, phi)
    
    return ((e, n), (d, n))


def _mgf1(seed: bytes, length: int, hash_func=hashlib.sha256) -> bytes:
    """
    Mask Generation Function based on SHA-256.
    
    Args:
        seed: Seed from which mask is generated
        length: Intended length of the mask in bytes
        hash_func: Hash function to use (default SHA-256)
    
    Returns:
        Mask of specified length
    """
    h_len = hash_func().digest_size
    if length > (2**32) * h_len:
        raise ValueError("Mask too long")
    
    T = b""
    counter = 0
    while len(T) < length:
        C = counter.to_bytes(4, 'big')
        T += hash_func(seed + C).digest()
        counter += 1
    
    return T[:length]


def _xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings of equal length."""
    return bytes(x ^ y for x, y in zip(a, b))


def _oaep_encode(message: bytes, k: int, label: bytes = b"") -> bytes:
    """
    OAEP encoding with SHA-256.
    
    Args:
        message: Message to encode
        k: Length of modulus in bytes
        label: Optional label (default empty)
    
    Returns:
        Encoded message of length k
    """
    hash_func = hashlib.sha256
    h_len = hash_func().digest_size
    
    # Check message length
    max_msg_len = k - 2 * h_len - 2
    if len(message) > max_msg_len:
        raise ValueError(f"Message too long for OAEP encoding (max {max_msg_len} bytes)")
    
    # Compute lHash
    l_hash = hash_func(label).digest()
    
    # Padding string PS
    ps_len = k - len(message) - 2 * h_len - 2
    ps = b'\x00' * ps_len
    
    # Data block DB = lHash || PS || 0x01 || M
    db = l_hash + ps + b'\x01' + message
    
    # Generate random seed
    seed = os.urandom(h_len)
    
    # dbMask = MGF(seed, k - hLen - 1)
    db_mask = _mgf1(seed, k - h_len - 1)
    
    # maskedDB = DB ⊕ dbMask
    masked_db = _xor_bytes(db, db_mask)
    
    # seedMask = MGF(maskedDB, hLen)
    seed_mask = _mgf1(masked_db, h_len)
    
    # maskedSeed = seed ⊕ seedMask
    masked_seed = _xor_bytes(seed, seed_mask)
    
    # EM = 0x00 || maskedSeed || maskedDB
    em = b'\x00' + masked_seed + masked_db
    
    return em


def _oaep_decode(encoded: bytes, k: int, label: bytes = b"") -> bytes:
    """
    OAEP decoding with SHA-256.
    
    Args:
        encoded: Encoded message of length k
        k: Length of modulus in bytes
        label: Optional label (default empty)
    
    Returns:
        Decoded message
    """
    hash_func = hashlib.sha256
    h_len = hash_func().digest_size
    
    # Check encoded message length
    if len(encoded) != k or k < 2 * h_len + 2:
        raise ValueError("Decoding error: invalid encoded message length")
    
    # Split EM = Y || maskedSeed || maskedDB
    y = encoded[0]
    masked_seed = encoded[1:h_len + 1]
    masked_db = encoded[h_len + 1:]
    
    # seedMask = MGF(maskedDB, hLen)
    seed_mask = _mgf1(masked_db, h_len)
    
    # seed = maskedSeed ⊕ seedMask
    seed = _xor_bytes(masked_seed, seed_mask)
    
    # dbMask = MGF(seed, k - hLen - 1)
    db_mask = _mgf1(seed, k - h_len - 1)
    
    # DB = maskedDB ⊕ dbMask
    db = _xor_bytes(masked_db, db_mask)
    
    # Compute lHash
    l_hash = hash_func(label).digest()
    
    # Split DB = lHash' || PS || 0x01 || M
    l_hash_prime = db[:h_len]
    
    # Check lHash
    if l_hash != l_hash_prime:
        raise ValueError("Decoding error: label hash mismatch")
    
    # Find 0x01 separator
    separator_index = -1
    for i in range(h_len, len(db)):
        if db[i] == 0x01:
            separator_index = i
            break
        elif db[i] != 0x00:
            raise ValueError("Decoding error: invalid padding")
    
    if separator_index == -1:
        raise ValueError("Decoding error: no 0x01 separator found")
    
    # Extract message
    message = db[separator_index + 1:]
    
    # Check Y
    if y != 0:
        raise ValueError("Decoding error: invalid first byte")
    
    return message


def encrypt(message: bytes, public_key: Tuple[int, int]) -> bytes:
    """
    Encrypt message using RSA with OAEP padding.
    Handles arbitrary-length messages by splitting into blocks.
    
    Args:
        message: Message to encrypt (bytes)
        public_key: Public key (e, n)
    
    Returns:
        Encrypted message (bytes)
    """
    e, n = public_key
    k = (n.bit_length() + 7) // 8  # Modulus length in bytes
    
    # Calculate maximum message length per block
    h_len = hashlib.sha256().digest_size
    max_block_size = k - 2 * h_len - 2
    
    if len(message) == 0:
        raise ValueError("Message cannot be empty")
    
    # Split message into blocks
    blocks = []
    for i in range(0, len(message), max_block_size):
        block = message[i:i + max_block_size]
        blocks.append(block)
    
    # Encrypt each block
    encrypted_blocks = []
    for block in blocks:
        # OAEP encode
        em = _oaep_encode(block, k)
        
        # Convert to integer
        m = int.from_bytes(em, 'big')
        
        # RSA encryption: c = m^e mod n
        c = pow(m, e, n)
        
        # Convert back to bytes (fixed length k)
        c_bytes = c.to_bytes(k, 'big')
        encrypted_blocks.append(c_bytes)
    
    # Prepend number of blocks (4 bytes) and concatenate all encrypted blocks
    num_blocks = len(encrypted_blocks).to_bytes(4, 'big')
    return num_blocks + b''.join(encrypted_blocks)


def decrypt(ciphertext: bytes, private_key: Tuple[int, int]) -> bytes:
    """
    Decrypt ciphertext using RSA with OAEP padding.
    Handles multi-block messages.
    
    Args:
        ciphertext: Encrypted message (bytes)
        private_key: Private key (d, n)
    
    Returns:
        Decrypted message (bytes)
    """
    d, n = private_key
    k = (n.bit_length() + 7) // 8  # Modulus length in bytes
    
    # Extract number of blocks
    if len(ciphertext) < 4:
        raise ValueError("Invalid ciphertext: too short")
    
    num_blocks = int.from_bytes(ciphertext[:4], 'big')
    ciphertext = ciphertext[4:]
    
    # Check ciphertext length
    if len(ciphertext) != num_blocks * k:
        raise ValueError("Invalid ciphertext: incorrect length")
    
    # Decrypt each block
    decrypted_blocks = []
    for i in range(num_blocks):
        # Extract block
        c_bytes = ciphertext[i * k:(i + 1) * k]
        
        # Convert to integer
        c = int.from_bytes(c_bytes, 'big')
        
        # RSA decryption: m = c^d mod n
        m = pow(c, d, n)
        
        # Convert back to bytes
        em = m.to_bytes(k, 'big')
        
        # OAEP decode
        block = _oaep_decode(em, k)
        decrypted_blocks.append(block)
    
    # Concatenate all decrypted blocks
    return b''.join(decrypted_blocks)
