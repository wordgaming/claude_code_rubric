import pytest
from cipher.vigenere import encrypt, decrypt

@ pytest.mark.parametrize(
    "text, key, expected",
    [
        ("ATTACKATDAWN", "LEMON", "LXFOPVEFRNHR"),
        ("attack at dawn", "LEMON", "lxfopv ef rnhr"),
        ("Hello, World!", "KEY", "Rijvs, Uyvjn!"),
    ],
)
def test_encrypt(text, key, expected):
    assert encrypt(text, key) == expected


@ pytest.mark.parametrize(
    "text, key",
    [
        ("ATTACKATDAWN", "LEMON"),
        ("Hello, World!", "KEY"),
    ],
)
def test_decrypt(text, key):
    encrypted = encrypt(text, key)
    assert decrypt(encrypted, key) == text