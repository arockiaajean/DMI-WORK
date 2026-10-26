# extract pdf with page no.
import pandas as pd
from pypdf import PdfReader, PdfWriter
from tqdm import tqdm

excel_file = "pages.xlsx"
pdf_file = "input.pdf"
output_pdf = "extracted_pages.pdf"

# Read page numbers from Excel
df = pd.read_excel(excel_file)

# Change column name if needed
page_numbers = df["PageNo"].dropna().astype(int).tolist()

reader = PdfReader(pdf_file)
writer = PdfWriter()

total_pages = len(reader.pages)

for page_no in tqdm(page_numbers, desc="Extracting pages"):
    if 1 <= page_no <= total_pages:
        writer.add_page(reader.pages[page_no - 1])  # PDF pages are 0-based
    else:
        print(f"Page {page_no} does not exist.")

with open(output_pdf, "wb") as f:
    writer.write(f)

print(f"\nDone! Saved as: {output_pdf}")
