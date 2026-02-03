# Cipher Suite

A Python package implementing classic and modern cryptographic ciphers:
- Caesar Cipher
- Vigenère Cipher
- RSA with OAEP Padding (PKCS#1 with SHA-256)

## Installation

```bash
pip install -e .
```

## Usage

### Caesar Cipher
```python
from cipher.caesar import encrypt, decrypt

# Encrypt a message
encrypted = encrypt("Hello, World!", 3)  # Shifts each letter by 3
print(encrypted)  # "Khoor, Zruog!"

# Decrypt a message
decrypted = decrypt(encrypted, 3)  # Shifts back by 3
print(decrypted)  # "Hello, World!"
```

### Vigenère Cipher
```python
from cipher.vigenere import encrypt, decrypt

# Encrypt a message
encrypted = encrypt("Hello, World!", "KEY")  # Uses "KEY" as the encryption key
print(encrypted)

# Decrypt a message
decrypted = decrypt(encrypted, "KEY")  # Must use the same key
print(decrypted)  # "Hello, World!"
```

### RSA with OAEP Padding
```python
from cipher.rsa import generate_keypair, encrypt, decrypt

# Generate a keypair (2048-bit by default)
public_key, private_key = generate_keypair(2048)

# Encrypt a message (supports arbitrary-length messages)
message = b"Hello, World! This is a secret message."
ciphertext = encrypt(message, public_key)

# Decrypt the message
decrypted = decrypt(ciphertext, private_key)
print(decrypted)  # b"Hello, World! This is a secret message."

# The implementation automatically handles messages longer than one block
long_message = b"A" * 10000  # 10KB message
ciphertext = encrypt(long_message, public_key)
decrypted = decrypt(ciphertext, private_key)
assert decrypted == long_message
```

#### RSA Features
- **PKCS#1 OAEP Padding**: Uses Optimal Asymmetric Encryption Padding with SHA-256 for enhanced security
- **Arbitrary-length messages**: Automatically splits long messages into blocks and recombines them
- **Secure key generation**: Uses Miller-Rabin primality testing for generating strong primes
- **Standard key sizes**: Supports 1024, 2048, 4096-bit keys (2048-bit recommended)

#### RSA Technical Details
- **Padding scheme**: PKCS#1 OAEP with SHA-256 hash function
- **Mask Generation Function**: MGF1 based on SHA-256
- **Public exponent**: e = 65537 (standard choice)
- **Block processing**: For 2048-bit RSA, each block can contain up to 190 bytes of plaintext
- **Randomization**: Each encryption uses a random seed, so encrypting the same message twice produces different ciphertexts

## Running Tests

The project uses pytest for testing. You can run tests in two ways:

1. Using Docker (recommended):
```bash
docker build -t cipher-suite .
docker run --rm cipher-suite
```

2. Directly with pytest:
```bash
pip install -e .
pytest
```

To run specific test files:
```bash
pytest tests/test_rsa.py      # Test RSA only
pytest tests/test_caesar.py   # Test Caesar cipher only
pytest tests/test_vigenere.py # Test Vigenère cipher only
```

## Project Structure
```
.
├── cipher/
│   ├── __init__.py
│   ├── caesar.py
│   ├── vigenere.py
│   └── rsa.py          # RSA with OAEP padding
├── tests/
│   ├── test_caesar.py
│   ├── test_vigenere.py
│   └── test_rsa.py     # RSA tests
├── Dockerfile
├── requirements.txt
└── setup.py
```

## Security Notes

### RSA Implementation
- This is an educational implementation demonstrating RSA with OAEP padding
- For production use, consider using established libraries like `cryptography` or `PyCryptodome`
- The implementation uses secure random number generation from `os.urandom()`
- Key generation uses Miller-Rabin primality testing with 5 rounds
- Minimum recommended key size is 2048 bits for adequate security

### Classical Ciphers
- Caesar and Vigenère ciphers are **not secure** for real-world use
- They are included for educational purposes only
- For actual encryption needs, use modern algorithms like RSA, AES, or ChaCha20
