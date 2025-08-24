# Secure File Encryption & Decryption Web Application

A professional-grade web application for secure file encryption and decryption, showcasing advanced cryptographic principles and security best practices. Built with Python Flask, PyCryptodome, and modern web technologies.

## 🚀 Features

### Core Functionality
- **Symmetric Encryption (AES-256-CBC)**: Fast and secure file encryption using password-derived keys
- **Asymmetric Encryption (RSA-2048)**: Public-key cryptography for secure file sharing
- **File Integrity Verification**: SHA-256 hashing ensures data integrity
- **Password Strength Validation**: Real-time password strength assessment
- **RSA Key Generation**: Secure generation of RSA key pairs

### Security Features
- **Military-Grade Algorithms**: AES-256 encryption with PBKDF2 key derivation
- **Random IV Generation**: Unique initialization vectors for each encryption
- **Rate Limiting**: Protection against abuse and brute force attacks
- **Secure Key Management**: No sensitive data stored on server
- **Input Validation**: Comprehensive validation and sanitization

### User Experience
- **Responsive Design**: Works on desktop and mobile devices
- **Progress Indicators**: Real-time feedback during operations
- **Drag & Drop Support**: Intuitive file upload interface
- **Cross-Browser Compatibility**: Works on Chrome, Firefox, Safari, Edge
- **File Size Support**: Handles files up to 100MB

## 🛠️ Technology Stack

### Backend
- **Python 3.x**: Core application logic
- **Flask**: Lightweight web framework
- **PyCryptodome**: Cryptographic operations (AES, RSA, PBKDF2)
- **hashlib**: SHA-256 hashing for integrity verification
- **Werkzeug**: File handling and security utilities

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with responsive design
- **JavaScript (ES6+)**: Interactive functionality
- **Fetch API**: Asynchronous HTTP requests
- **File API**: Client-side file handling

### Security Libraries
- **AES-256-CBC**: Symmetric encryption algorithm
- **RSA-2048**: Asymmetric encryption algorithm
- **PBKDF2**: Password-based key derivation function
- **SHA-256**: Cryptographic hash function

## 📋 Requirements

### System Requirements
- Python 3.7 or higher
- 4GB RAM minimum (8GB recommended)
- 100MB free disk space
- Modern web browser with JavaScript enabled

### Python Dependencies
```
Flask==2.3.3
PyCryptodome==3.19.0
Werkzeug==2.3.7
python-dotenv==1.0.0
```

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd secure-file-encryption
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```bash
# Optional: Set a custom secret key
SECRET_KEY=your-super-secret-key-here

# Optional: Set Flask environment
FLASK_ENV=development
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📖 Usage Guide

### Symmetric Encryption (AES-256)
1. **Select File**: Choose any file up to 100MB
2. **Enter Password**: Use a strong password (8+ chars, mixed case, numbers)
3. **Encrypt**: Click "Encrypt File" to process
4. **Download**: Encrypted file (.enc) will download automatically

### Symmetric Decryption
1. **Select Encrypted File**: Choose a .enc file
2. **Enter Password**: Use the same password from encryption
3. **Decrypt**: Click "Decrypt File" to restore original
4. **Download**: Decrypted file will download automatically

### Asymmetric Encryption (RSA)
1. **Generate Keys**: Create your RSA key pair
2. **Share Public Key**: Send your public key to others
3. **Encrypt for Recipient**: Others encrypt files using your public key
4. **Decrypt with Private Key**: Only you can decrypt using your private key

### RSA Key Management
1. **Generate New Pair**: Click "Generate New RSA Key Pair"
2. **Save Private Key**: Download and securely store your private key
3. **Share Public Key**: Copy and share your public key with others
4. **Key Security**: Never share your private key - it cannot be recovered

## 🔒 Security Implementation

### Cryptographic Algorithms
- **AES-256-CBC**: Industry-standard symmetric encryption
- **RSA-2048**: 2048-bit asymmetric encryption
- **PBKDF2**: Password-based key derivation with salt
- **SHA-256**: Cryptographic hash for integrity verification

### Security Measures
- **Random IV Generation**: Unique initialization vectors prevent pattern analysis
- **Salt Generation**: Random salts prevent rainbow table attacks
- **Key Derivation**: PBKDF2 with 32-byte salt and 32-byte key
- **Integrity Checking**: SHA-256 hash verification prevents tampering
- **Rate Limiting**: Prevents brute force and abuse attacks

### Data Privacy
- **No Server Storage**: Files and keys are never stored on the server
- **Temporary Processing**: All operations performed in memory
- **Secure Transmission**: HTTPS recommended for production deployment
- **Session Security**: Secure session management with random keys

## 🧪 Testing

### Manual Testing
1. **Encryption Test**: Encrypt a small text file with a password
2. **Decryption Test**: Decrypt the encrypted file with the same password
3. **Integrity Test**: Verify the decrypted file matches the original
4. **Key Generation Test**: Generate RSA keys and verify format

### Automated Testing
```bash
# Run unit tests (if implemented)
python -m pytest tests/

# Run security tests
python security_tests.py
```

### Test Scenarios
- **File Types**: Test various file formats (txt, pdf, images, etc.)
- **File Sizes**: Test small (<1MB), medium (1-50MB), large (50-100MB) files
- **Password Strength**: Test weak and strong passwords
- **Error Handling**: Test invalid inputs and edge cases

## 🚀 Deployment

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment
1. **Web Server**: Use Gunicorn or uWSGI
2. **Reverse Proxy**: Configure Nginx or Apache
3. **HTTPS**: Enable SSL/TLS certificates
4. **Environment Variables**: Set production configuration
5. **Process Management**: Use systemd or supervisor

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Cloud Platforms
- **Heroku**: Easy deployment with Procfile
- **AWS**: EC2 with load balancer
- **Google Cloud**: App Engine or Compute Engine
- **Azure**: App Service or Virtual Machines

## 📊 Performance

### Benchmarks
- **Small Files (<1MB)**: <1 second encryption/decryption
- **Medium Files (1-50MB)**: 1-10 seconds processing
- **Large Files (50-100MB)**: 10-60 seconds processing
- **Memory Usage**: <100MB RAM for typical operations
- **Concurrent Users**: Supports 10+ simultaneous users

### Optimization
- **Streaming Processing**: Large files processed in chunks
- **Memory Management**: Efficient memory usage for large files
- **Background Processing**: Non-blocking operations
- **Caching**: Temporary file caching for performance

## 🔧 Configuration

### Flask Configuration
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
```

### Security Settings
```python
# Rate limiting
RATE_LIMIT_DEFAULT = 10  # requests per minute
RATE_LIMIT_KEY_GENERATION = 5  # requests per 5 minutes

# File size limits
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'*'}  # All file types
```

### Environment Variables
```bash
# Required
SECRET_KEY=your-secret-key

# Optional
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
HOST=0.0.0.0
```

## 🐛 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure PyCryptodome is installed correctly
2. **File Size Errors**: Check file size limits and server configuration
3. **Memory Errors**: Large files may require more RAM
4. **Browser Compatibility**: Ensure JavaScript is enabled

### Error Messages
- **"No file provided"**: File upload failed
- **"File too large"**: Exceeds 100MB limit
- **"Invalid password"**: Password doesn't meet strength requirements
- **"Decryption failed"**: Wrong password or corrupted file

### Debug Mode
```bash
# Enable debug mode for development
export FLASK_DEBUG=1
python app.py
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Standards
- **Python**: PEP 8 style guide
- **JavaScript**: ES6+ standards
- **Documentation**: Clear docstrings and comments
- **Testing**: Maintain test coverage

### Security Guidelines
- **No Hardcoded Secrets**: Use environment variables
- **Input Validation**: Validate all user inputs
- **Error Handling**: Don't expose sensitive information
- **Dependency Updates**: Keep dependencies current

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyCryptodome**: Cryptographic operations library
- **Flask**: Web framework
- **Cryptographic Standards**: NIST and industry best practices
- **Security Community**: Open source security tools and guidance

## 📞 Support

### Documentation
- **README**: This file contains comprehensive setup and usage information
- **Code Comments**: Inline documentation throughout the codebase
- **API Documentation**: RESTful API endpoints and parameters

### Issues
- **GitHub Issues**: Report bugs and request features
- **Security Issues**: Report security vulnerabilities privately
- **Community**: Join discussions and contribute

### Contact
- **Email**: [your-email@example.com]
- **GitHub**: [your-github-username]
- **LinkedIn**: [your-linkedin-profile]

---

**⚠️ Security Notice**: This application is designed for educational and portfolio purposes. For production use in critical environments, additional security audits and hardening are recommended.



