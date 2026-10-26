
from pypdf import PdfWriter
from pathlib import Path

# Folder containing your PDF files
folder_path = Path("/home/ajean/Downloads/cmm 3")

# Output PDF file
output_file = folder_path / "CONSOLIDATE CMM 02.pdf"

# Find all PDF files and sort them by filename
pdf_files = sorted(
    file for file in folder_path.glob("*.pdf")
    if file != output_file
)

if not pdf_files:
    print("No PDF files found in the folder.")
else:
    writer = PdfWriter()

    for pdf in pdf_files:
        print(f"Adding: {pdf.name}")
        writer.append(str(pdf))

    with open(output_file, "wb") as output:
        writer.write(output)

    writer.close()

    print(f"\nSuccessfully merged {len(pdf_files)} PDF files.")
    print(f"Output saved to: {output_file}")

