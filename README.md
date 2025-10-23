# 🔐 Secure File Encryption & Decryption Web Application

A **professional-grade web application** for secure file encryption and decryption — showcasing **advanced cryptographic principles** and **modern security best practices**.  
Built with **Python Flask**, **PyCryptodome**, and **modern web technologies**.

---

## 🚀 Features

### ⚙️ Core Functionality
- 🔒 **Symmetric Encryption (AES-256-CBC)** — Fast and secure file encryption using password-derived keys  
- 🧩 **Asymmetric Encryption (RSA-2048)** — Public-key cryptography for secure file sharing  
- 🧾 **File Integrity Verification** — SHA-256 hashing ensures data integrity  
- 🔑 **RSA Key Generation** — Secure generation of RSA key pairs  
- 🧠 **Password Strength Validation** — Real-time password strength assessment  

### 🛡️ Security Features
- 🧮 **Military-Grade Algorithms** — AES-256 + PBKDF2 key derivation  
- 🧷 **Random IV Generation** — Unique initialization vectors for each encryption  
- 🚫 **Rate Limiting** — Protects against abuse and brute force attacks  
- 🧰 **Secure Key Management** — No sensitive data stored on the server  
- 🧹 **Input Validation** — Comprehensive sanitization and validation  

### 💡 User Experience
- 📱 **Responsive Design** — Works on desktop & mobile  
- ⏳ **Progress Indicators** — Real-time feedback during encryption/decryption  
- 📂 **Drag & Drop Support** — Easy file uploads  
- 🌐 **Cross-Browser Compatibility** — Chrome, Firefox, Safari, Edge  
- 📏 **File Size Support** — Handles files up to 100 MB  

---

## 🛠️ Technology Stack

| Category | Technologies |
|-----------|---------------|
| **Backend** | Python 3.x, Flask, PyCryptodome, hashlib, Werkzeug |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Fetch API, File API |
| **Security** | AES-256-CBC, RSA-2048, PBKDF2, SHA-256 |

---

## 📋 Requirements

### 🖥️ System Requirements
- Python 3.7 or higher  
- 4 GB RAM (min 8 GB recommended)  
- 100 MB free disk space  
- Modern web browser with JavaScript enabled  

### 🐍 Python Dependencies
```bash
Flask==2.3.3
PyCryptodome==3.19.0
Werkzeug==2.3.7
python-dotenv==1.0.0

⚡ Installation & Setup
1️⃣ Clone the Repository
git clone <repository-url>
cd secure-file-encryption

2️⃣ Create a Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Create Environment Configuration
# .env file
SECRET_KEY=your-super-secret-key
FLASK_ENV=development

5️⃣ Run the Application
python app.py

🧭 Usage Guide
🔐 Symmetric Encryption (AES-256)

Select file (≤ 100 MB)

Enter strong password

Click Encrypt File

Download .enc file

🔓 Symmetric Decryption

Select .enc file

Enter same password

Click Decrypt File

Download restored file

🧮 Asymmetric Encryption (RSA)

Generate RSA key pair

Share public key

Encrypt file using recipient’s public key

Decrypt using your private key

🔒 Security Implementation
🧩 Cryptographic Algorithms

AES-256-CBC

RSA-2048

PBKDF2 (with salt)

SHA-256

🛡️ Security Measures

Random IV & Salt generation

Key derivation (PBKDF2 + 32-byte salt)

SHA-256 hash verification

Rate limiting for requests

🔐 Data Privacy

Files & keys never stored on the server

All operations done in memory

Use HTTPS for production

Secure session management

🧪 Testing
Manual Tests

✅ Encrypt/Decrypt small text file

✅ Verify SHA-256 integrity

✅ Generate RSA key pair

Automated Tests
python -m pytest tests/
python security_tests.py

🚀 Deployment
Local
python app.py
# Access: http://localhost:5000
