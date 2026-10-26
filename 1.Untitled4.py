from cryptography.fernet import Fernet

# Generate a key (run once and save it securely)
key = Fernet.generate_key()

with open("secret.key", "wb") as key_file:
    key_file.write(key)

# Load key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

input_file = "2026 april.rar"
encrypted_file = "temp.pdf.enc"

with open(input_file, "rb") as f:
    data = f.read()

encrypted_data = cipher.encrypt(data)

with open(encrypted_file, "wb") as f:
    f.write(encrypted_data)

print("File encrypted successfully!")
