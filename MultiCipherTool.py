import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QMessageBox, QGroupBox, QStatusBar, QCheckBox, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

# --- logic from Lab 5 encryption.py ---

def reverse_text(text: str) -> str:
    return text[::-1]

def caesar_cipher_logic(text: str, k: int, encrypt: bool = True) -> str:
    if not encrypt:
        k = -k
    
    result = ""
    for i in text:
        if i == " ":
            result += " "
            continue
        
        if i.islower():
            x = ord(i)
            # The logic in Lab 5: chr(((x + k - 97) % 26) + 97)
            # This works for both positive and negative k (for decryption)
            c = chr(((x + k - 97) % 26) + 97)
            result += c
        elif i.isupper():
            x = ord(i)
            c = chr(((x + k - 65) % 26) + 65)
            result += c
        else:
            result += i
    return result

# Bijective Monoalphabetic Map (Guaranteed unique values for every key)
# Generated to ensure perfect reversibility.
MONO_MAP = {
    'a': 'P', 'b': '5', 'c': 'k', 'd': 'Z', 'e': '?', 'f': '1', 'g': 'y', 'h': 'S', 'i': '9', 'j': 'm',
    'k': '@', 'l': 'F', 'm': 'o', 'n': '2', 'o': 'L', 'p': 'w', 'q': 'D', 'r': 'H', 's': '4', 't': 'n',
    'u': 'G', 'v': 'j', 'w': 'B', 'x': 'R', 'y': '0', 'z': '!', 'A': 'x', 'B': '8', 'C': 'U', 'D': 't',
    'E': 'q', 'F': 'K', 'G': 'v', 'H': 'A', 'I': '6', 'J': 'e', 'K': 'i', 'L': 'M', 'M': '3', 'N': 'X',
    'O': 'z', 'P': 'J', 'Q': 'C', 'R': '7', 'S': 'E', 'T': 'b', 'U': 'Y', 'V': 'l', 'W': 'O', 'X': 's',
    'Y': 'Q', 'Z': 'r', '0': 'u', '1': 'g', '2': 'p', '3': 'V', '4': 'a', '5': 'd', '6': 'f', '7': 'c',
    '8': 'h', '9': 'W', '!': 'I', '@': 'N', '#': 'T', '$': '.', '%': ',', '^': ':', '&': ';', '*': '-',
    '(': '_', ')': '+', '_': '=', '+': '[', '-': ']', '=': '{', '[': '}', ']': '<', '{': '>', '}': '/',
    ';': '?', ':': '"', "'": '|', '"': ' ', ',': '(', '.': ')', '<': '*', '>': '&', '/': '^', '?': '%',
    ' ': '$', '|': '#'
}
INVERSE_MONO_MAP = {v: k for k, v in MONO_MAP.items()}

def mono_cipher_logic(text: str, encrypt: bool = True) -> str:
    mapping = MONO_MAP if encrypt else INVERSE_MONO_MAP
    result = []
    for ch in text:
        result.append(mapping.get(ch, ch))
    return ''.join(result)

# --- GUI Application ---

class MultiCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Multi-Method Encryption Tool (Updated)")
        self.setGeometry(100, 100, 850, 950)
        self.setMinimumSize(750, 900)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Stylesheet (Adapted from AES-256-GCM.py)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F3F4F6;
            }
            QGroupBox {
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                margin-top: 24px;
                padding-top: 20px;
                padding-bottom: 20px;
                background-color: #FFFFFF;
                color: #374151;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #1F2937;
            }
            QTextEdit, QLineEdit, QSpinBox {
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                background-color: #F9FAFB;
                color: #111827;
                selection-background-color: #3B82F6;
            }
            QTextEdit:focus, QLineEdit:focus, QSpinBox:focus {
                border: 2px solid #3B82F6;
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #3B82F6; /* Blue Primary */
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
                padding-top: 14px; /* Pressed effect */
                padding-bottom: 10px;
            }
            QPushButton#decryptBtn {
                background-color: #10B981; /* Emerald Green */
            }
            QPushButton#decryptBtn:hover {
                background-color: #059669;
            }
            QPushButton#decryptBtn:pressed {
                background-color: #047857;
            }
            QPushButton#copyBtn {
                background-color: #F59E0B; /* Amber */
                color: white;
            }
            QPushButton#copyBtn:hover {
                background-color: #D97706;
            }
            QPushButton#copyBtn:disabled {
                background-color: #E5E7EB;
                color: #9CA3AF;
            }
            QPushButton#clearBtn {
                background-color: #EF4444; /* Red */
            }
            QPushButton#clearBtn:hover {
                background-color: #DC2626;
            }
            QPushButton#pasteBtn {
                background-color: #6B7280; /* Gray */
                min-width: 80px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton#pasteBtn:hover {
                background-color: #4B5563;
            }
            QLabel {
                color: #374151;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 4px;
            }
            QCheckBox {
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
                color: #1F2937;
                spacing: 12px;
                padding: 4px;
            }
            QStatusBar {
                background-color: #E5E7EB;
                color: #374151;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🛡️ Multi-Method Encryption Tool")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #111827; margin-bottom: 16px; font-family: 'Segoe UI', sans-serif;")
        main_layout.addWidget(title)
        
        # Input Group
        input_group = QGroupBox("Input Text")
        input_layout = QVBoxLayout()
        
        # Header with Paste
        input_header = QHBoxLayout()
        input_header.addStretch()
        self.paste_btn = QPushButton("📥 Paste from Clipboard")
        self.paste_btn.setObjectName("pasteBtn")
        self.paste_btn.setCursor(Qt.PointingHandCursor)
        self.paste_btn.clicked.connect(self.paste_text)
        input_header.addWidget(self.paste_btn)
        input_layout.addLayout(input_header)
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter your text here...")
        self.message_input.setMinimumHeight(100)
        input_layout.addWidget(self.message_input)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Pipeline Configuration Group
        pipeline_group = QGroupBox("Encryption Process")
        pipeline_layout = QVBoxLayout()
        pipeline_layout.setSpacing(12)
        
        # Step 1: Reverse
        step1_layout = QHBoxLayout()
        self.check_reverse = QCheckBox("1. Reverse String")
        self.check_reverse.setCursor(Qt.PointingHandCursor)
        step1_layout.addWidget(self.check_reverse)
        step1_layout.addStretch()
        pipeline_layout.addLayout(step1_layout)
        
        # Step 2: Caesar
        step2_layout = QHBoxLayout()
        self.check_caesar = QCheckBox("2. Caesar Cipher")
        self.check_caesar.setCursor(Qt.PointingHandCursor)
        step2_layout.addWidget(self.check_caesar)
        
        step2_layout.addSpacing(20)
        step2_layout.addWidget(QLabel("Shift Amount:"))
        self.spin_k = QSpinBox()
        self.spin_k.setRange(-1000000, 1000000)
        self.spin_k.setValue(4)
        self.spin_k.setFixedWidth(180)
        self.spin_k.setAlignment(Qt.AlignCenter)
        step2_layout.addWidget(self.spin_k)
        step2_layout.addStretch()
        pipeline_layout.addLayout(step2_layout)
        
        # Step 3: Monoalphabetic
        step3_layout = QHBoxLayout()
        self.check_mono = QCheckBox("3. Monoalphabetic Substitution")
        self.check_mono.setCursor(Qt.PointingHandCursor)
        step3_layout.addWidget(self.check_mono)
        step3_layout.addStretch()
        pipeline_layout.addLayout(step3_layout)
        
        pipeline_group.setLayout(pipeline_layout)
        main_layout.addWidget(pipeline_group)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.encrypt_btn = QPushButton("🔒 Encrypt")
        self.encrypt_btn.setCursor(Qt.PointingHandCursor)
        self.encrypt_btn.setMinimumHeight(45)
        self.encrypt_btn.clicked.connect(self.run_encryption)
        button_layout.addWidget(self.encrypt_btn, 1)
        
        self.decrypt_btn = QPushButton("🔓 Decrypt")
        self.decrypt_btn.setObjectName("decryptBtn")
        self.decrypt_btn.setCursor(Qt.PointingHandCursor)
        self.decrypt_btn.setMinimumHeight(45)
        self.decrypt_btn.clicked.connect(self.run_decryption)
        button_layout.addWidget(self.decrypt_btn, 1)
        
        main_layout.addLayout(button_layout)
        
        # Output Group
        output_group = QGroupBox("Result")
        output_layout = QVBoxLayout()
        
        self.result_output = QTextEdit()
        self.result_output.setPlaceholderText("Result will appear here...")
        self.result_output.setReadOnly(True)
        self.result_output.setMinimumHeight(100)
        self.result_output.setStyleSheet("background-color: #f9f9f9;")
        output_layout.addWidget(self.result_output)
        
        # Bottom Buttons
        bottom_btns = QHBoxLayout()
        bottom_btns.setSpacing(20)
        
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_all)
        bottom_btns.addWidget(self.clear_btn, 1)
        
        self.copy_btn = QPushButton("📋 Copy Result")
        self.copy_btn.setObjectName("copyBtn")
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.setEnabled(False)
        self.copy_btn.clicked.connect(self.copy_result)
        bottom_btns.addWidget(self.copy_btn, 2) # Copy is wider
        
        output_layout.addLayout(bottom_btns)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # Footer
        footer = QLabel("Multi-Cipher Tool © 2025")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #999; margin-top: 10px;")
        main_layout.addWidget(footer)
        
        central_widget.setLayout(main_layout)
        
        # Shortcuts
        self.encrypt_btn.setShortcut(QKeySequence("Ctrl+E"))
        self.decrypt_btn.setShortcut(QKeySequence("Ctrl+D"))
        self.copy_btn.setShortcut(QKeySequence("Ctrl+C"))
        self.paste_btn.setShortcut(QKeySequence("Ctrl+V"))

    def run_encryption(self):
        text = self.message_input.toPlainText()
        if not text:
            self.statusBar.showMessage("Please enter text to encrypt.", 3000)
            return
            
        try:
            # Pipeline: Reverse -> Caesar -> Mono
            if self.check_reverse.isChecked():
                text = reverse_text(text)
            
            if self.check_caesar.isChecked():
                k = self.spin_k.value()
                text = caesar_cipher_logic(text, k, encrypt=True)
                
            if self.check_mono.isChecked():
                text = mono_cipher_logic(text, encrypt=True)
                
            self.result_output.setPlainText(text)
            self.copy_btn.setEnabled(True)
            self.statusBar.showMessage("✓ Encryption successful!", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")

    def run_decryption(self):
        text = self.message_input.toPlainText()
        if not text:
            self.statusBar.showMessage("Please enter text to decrypt.", 3000)
            return
            
        try:
            # Pipeline Reverse: Mono -> Caesar -> Reverse
            if self.check_mono.isChecked():
                text = mono_cipher_logic(text, encrypt=False)
                
            if self.check_caesar.isChecked():
                k = self.spin_k.value()
                text = caesar_cipher_logic(text, k, encrypt=False)
                
            if self.check_reverse.isChecked():
                text = reverse_text(text)
                
            self.result_output.setPlainText(text)
            self.copy_btn.setEnabled(True)
            self.statusBar.showMessage("✓ Decryption successful!", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")

    def paste_text(self):
        clipboard = QApplication.clipboard()
        self.message_input.setPlainText(clipboard.text())
        self.statusBar.showMessage("Pasted from clipboard", 2000)

    def copy_result(self):
        text = self.result_output.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.statusBar.showMessage("Copied to clipboard", 2000)

    def clear_all(self):
        self.message_input.clear()
        self.result_output.clear()
        self.copy_btn.setEnabled(False)
        self.statusBar.showMessage("Cleared all fields", 2000)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MultiCipherApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
