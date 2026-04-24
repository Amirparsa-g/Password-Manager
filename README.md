🔐 Secure Password Manager (Python)
A simple offline encrypted password manager built with Python and CustomTkinter.

This project allows users to securely store, edit, and manage their passwords locally using strong encryption.

The application protects stored credentials by encrypting the entire vault using a key derived from the user’s master password.

✨ Features
🔑 Master Password Authentication
🔒 Encrypted Vault Storage (Fernet / AES)
➕ Add new password entries
✏️ Edit existing passwords
🗑 Delete saved passwords
👁 Show / Hide password
📋 Copy password to clipboard
🧹 Clipboard auto‑clear for security
🧂 Secure key derivation using PBKDF2 + Salt
💾 Encrypted vault file (vault.enc)
🛠 Technologies Used
Python
CustomTkinter – Modern UI for Tkinter
cryptography library – Encryption (Fernet)
PBKDF2HMAC – Secure key derivation
JSON – Data structure before encryption
🔐 Security Design
The password manager follows a simple secure design:

The user creates a master password.

The master password is hashed and stored for login verification.

A cryptographic key is derived from the master password using:

PBKDF2
SHA256
A unique salt file
The derived key encrypts the entire vault using Fernet encryption.

Stored files:

text
vault.enc        → encrypted password vault
vault_salt.bin   → salt used for key derivation
master.hash      → hashed master password
Without the correct master password, the vault cannot be decrypted.

📂 Project Structure
text
password_manager/

main.py
password_manager_UI.py
vault_window.py
password_manager_security.py
encryption_handler.py

vault.enc
vault_salt.bin
master.hash
Main components:

UI layer → CustomTkinter interface
Vault manager → loading / saving encrypted data
Encryption handler → key derivation & encryption logic
⚙️ Installation
Clone the repository
text
git clone https://github.com/yourusername/password-manager.git
Install dependencies
text
pip install customtkinter cryptography
Run the application
text
python main.py
🚀 How It Works
Launch the application
Create or enter your master password
Unlock the vault
Add websites, usernames, and passwords
Manage entries using:
Edit
Delete
Copy
Show / Hide
All saved data is encrypted automatically.

📌 Future Improvements
Possible upgrades for the project:

🔍 Search bar for stored passwords
🔑 Password generator
⏳ Auto‑lock after inactivity
☁️ Cloud backup / sync
🏷 Categories or tags
📊 Password strength checker
📜 License
This project is for educational purposes and personal use.

👨‍💻 Author
Developed as a Python security and UI learning project.
<img width="1913" height="1015" alt="image" src="https://github.com/user-attachments/assets/6faef1bd-e1e8-4c80-8c2a-7b47bd5882ca" />
<img width="1920" height="1010" alt="image" src="https://github.com/user-attachments/assets/d58198e0-3f7e-4649-82f6-c0f71c7728a9" />
<img width="405" height="381" alt="image" src="https://github.com/user-attachments/assets/da651fb1-2004-4620-921a-30cdc2b05f87" />
<img width="1916" height="1023" alt="image" src="https://github.com/user-attachments/assets/9766376d-4dc7-40d6-98d2-bc2626d63161" />


