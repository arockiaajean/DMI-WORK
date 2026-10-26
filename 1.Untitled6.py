import pandas as pd
from PyPDF2 import PdfReader
from tqdm import tqdm

# Files
excel_file = r"pages.xlsx"
pdf_file = r"C:\Users\USER\Downloads\merge 01.pdf"
output_file = r"page no 01.xlsx"

# Read Excel
df = pd.read_excel(excel_file)

# Read PDF
reader = PdfReader(pdf_file)

results = []

# Progress bar for student numbers
for student_no in tqdm(df["Student No"], desc="Searching Students"):
    student_no = str(student_no).strip()
    page_found = "Not Found"

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and student_no in text:
            page_found = page_num
            break

    results.append(page_found)

# Add page numbers
df["Page No"] = results

# Save output
df.to_excel(output_file, index=False)

print(f"Done! Output saved to: {output_file}")
