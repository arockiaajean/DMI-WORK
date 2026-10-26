# to cut the pages

import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm

# === CONFIGURATION ===
excel_file = r"PAGES.xlsx"      # Excel file with page numbers
pdf_file = r"/home/ajean/Downloads/cmm 3/CONSOLIDATE CMM 03.pdf"         # Your large 3000-page PDF
output_pdf = r"CMM 3.pdf"  # Output PDF with Excel order

# Read numbers from Excel
df = pd.read_excel(excel_file)
search_terms = df.iloc[:, 0].dropna().astype(str).tolist()

# Load PDF
reader = PdfReader(pdf_file)
writer = PdfWriter()

print(f"🔍 Searching for {len(search_terms)} terms across {len(reader.pages)} pages...")

# Map each search term to its matching page number
term_page_map = {}

for i, page in enumerate(tqdm(reader.pages, desc="Scanning PDF pages")):
    text = page.extract_text() or ""
    for term in search_terms:
        if term not in term_page_map and term in text:
            term_page_map[term] = i  # store first page found

# Add pages in Excel order
for term in search_terms:
    if term in term_page_map:
        page_index = term_page_map[term]
        writer.add_page(reader.pages[page_index])

# Write output PDF
with open(output_pdf, "wb") as f:
    writer.write(f)

print(f"✅ Done! Extracted {len(writer.pages)} pages to '{output_pdf}' in Excel order.")

