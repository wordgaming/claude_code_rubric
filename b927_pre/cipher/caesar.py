def encrypt(text: str, shift: int) -> str:
    """
    Encrypts the input text using a Caesar cipher with the given shift and 
    leaving the non-alphabet characters unchanged.
    """

    result = []
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            result.append(
                chr((ord(char) - ord(base) + shift) % 26 + ord(base))
            )
        else:
            result.append(char)
    return ''.join(result)

def decrypt(text: str, shift: int) -> str:
    """
    Decrypts the input text by reversing the shift.
    """
    return encrypt(text, -shift)