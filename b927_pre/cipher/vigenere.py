def encrypt(text: str, key: str) -> str:
    """
    Encrypts the input text using the Vigenère cipher with the given key.
    Non-alphabet characters are left unchanged.
    """
    result = []
    key = key.upper()
    key_length = len(key)
    key_indices = [ord(k) - ord('A') for k in key]
    key_idx = 0

    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            shift = key_indices[key_idx % key_length]
            result.append(
                chr((ord(char) - ord(base) + shift) % 26 + ord(base))
            )
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

def decrypt(text: str, key: str) -> str:
    """
    Decrypts the input text using the Vigenère cipher with the given key.
    """
    result = []
    key = key.upper()
    key_length = len(key)
    key_indices = [ord(k) - ord('A') for k in key]
    key_idx = 0

    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            shift = key_indices[key_idx % key_length]
            result.append(
                chr((ord(char) - ord(base) - shift) % 26 + ord(base))
            )
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)