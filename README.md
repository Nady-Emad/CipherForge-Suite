# 🔐 **CipherForge Suite**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Security](https://img.shields.io/badge/Security-AES--256-red.svg)

**A Professional Encryption Toolkit with Modern GUI**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Technologies](#-technologies) • [Author](#-author)

</div>

---

## 📋 **Overview**

**CipherForge Suite** is a comprehensive encryption toolkit featuring two powerful applications:
- **Multi-Cipher Tool**: Classical encryption methods with customizable pipeline
- **AES-256-GCM Tool**: Military-grade encryption with modern security standards

Built with Python and PyQt5, offering an intuitive interface for both beginners and security professionals.

---

## ✨ **Features**

### **Multi-Cipher Tool**
- 🔄 **String Reversal**: Simple text obfuscation
- 🔤 **Caesar Cipher**: Classic shift cipher with adjustable key (supports -1M to +1M shifts)
- 🔠 **Monoalphabetic Substitution**: Bijective character mapping for enhanced security
- ⚙️ **Customizable Pipeline**: Chain encryption methods in sequence
- 🎨 **Modern UI**: Clean, responsive interface with real-time feedback

### **AES-256-GCM Tool**
- 🛡️ **AES-256-GCM**: Industry-standard authenticated encryption
- 🔑 **PBKDF2 Key Derivation**: 100,000 iterations with SHA-256
- 🔐 **Secure Random Generation**: Cryptographically secure salt and nonce
- 👁️ **Password Visibility Toggle**: Convenient password management
- 📋 **Clipboard Integration**: Quick copy/paste operations

### **Common Features**
- ⌨️ **Keyboard Shortcuts**: Ctrl+E (Encrypt), Ctrl+D (Decrypt), Ctrl+C (Copy)
- 🎯 **Status Notifications**: Real-time operation feedback
- 🧹 **Clear All Function**: Quick workspace reset
- 🎨 **Professional Design**: Modern color schemes with hover effects

---

## 🚀 **Installation**

### **Prerequisites**
```bash
Python 3.8 or higher
pip package manager
```

### **Required Libraries**
```bash
pip install PyQt5 cryptography
```

### **Quick Start**
```bash
# Clone the repository
git clone https://github.com/Nady-Emad/CipherForge-Suite.git

# Navigate to project directory
cd CipherForge-Suite

# Run Multi-Cipher Tool
python MultiCipherTool.py

# Or run AES-256-GCM Tool
python AES-256-GCM.py
```

---

## 💡 **Usage**

### **Multi-Cipher Tool**

1. **Enter your text** in the input area
2. **Select encryption methods** via checkboxes:
   - ✅ Reverse String
   - ✅ Caesar Cipher (set shift value)
   - ✅ Monoalphabetic Substitution
3. **Click Encrypt** (Ctrl+E) to process
4. **Click Decrypt** (Ctrl+D) to reverse the process

**Example Pipeline:**
```
Original Text → Reverse → Caesar (+4) → Monoalphabetic → Encrypted Output
```

### **AES-256-GCM Tool**

1. **Enter message** or paste encrypted text
2. **Set password** (use strong passwords!)
3. **Click Encrypt/Decrypt** based on your need
4. **Copy result** to clipboard for secure sharing

**Security Notes:**
- Uses 256-bit keys derived via PBKDF2
- Includes authenticated encryption (GCM mode)
- Base64 encoding for safe text transmission

---

## 📸 **Screenshots**

<div align="center">

### Multi-Cipher Tool Interface
```
╔══════════════════════════════════════════╗
║     🛡️ Multi-Method Encryption Tool      ║
╠══════════════════════════════════════════╣
║  Input Text:                             ║
║  ┌────────────────────────────────────┐  ║
║  │ Enter your text here...            │  ║
║  └────────────────────────────────────┘  ║
║                                          ║
║  Encryption Process:                     ║
║  ☐ 1. Reverse String                     ║
║  ☐ 2. Caesar Cipher    [Shift: 4]       ║
║  ☐ 3. Monoalphabetic Substitution        ║
║                                          ║
║     [🔒 Encrypt]    [🔓 Decrypt]         ║
╚══════════════════════════════════════════╝
```

### AES-256-GCM Tool Interface
```
╔══════════════════════════════════════════╗
║      🔐 AES-256-GCM Encryption Tool      ║
╠══════════════════════════════════════════╣
║  Message / Encrypted Text:   [📥 Paste] ║
║  ┌────────────────────────────────────┐  ║
║  │ Enter message...                   │  ║
║  └────────────────────────────────────┘  ║
║                                          ║
║  Password:                   [👁 Show]  ║
║  ┌────────────────────────────────────┐  ║
║  │ ••••••••••                         │  ║
║  └────────────────────────────────────┘  ║
║                                          ║
║     [🔒 Encrypt]    [🔓 Decrypt]         ║
╚══════════════════════════════════════════╝
```

</div>

---

## 🛠️ **Technologies**

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **PyQt5** | GUI framework for desktop applications |
| **Cryptography** | AES-256-GCM implementation |
| **PBKDF2HMAC** | Password-based key derivation |
| **Base64** | Safe text encoding for encrypted data |

---

## 📊 **Technical Details**

### **Encryption Algorithms**

| Algorithm | Key Size | Security Level | Use Case |
|-----------|----------|----------------|----------|
| **Reverse** | N/A | Low | Basic obfuscation |
| **Caesar** | Variable | Low | Educational purposes |
| **Monoalphabetic** | 94 chars | Medium | Classic cryptography |
| **AES-256-GCM** | 256-bit | Military-grade | Professional security |

### **Security Features**
- ✅ Authenticated Encryption (GCM mode)
- ✅ Random salt generation (16 bytes)
- ✅ Random nonce generation (12 bytes)
- ✅ 100,000 PBKDF2 iterations
- ✅ SHA-256 hashing algorithm

---

## 🔒 **Security Considerations**

### **Best Practices**
- 🔐 **Use strong passwords** (12+ characters, mixed case, numbers, symbols)
- 🔄 **Never reuse passwords** across different encryptions
- 💾 **Store encrypted data securely** (consider external backups)
- ⚠️ **Multi-Cipher Tool**: For educational purposes, not production use
- ✅ **AES-256-GCM Tool**: Suitable for sensitive data protection

### **Limitations**
- Classical ciphers (Reverse, Caesar, Mono) are **NOT** secure for modern use
- Password strength directly impacts AES encryption security
- No password recovery mechanism - **lost passwords = lost data**

---

## 📚 **Educational Value**

Perfect for learning:
- Classical cryptography concepts
- Modern encryption standards
- GUI application development
- Python security libraries
- PyQt5 interface design

---

## 🤝 **Contributing**

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

<div align="center">

### **Nady Emad**

**Networks & Cyber Security Student**  
*SUT University, Cairo, Egypt*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/nadyemad)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/Nady-Emad)

**Passionate about cybersecurity and building secure applications**

</div>

---

## 🙏 **Acknowledgments**

- PyQt5 documentation and community
- Python Cryptography library maintainers
- Classical cryptography pioneers
- Modern encryption standards organizations

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with ❤️ by [Nady Emad](https://github.com/Nady-Emad)

*© 2025 CipherForge Suite. All Rights Reserved.*

</div>

---

## 🔄 **Version History**

- **v1.0.0** (2025) - Initial release
  - Multi-Cipher Tool with 3 encryption methods
  - AES-256-GCM Tool with modern security
  - Professional GUI with keyboard shortcuts
  - Clipboard integration and status notifications

---

<div align="center">

### 📧 **Contact & Support**

For questions, suggestions, or collaborations:
- 📱 LinkedIn: [linkedin.com/in/nadyemad](https://www.linkedin.com/in/nadyemad)
- 💻 GitHub: [github.com/Nady-Emad](https://github.com/Nady-Emad)

</div>
