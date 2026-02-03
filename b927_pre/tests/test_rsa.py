"""
Tests for RSA encryption/decryption with OAEP padding.
"""

import pytest
from cipher.rsa import generate_keypair, encrypt, decrypt


def test_generate_keypair():
    """Test RSA keypair generation."""
    public_key, private_key = generate_keypair(1024)
    
    # Check that keys are tuples of two integers
    assert isinstance(public_key, tuple)
    assert isinstance(private_key, tuple)
    assert len(public_key) == 2
    assert len(private_key) == 2
    
    e, n_pub = public_key
    d, n_priv = private_key
    
    # Check that modulus is the same
    assert n_pub == n_priv
    
    # Check that e is 65537 (common choice)
    assert e == 65537
    
    # Check that n has approximately the right bit size
    assert n_pub.bit_length() >= 1000
    assert n_pub.bit_length() <= 1050


def test_encrypt_decrypt_short_message():
    """Test encryption and decryption of a short message."""
    public_key, private_key = generate_keypair(1024)
    
    message = b"Hello, World!"
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    
    assert decrypted == message


def test_encrypt_decrypt_empty_message():
    """Test that empty messages raise an error."""
    public_key, private_key = generate_keypair(1024)
    
    with pytest.raises(ValueError):
        encrypt(b"", public_key)


def test_encrypt_decrypt_long_message():
    """Test encryption and decryption of a message longer than one block."""
    public_key, private_key = generate_keypair(2048)
    
    # Create a message longer than one OAEP block
    # For 2048-bit RSA with SHA-256, max block size is 256 - 2*32 - 2 = 190 bytes
    message = b"A" * 500  # Multiple blocks needed
    
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    
    assert decrypted == message


def test_encrypt_decrypt_various_lengths():
    """Test encryption and decryption of messages of various lengths."""
    public_key, private_key = generate_keypair(2048)
    
    test_messages = [
        b"Short",
        b"A" * 50,
        b"B" * 150,
        b"C" * 200,
        b"D" * 400,
        b"E" * 1000,
    ]
    
    for message in test_messages:
        ciphertext = encrypt(message, public_key)
        decrypted = decrypt(ciphertext, private_key)
        assert decrypted == message, f"Failed for message of length {len(message)}"


def test_encrypt_decrypt_binary_data():
    """Test encryption and decryption of binary data."""
    public_key, private_key = generate_keypair(2048)
    
    # Test with various binary patterns
    message = bytes(range(256))
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    
    assert decrypted == message


def test_different_keys_produce_different_ciphertexts():
    """Test that different keys produce different ciphertexts."""
    public_key1, _ = generate_keypair(1024)
    public_key2, _ = generate_keypair(1024)
    
    message = b"Test message"
    
    ciphertext1 = encrypt(message, public_key1)
    ciphertext2 = encrypt(message, public_key2)
    
    # Different keys should produce different ciphertexts
    assert ciphertext1 != ciphertext2


def test_same_message_different_ciphertexts():
    """Test that encrypting the same message twice produces different ciphertexts (due to random padding)."""
    public_key, private_key = generate_keypair(1024)
    
    message = b"Test message"
    
    ciphertext1 = encrypt(message, public_key)
    ciphertext2 = encrypt(message, public_key)
    
    # Due to random seed in OAEP, ciphertexts should be different
    assert ciphertext1 != ciphertext2
    
    # But both should decrypt to the same message
    assert decrypt(ciphertext1, private_key) == message
    assert decrypt(ciphertext2, private_key) == message


def test_wrong_key_fails():
    """Test that decryption with wrong key fails or produces garbage."""
    public_key1, private_key1 = generate_keypair(1024)
    public_key2, private_key2 = generate_keypair(1024)
    
    message = b"Secret message"
    
    ciphertext = encrypt(message, public_key1)
    
    # Decrypting with wrong key should fail
    try:
        decrypted = decrypt(ciphertext, private_key2)
        # If it doesn't raise an error, it should at least produce different output
        assert decrypted != message
    except (ValueError, OverflowError):
        # Expected: decryption fails with wrong key
        pass


def test_corrupted_ciphertext_fails():
    """Test that corrupted ciphertext fails to decrypt."""
    public_key, private_key = generate_keypair(1024)
    
    message = b"Test message"
    ciphertext = encrypt(message, public_key)
    
    # Corrupt the ciphertext
    corrupted = bytearray(ciphertext)
    corrupted[10] ^= 0xFF  # Flip some bits
    corrupted = bytes(corrupted)
    
    # Decryption should fail
    with pytest.raises((ValueError, OverflowError)):
        decrypt(corrupted, private_key)


def test_unicode_text():
    """Test encryption and decryption of Unicode text."""
    public_key, private_key = generate_keypair(2048)
    
    # Test with various Unicode characters
    text = "Hello, 世界! 🌍 Привет мир"
    message = text.encode('utf-8')
    
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    
    assert decrypted == message
    assert decrypted.decode('utf-8') == text


def test_maximum_message_length():
    """Test encryption of very long messages."""
    public_key, private_key = generate_keypair(2048)
    
    # Test with a very long message (10KB)
    message = b"X" * 10000
    
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    
    assert decrypted == message
    assert len(decrypted) == 10000
