import os
import hashlib
import secrets
from flask import Flask, request, jsonify, send_file, render_template_string
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import tempfile
import json
import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Rate limiting storage (in production, use Redis)
request_counts = {}

def rate_limit(limit=10, window=60):
    """Simple rate limiting"""
    client_ip = request.remote_addr
    current_time = time.time()
    
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    
    # Remove old requests outside the window
    request_counts[client_ip] = [req_time for req_time in request_counts[client_ip] 
                                if current_time - req_time < window]
    
    if len(request_counts[client_ip]) >= limit:
        return False
    
    request_counts[client_ip].append(current_time)
    return True

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

def validate_password_strength(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

@app.route('/')
def index():
    """Serve the main application page"""
    try:
        with open('simple_template.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return "HTML template not found. Please ensure simple_template.html exists.", 500

@app.route('/api/encrypt', methods=['POST'])
def encrypt_file():
    """Encrypt file endpoint"""
    if not rate_limit():
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file data
        file_data = file.read()
        if len(file_data) == 0:
            return jsonify({'error': 'Empty file'}), 400
        
        # Get encryption parameters
        encryption_type = request.form.get('encryption_type', 'symmetric')
        password = request.form.get('password', '')
        
        if encryption_type == 'symmetric':
            if not password:
                return jsonify({'error': 'Password required for symmetric encryption'}), 400
            
            # Validate password strength
            is_strong, message = validate_password_strength(password)
            if not is_strong:
                return jsonify({'error': message}), 400
            
            # Encrypt file
            encrypted_data, error = encrypt_file_symmetric(file_data, password)
            if error:
                return jsonify({'error': f'Encryption failed: {error}'}), 500
            
            # Create temporary file for download
            with tempfile.NamedTemporaryFile(delete=False, suffix='.enc') as temp_file:
                temp_file.write(encrypted_data)
                temp_path = temp_file.name
            
            return send_file(temp_path, as_attachment=True, 
                           download_name=f"{secure_filename(file.filename)}.enc")
        
        elif encryption_type == 'asymmetric':
            public_key = request.form.get('public_key', '')
            if not public_key:
                return jsonify({'error': 'Public key required for asymmetric encryption'}), 400
            
            # Encrypt file
            encrypted_data, error = encrypt_file_asymmetric(file_data, public_key)
            if error:
                return jsonify({'error': f'Encryption failed: {error}'}), 500
            
            # Create temporary file for download
            with tempfile.NamedTemporaryFile(delete=False, suffix='.enc') as temp_file:
                temp_file.write(encrypted_data)
                temp_path = temp_file.name
            
            return send_file(temp_path, as_attachment=True, 
                           download_name=f"{secure_filename(file.filename)}.enc")
        
        else:
            return jsonify({'error': 'Invalid encryption type'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt_file():
    """Decrypt file endpoint"""
    if not rate_limit():
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read encrypted file data
        encrypted_data = file.read()
        if len(encrypted_data) == 0:
            return jsonify({'error': 'Empty file'}), 400
        
        # Get decryption parameters
        decryption_type = request.form.get('decryption_type', 'symmetric')
        password = request.form.get('password', '')
        
        if decryption_type == 'symmetric':
            if not password:
                return jsonify({'error': 'Password required for symmetric decryption'}), 400
            
            # Decrypt file
            decrypted_data, error = decrypt_file_symmetric(encrypted_data, password)
            if error:
                return jsonify({'error': f'Decryption failed: {error}'}), 400
            
            # Create temporary file for download
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(decrypted_data)
                temp_path = temp_file.name
            
            # Try to determine original filename
            original_name = file.filename.replace('.enc', '') if file.filename.endswith('.enc') else file.filename
            
            return send_file(temp_path, as_attachment=True, 
                           download_name=f"decrypted_{secure_filename(original_name)}")
        
        else:
            return jsonify({'error': 'Only symmetric decryption is supported'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/generate-keys', methods=['POST'])
def generate_keys():
    """Generate RSA key pair endpoint"""
    if not rate_limit(5, 300):  # 5 requests per 5 minutes
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    try:
        private_key, public_key, error = generate_rsa_keypair()
        if error:
            return jsonify({'error': f'Key generation failed: {error}'}), 500
        
        return jsonify({
            'private_key': private_key.decode('utf-8'),
            'public_key': public_key.decode('utf-8')
        })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/validate-password', methods=['POST'])
def validate_password():
    """Validate password strength endpoint"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        is_strong, message = validate_password_strength(password)
        
        return jsonify({
            'is_strong': is_strong,
            'message': message
        })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
