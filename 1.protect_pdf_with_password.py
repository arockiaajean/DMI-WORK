from pypdf import PdfReader, PdfWriter

# Input and output PDF files
input_pdf = r"C:\Users\USER\Documents\Samples_3 Years - Old.pdf"
output_pdf = r"protected.pdf"

# Password
password = "262717754"

# Read the existing PDF
reader = PdfReader(input_pdf)

# Create a new PDF writer
writer = PdfWriter()

# Copy all pages
for page in reader.pages:
    writer.add_page(page)

# Encrypt the PDF
writer.encrypt(password)

# Save the encrypted PDF
with open(output_pdf, "wb") as f:
    writer.write(f)

print(f"Password-protected PDF created successfully: {output_pdf}")
print(f"Password: {password}")
