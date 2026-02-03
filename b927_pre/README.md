# Cipher Suite

A Python package implementing classic cryptographic ciphers:
- Caesar Cipher
- Vigenère Cipher

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

## Project Structure
```
.
├── cipher/
│   ├── __init__.py
│   ├── caesar.py
│   └── vigenere.py
├── tests/
│   ├── test_caesar.py
│   └── test_vigenere.py
├── Dockerfile
├── requirements.txt
└── setup.py
``` 