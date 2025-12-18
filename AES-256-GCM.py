from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLineEdit, 
                             QLabel, QMessageBox, QGroupBox, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QClipboard, QKeySequence

def derive_key(password: str, salt: bytes) -> bytes:
    # Convert password to a strong 256-bit key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit
        salt=salt,
        iterations=100000,  # More iterations = stronger
    )
    return kdf.derive(password.encode())

def encrypt(text: str, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    ciphertext = aesgcm.encrypt(nonce, text.encode(), None)
    # Store salt + nonce + ciphertext encoded in base64
    return base64.b64encode(salt + nonce + ciphertext).decode()

def decrypt(encrypted_text: str, password: str) -> str:
    try:
        data = base64.b64decode(encrypted_text)
    except Exception:
        raise ValueError("Invalid base64 encoded text")
    
    if len(data) < 28:
        raise ValueError("Encrypted text is too short or corrupted")
    
    salt, nonce, ciphertext = data[:16], data[16:28], data[28:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode()

class AESEncryptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("AES-256-GCM Encryption Tool")
        self.setGeometry(100, 100, 850, 950)
        self.setMinimumSize(750, 950)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTextEdit, QLineEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                background-color: white;
            }
            QTextEdit:focus, QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#decryptBtn {
                background-color: #2196F3;
            }
            QPushButton#decryptBtn:hover {
                background-color: #0b7dda;
            }
            QPushButton#decryptBtn:pressed {
                background-color: #0a6bc2;
            }
            QPushButton#copyBtn {
                background-color: #FF9800;
                min-width: 200px;
            }
            QPushButton#copyBtn:hover {
                background-color: #F57C00;
            }
            QPushButton#copyBtn:pressed {
                background-color: #E65100;
            }
            QPushButton#copyBtn:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QPushButton#clearBtn {
                background-color: #e74c3c; /* red */
                min-width: 120px;
            }
            QPushButton#clearBtn:hover {
                background-color: #c0392b;
            }
            QPushButton#clearBtn:pressed {
                background-color: #a93226;
            }
            QPushButton#pasteBtn {
                background-color: #607D8B;
                min-width: 120px;
            }
            QPushButton#pasteBtn:hover {
                background-color: #455A64;
            }
            QPushButton#pasteBtn:pressed {
                background-color: #37474F;
            }
            QPushButton#showPasswordBtn {
                background-color: #9E9E9E;
                min-width: 100px;
            }
            QPushButton#showPasswordBtn:hover {
                background-color: #757575;
            }
            QPushButton#showPasswordBtn:checked {
                background-color: #616161;
            }
            QLabel {
                color: #333;
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🔐 AES-256-GCM Encryption Tool")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        # Input Group
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()
        
        # Message/Text input with paste and clear buttons
        message_header_layout = QHBoxLayout()
        message_label = QLabel("Message / Encrypted Text:")
        message_header_layout.addWidget(message_label)
        message_header_layout.addStretch()
        
        self.paste_btn = QPushButton("📥 Paste")
        self.paste_btn.setObjectName("pasteBtn")
        self.paste_btn.clicked.connect(self.paste_text)
        message_header_layout.addWidget(self.paste_btn)
        
        # (Clear button moved to bottom for better UX)
        
        input_layout.addLayout(message_header_layout)
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter your message to encrypt or encrypted text to decrypt...")
        self.message_input.setMinimumHeight(120)
        input_layout.addWidget(self.message_input)
        
        # Password input with show/hide button
        password_header_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_header_layout.addWidget(password_label)
        password_header_layout.addStretch()
        
        self.show_password_btn = QPushButton("👁 Show")
        self.show_password_btn.setObjectName("showPasswordBtn")
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.setMinimumWidth(100)
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        password_header_layout.addWidget(self.show_password_btn)
        
        input_layout.addLayout(password_header_layout)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your strong password...")
        self.password_input.setEchoMode(QLineEdit.Password)
        input_layout.addWidget(self.password_input)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.encrypt_btn = QPushButton("🔒 Encrypt")
        self.encrypt_btn.clicked.connect(self.encrypt_message)
        button_layout.addWidget(self.encrypt_btn)
        
        self.decrypt_btn = QPushButton("🔓 Decrypt")
        self.decrypt_btn.setObjectName("decryptBtn")
        self.decrypt_btn.clicked.connect(self.decrypt_message)
        button_layout.addWidget(self.decrypt_btn)
        
        main_layout.addLayout(button_layout)
        
        # Output Group
        output_group = QGroupBox("Result")
        output_layout = QVBoxLayout()
        
        # Result label
        result_label = QLabel("Result:")
        output_layout.addWidget(result_label)
        
        # Result output
        self.result_output = QTextEdit()
        self.result_output.setPlaceholderText("Result will appear here...")
        self.result_output.setReadOnly(True)
        self.result_output.setMinimumHeight(150)
        self.result_output.setStyleSheet("background-color: #f9f9f9;")
        output_layout.addWidget(self.result_output)
        
        # Copy and Clear All buttons at the bottom, centered
        copy_button_layout = QHBoxLayout()
        copy_button_layout.addStretch()

        # Clear All button (moved to bottom, clears all fields)
        self.clear_btn = QPushButton("🗑️ Clear All")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setEnabled(True)
        self.clear_btn.clicked.connect(self.clear_input)
        copy_button_layout.addWidget(self.clear_btn)

        # Spacing between buttons
        copy_button_layout.addSpacing(12)

        self.copy_btn = QPushButton("📋 Copy Result")
        self.copy_btn.setObjectName("copyBtn")
        self.copy_btn.setEnabled(False)  # Disabled by default until there's a result
        self.copy_btn.clicked.connect(self.copy_result)
        copy_button_layout.addWidget(self.copy_btn)

        copy_button_layout.addStretch()
        output_layout.addLayout(copy_button_layout)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # Footer label
        footer_label = QLabel("Nady Emad - 2025 ©")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #999; font-size: 14px; padding: 10px;")
        main_layout.addWidget(footer_label)
        
        central_widget.setLayout(main_layout)
        
        # Keyboard shortcuts
        self.encrypt_btn.setShortcut(QKeySequence("Ctrl+E"))
        self.decrypt_btn.setShortcut(QKeySequence("Ctrl+D"))
        self.copy_btn.setShortcut(QKeySequence("Ctrl+C"))
        self.paste_btn.setShortcut(QKeySequence("Ctrl+V"))
    
    def encrypt_message(self):
        message = self.message_input.toPlainText().strip()
        password = self.password_input.text().strip()
        
        if not message:
            QMessageBox.warning(self, "Warning", "Please enter a message to encrypt.")
            return
        
        if not password:
            QMessageBox.warning(self, "Warning", "Please enter a password.")
            return
        
        try:
            encrypted = encrypt(message, password)
            self.result_output.setPlainText(encrypted)
            self.copy_btn.setEnabled(True)
            self.statusBar.showMessage("✓ Message encrypted successfully!", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Encryption failed:\n{str(e)}")
            self.statusBar.showMessage("✗ Encryption failed", 3000)
            self.copy_btn.setEnabled(False)
    
    def decrypt_message(self):
        encrypted_text = self.message_input.toPlainText().strip()
        password = self.password_input.text().strip()
        
        if not encrypted_text:
            QMessageBox.warning(self, "Warning", "Please enter encrypted text to decrypt.")
            return
        
        if not password:
            QMessageBox.warning(self, "Warning", "Please enter a password.")
            return
        
        try:
            decrypted = decrypt(encrypted_text, password)
            self.result_output.setPlainText(decrypted)
            self.copy_btn.setEnabled(True)
            self.statusBar.showMessage("✓ Message decrypted successfully!", 3000)
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Decryption failed:\n{str(e)}\n\nPlease check your encrypted text format.")
            self.statusBar.showMessage("✗ Decryption failed - Invalid encrypted text format", 3000)
            self.result_output.clear()
            self.copy_btn.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Decryption failed:\n{str(e)}\n\nPlease check your password and encrypted text.")
            self.statusBar.showMessage("✗ Decryption failed - Check password and encrypted text", 3000)
            self.result_output.clear()
            self.copy_btn.setEnabled(False)
    
    def copy_result(self):
        result_text = self.result_output.toPlainText().strip()
        if not result_text:
            QMessageBox.warning(self, "Warning", "No result to copy.")
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(result_text)
        self.statusBar.showMessage("✓ Result copied to clipboard!", 2000)
    
    def paste_text(self):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text().strip()
        
        if not clipboard_text:
            QMessageBox.information(self, "Info", "Clipboard is empty.")
            return
        
        # Paste into message input
        self.message_input.setPlainText(clipboard_text)
        self.statusBar.showMessage("✓ Text pasted from clipboard!", 2000)
    
    def toggle_password_visibility(self, checked):
        """Toggle password visibility"""
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText("🙈 Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setText("👁 Show")
    
    def clear_input(self):
        self.message_input.clear()
        self.password_input.clear()
        self.result_output.clear()
        self.copy_btn.setEnabled(False)
        self.show_password_btn.setChecked(False)
        self.show_password_btn.setText("👁 Show")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.statusBar.showMessage("All fields cleared", 2000)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    window = AESEncryptionApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
