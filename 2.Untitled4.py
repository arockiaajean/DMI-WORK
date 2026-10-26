from cryptography.fernet import Fernet

with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

encrypted_file = "temp.pdf.enc"
output_file = "a\example_decrypted.rar"

with open(encrypted_file, "rb") as f:
    encrypted_data = f.read()

decrypted_data = cipher.decrypt(encrypted_data)

with open(output_file, "wb") as f:
    f.write(decrypted_data)

print("File decrypted successfully!")
