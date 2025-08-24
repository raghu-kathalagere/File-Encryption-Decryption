#!/usr/bin/env python3
"""
Simple test script to verify the application structure and basic functionality.
This script runs without external dependencies to check the application setup.
"""

import os
import sys

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing Project File Structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'simple_template.html',
        'README.md',
        'PROJECT_OVERVIEW.md',
        'test_encryption.py',
        'start.bat',
        'start.sh',
        'Dockerfile',
        'docker-compose.yml'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files present")
        return True

def test_python_syntax():
    """Test that Python files have valid syntax"""
    print("\n🐍 Testing Python Syntax...")
    
    python_files = ['app.py', 'test_encryption.py']
    syntax_errors = []
    
    for file in python_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, file, 'exec')
            print(f"   ✅ {file} - Valid Python syntax")
        except SyntaxError as e:
            print(f"   ❌ {file} - Syntax error: {e}")
            syntax_errors.append((file, e))
        except Exception as e:
            print(f"   ❌ {file} - Error reading file: {e}")
            syntax_errors.append((file, e))
    
    if syntax_errors:
        print(f"\n❌ Found {len(syntax_errors)} syntax errors")
        return False
    else:
        print(f"\n✅ All Python files have valid syntax")
        return True

def test_requirements():
    """Test that requirements.txt contains necessary dependencies"""
    print("\n📦 Testing Requirements File...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = [
            'Flask',
            'PyCryptodome',
            'Werkzeug',
            'python-dotenv'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package in content:
                print(f"   ✅ {package}")
            else:
                print(f"   ❌ {package} - MISSING")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n❌ Missing {len(missing_packages)} required packages")
            return False
        else:
            print(f"\n✅ All {len(required_packages)} required packages listed")
            return True
            
    except Exception as e:
        print(f"   ❌ Error reading requirements.txt: {e}")
        return False

def test_html_template():
    """Test that HTML template is accessible"""
    print("\n🌐 Testing HTML Template...")
    
    try:
        with open('simple_template.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for essential HTML elements
        required_elements = [
            '<html',
            '<head',
            '<body',
            'Secure File Encryption',
            'encryptForm',
            'decryptForm'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element in content:
                print(f"   ✅ {element}")
            else:
                print(f"   ❌ {element} - MISSING")
                missing_elements.append(element)
        
        if missing_elements:
            print(f"\n❌ Missing {len(missing_elements)} required HTML elements")
            return False
        else:
            print(f"\n✅ All {len(required_elements)} required HTML elements present")
            return True
            
    except Exception as e:
        print(f"   ❌ Error reading HTML template: {e}")
        return False

def test_flask_app():
    """Test that Flask app can be imported (without running)"""
    print("\n⚡ Testing Flask Application...")
    
    try:
        # Check if app.py can be parsed
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for essential Flask components
        required_components = [
            'from flask import',
            'app = Flask(__name__)',
            '@app.route',
            'if __name__ == \'__main__\':'
        ]
        
        missing_components = []
        for component in required_components:
            if component in content:
                print(f"   ✅ {component}")
            else:
                print(f"   ❌ {component} - MISSING")
                missing_components.append(component)
        
        if missing_components:
            print(f"\n❌ Missing {len(missing_components)} required Flask components")
            return False
        else:
            print(f"\n✅ All {len(required_components)} required Flask components present")
            return True
            
    except Exception as e:
        print(f"   ❌ Error reading Flask app: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Secure File Encryption Application Tests\n")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Syntax", test_python_syntax),
        ("Requirements", test_requirements),
        ("HTML Template", test_html_template),
        ("Flask Application", test_flask_app),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is properly structured.")
        print("\n📋 Next Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: python app.py")
        print("3. Open browser to: http://localhost:5000")
        print("4. Test encryption/decryption functionality")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)



