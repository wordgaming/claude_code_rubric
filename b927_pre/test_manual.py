"""
Simple test script to verify RSA implementation.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cipher.rsa import generate_keypair, encrypt, decrypt

def test_basic_functionality():
    """Test basic RSA encryption and decryption."""
    print("Testing RSA implementation...")
    
    # Test 1: Generate keypair
    print("\n1. Generating 1024-bit RSA keypair...")
    public_key, private_key = generate_keypair(1024)
    e, n = public_key
    d, n_priv = private_key
    print(f"   Public key: e={e}, n={n.bit_length()} bits")
    print(f"   Private key: d={d.bit_length()} bits")
    assert n == n_priv, "Modulus mismatch!"
    print("   ✓ Keypair generated successfully")
    
    # Test 2: Short message
    print("\n2. Testing short message encryption...")
    message = b"Hello, World!"
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    assert decrypted == message, f"Decryption failed! Got {decrypted}"
    print(f"   Original:  {message}")
    print(f"   Decrypted: {decrypted}")
    print("   ✓ Short message test passed")
    
    # Test 3: Long message (multiple blocks)
    print("\n3. Testing long message encryption (500 bytes)...")
    long_message = b"A" * 500
    ciphertext = encrypt(long_message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    assert decrypted == long_message, "Long message decryption failed!"
    print(f"   Message length: {len(long_message)} bytes")
    print(f"   Ciphertext length: {len(ciphertext)} bytes")
    print(f"   Decrypted length: {len(decrypted)} bytes")
    print("   ✓ Long message test passed")
    
    # Test 4: Binary data
    print("\n4. Testing binary data encryption...")
    binary_data = bytes(range(256))
    ciphertext = encrypt(binary_data, public_key)
    decrypted = decrypt(ciphertext, private_key)
    assert decrypted == binary_data, "Binary data decryption failed!"
    print(f"   Binary data length: {len(binary_data)} bytes")
    print("   ✓ Binary data test passed")
    
    # Test 5: Randomization (same message produces different ciphertexts)
    print("\n5. Testing OAEP randomization...")
    message = b"Test message"
    ciphertext1 = encrypt(message, public_key)
    ciphertext2 = encrypt(message, public_key)
    assert ciphertext1 != ciphertext2, "Ciphertexts should be different!"
    decrypted1 = decrypt(ciphertext1, private_key)
    decrypted2 = decrypt(ciphertext2, private_key)
    assert decrypted1 == message and decrypted2 == message, "Decryption failed!"
    print("   ✓ OAEP randomization working correctly")
    
    # Test 6: Unicode text
    print("\n6. Testing Unicode text encryption...")
    text = "Hello, 世界! 🌍"
    message = text.encode('utf-8')
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    assert decrypted == message, "Unicode decryption failed!"
    assert decrypted.decode('utf-8') == text, "Unicode text mismatch!"
    print(f"   Original text: {text}")
    print(f"   Decrypted text: {decrypted.decode('utf-8')}")
    print("   ✓ Unicode text test passed")
    
    print("\n" + "="*50)
    print("All tests passed! ✓")
    print("="*50)

if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
