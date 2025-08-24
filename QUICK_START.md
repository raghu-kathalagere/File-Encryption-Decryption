# 🚀 Quick Start Guide

## Get the Application Running in 3 Steps

### Step 1: Install Dependencies
```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

### Step 2: Run the Application
```bash
# Windows
start.bat

# macOS/Linux
chmod +x start.sh
./start.sh

# Or manually
python app.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

## 🎯 What You Can Do

### 🔐 Encrypt Files
1. Select any file (up to 100MB)
2. Enter a strong password
3. Click "Encrypt File"
4. Download your encrypted file (.enc)

### 🔓 Decrypt Files
1. Select your encrypted file (.enc)
2. Enter the same password
3. Click "Decrypt File"
4. Download your original file

### 🔑 Generate RSA Keys
1. Click "Generate New RSA Key Pair"
2. Save your private key securely
3. Share your public key with others
4. Others can encrypt files for you

## 🐛 Troubleshooting

### Common Issues
- **"Module not found"**: Run `pip install -r requirements.txt`
- **"Port already in use"**: Change port in `app.py` or stop other services
- **"File too large"**: Ensure file is under 100MB

### Need Help?
- Check the full [README.md](README.md) for detailed instructions
- Review [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for technical details
- Run `python simple_test.py` to verify setup

## 🔒 Security Features

- **AES-256 encryption** with PBKDF2 key derivation
- **RSA-2048 asymmetric encryption** for key exchange
- **SHA-256 integrity verification** to prevent tampering
- **Rate limiting** to prevent abuse
- **No server-side storage** of files or keys

## 📱 Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ❌ Internet Explorer (not supported)

---

**Ready to encrypt?** Start with Step 1 above! 🚀



