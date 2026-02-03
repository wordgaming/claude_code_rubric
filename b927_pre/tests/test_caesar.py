import pytest
from cipher.caesar import encrypt, decrypt

@ pytest.mark.parametrize(
    "text, shift, expected",
    [
        ("ABC", 3, "DEF"),
        ("xyz", 2, "zab"),
        ("Hello, World!", 5, "Mjqqt, Btwqi!"),
        ("abc", 26, "abc"),
        ("abc", 52, "abc"),
    ],
)
def test_encrypt(text, shift, expected):
    assert encrypt(text, shift) == expected

@ pytest.mark.parametrize(
    "text, shift",
    [
        ("ABC", 3),
        ("xyz", 2),
        ("Hello, World!", 5),
    ],
)
def test_decrypt(text, shift):
    encrypted = encrypt(text, shift)
    assert decrypt(encrypted, shift) == text