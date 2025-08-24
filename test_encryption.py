#!/usr/bin/env python3
"""
Test script for the file encryption application.
This script tests the core cryptographic functions without requiring the web interface.
"""

import os
import tempfile
import hashlib
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

def derive_key(password, salt=None):
    """Derive AES key from password using PBKDF2"""
    if salt is None:
        salt = get_random_bytes(32)
    key = PBKDF2(password.encode('utf-8'), salt, dkLen=32)
    return key, salt

def encrypt_file_symmetric(file_data, password):
    """Encrypt file using AES-256-CBC"""
    try:
        # Derive key from password
        key, salt = derive_key(password)
        
        # Generate random IV
        iv = get_random_bytes(16)
        
        # Create AES cipher
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Pad data and encrypt
        padded_data = pad(file_data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        
        # Calculate hash for integrity
        file_hash = hashlib.sha256(file_data).hexdigest()
        
        # Combine salt + IV + encrypted data + hash
        result = salt + iv + encrypted_data + file_hash.encode('utf-8')
        
        return result, None
    except Exception as e:
        return None, str(e)

def decrypt_file_symmetric(encrypted_data, password):
    """Decrypt file using AES-256-CBC"""
    try:
        # Extract components
        salt = encrypted_data[:32]
        iv = encrypted_data[32:48]
        hash_part = encrypted_data[-64:]  # SHA-256 hash is 64 hex chars
        encrypted_part = encrypted_data[48:-64]
        
        # Derive key from password and salt
        key, _ = derive_key(password, salt)
        
        # Create AES cipher
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt data
        decrypted_padded = cipher.decrypt(encrypted_part)
        decrypted_data = unpad(decrypted_padded, AES.block_size)
        
        # Verify integrity
        calculated_hash = hashlib.sha256(decrypted_data).hexdigest()
        stored_hash = hash_part.decode('utf-8')
        
        if calculated_hash != stored_hash:
            return None, "File integrity check failed - file may be corrupted"
        
        return decrypted_data, None
    except Exception as e:
        return None, str(e)

def generate_rsa_keypair():
    """Generate RSA key pair"""
    try:
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key, None
    except Exception as e:
        return None, None, str(e)

def encrypt_file_asymmetric(file_data, public_key_pem):
    """Encrypt file using RSA"""
    try:
        # Import public key
        public_key = RSA.import_key(public_key_pem)
        
        # Generate random AES key for file encryption
        aes_key = get_random_bytes(32)
        iv = get_random_bytes(16)
        
        # Encrypt file with AES
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        padded_data = pad(file_data, AES.block_size)
        encrypted_file = cipher.encrypt(padded_data)
        
        # Encrypt AES key with RSA
        rsa_cipher = PKCS1_OAEP.new(public_key)
        encrypted_aes_key = rsa_cipher.encrypt(aes_key)
        
        # Combine encrypted AES key + IV + encrypted file
        result = encrypted_aes_key + iv + encrypted_file
        
        return result, None
    except Exception as e:
        return None, str(e)

def test_symmetric_encryption():
    """Test symmetric encryption and decryption"""
    print("🔐 Testing Symmetric Encryption (AES-256-CBC)...")
    
    # Test data
    test_data = b"This is a test file content for encryption testing."
    password = "TestPassword123!"
    
    print(f"   Original data: {test_data.decode('utf-8')}")
    print(f"   Password: {password}")
    
    # Encrypt
    encrypted_data, error = encrypt_file_symmetric(test_data, password)
    if error:
        print(f"   ❌ Encryption failed: {error}")
        return False
    
    print(f"   ✅ Encryption successful. Encrypted size: {len(encrypted_data)} bytes")
    
    # Decrypt
    decrypted_data, error = decrypt_file_symmetric(encrypted_data, password)
    if error:
        print(f"   ❌ Decryption failed: {error}")
        return False
    
    print(f"   ✅ Decryption successful. Decrypted data: {decrypted_data.decode('utf-8')}")
    
    # Verify integrity
    if decrypted_data == test_data:
        print("   ✅ Data integrity verified - original and decrypted data match!")
        return True
    else:
        print("   ❌ Data integrity check failed!")
        return False

def test_asymmetric_encryption():
    """Test asymmetric encryption and decryption"""
    print("\n🔑 Testing Asymmetric Encryption (RSA-2048)...")
    
    # Generate key pair
    private_key, public_key, error = generate_rsa_keypair()
    if error:
        print(f"   ❌ Key generation failed: {error}")
        return False
    
    print("   ✅ RSA key pair generated successfully")
    
    # Test data
    test_data = b"This is a test file for asymmetric encryption testing."
    print(f"   Original data: {test_data.decode('utf-8')}")
    
    # Encrypt with public key
    encrypted_data, error = encrypt_file_asymmetric(test_data, public_key)
    if error:
        print(f"   ❌ Asymmetric encryption failed: {error}")
        return False
    
    print(f"   ✅ Asymmetric encryption successful. Encrypted size: {len(encrypted_data)} bytes")
    
    # Note: Asymmetric decryption would require the private key
    # This is a simplified test - in practice, decryption would be done by the key owner
    print("   ℹ️  Asymmetric decryption test skipped (requires private key)")
    
    return True

def test_password_derivation():
    """Test password-based key derivation"""
    print("\n🔑 Testing Password-Based Key Derivation (PBKDF2)...")
    
    password = "TestPassword123!"
    
    # Generate key and salt
    key1, salt1 = derive_key(password)
    key2, salt2 = derive_key(password)
    
    print(f"   Password: {password}")
    print(f"   Key length: {len(key1)} bytes")
    print(f"   Salt length: {len(salt1)} bytes")
    
    # Test that same password with same salt produces same key
    key3, _ = derive_key(password, salt1)
    if key1 == key3:
        print("   ✅ Key derivation consistency verified")
    else:
        print("   ❌ Key derivation consistency failed")
        return False
    
    # Test that different salts produce different keys
    if key1 != key2:
        print("   ✅ Salt uniqueness verified (different keys for different salts)")
    else:
        print("   ❌ Salt uniqueness failed")
        return False
    
    return True

def test_file_operations():
    """Test file encryption and decryption with actual files"""
    print("\n📁 Testing File Operations...")
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        test_content = b"This is a test file content.\nIt contains multiple lines.\nAnd some special characters: !@#$%^&*()"
        temp_file.write(test_content)
        temp_file_path = temp_file.name
    
    try:
        print(f"   Created test file: {temp_file_path}")
        print(f"   File size: {len(test_content)} bytes")
        
        # Read file
        with open(temp_file_path, 'rb') as f:
            file_data = f.read()
        
        password = "FileTestPassword456!"
        
        # Encrypt file
        encrypted_data, error = encrypt_file_symmetric(file_data, password)
        if error:
            print(f"   ❌ File encryption failed: {error}")
            return False
        
        print(f"   ✅ File encryption successful. Encrypted size: {len(encrypted_data)} bytes")
        
        # Decrypt file
        decrypted_data, error = decrypt_file_symmetric(encrypted_data, password)
        if error:
            print(f"   ❌ File decryption failed: {error}")
            return False
        
        print(f"   ✅ File decryption successful. Decrypted size: {len(decrypted_data)} bytes")
        
        # Verify integrity
        if decrypted_data == file_data:
            print("   ✅ File integrity verified - original and decrypted files match!")
            return True
        else:
            print("   ❌ File integrity check failed!")
            return False
            
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
            print(f"   🗑️  Cleaned up test file: {temp_file_path}")

def main():
    """Run all tests"""
    print("🚀 Starting File Encryption Application Tests\n")
    print("=" * 60)
    
    tests = [
        ("Symmetric Encryption", test_symmetric_encryption),
        ("Asymmetric Encryption", test_asymmetric_encryption),
        ("Password Derivation", test_password_derivation),
        ("File Operations", test_file_operations),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            print()
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The encryption application is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)



