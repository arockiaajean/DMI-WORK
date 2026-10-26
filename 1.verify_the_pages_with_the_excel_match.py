# to verify the pages

import pandas as pd
from PyPDF2 import PdfReader
import re

excel_file = r"students.xlsx"
pdf_file = r"matched_pages_ordered 17.10.2025.pdf"
output_excel = r"verified_per_page 17.10.2025.xlsx"

df = pd.read_excel(excel_file)

reader = PdfReader(pdf_file)

def exact_word_match(word, text):
    pattern = r"\b" + re.escape(word.lower()) + r"\b"
    return re.search(pattern, text) is not None

results = []

for index, row in df.iterrows():
    colA = str(row.iloc[0]).strip()
    colB = str(row.iloc[1]).strip()
    foundA_page = []
    foundB_page = []

    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue
        text_lower = text.lower()

        if exact_word_match(colA, text_lower):
            foundA_page.append(page_no)
        if exact_word_match(colB, text_lower):
            foundB_page.append(page_no)

    # Determine result summary
    if foundA_page and foundB_page:
        result = f"✅ FOUND A & B (Pages: {sorted(set(foundA_page + foundB_page))})"
    elif foundA_page:
        result = f"✅ FOUND A (Pages: {foundA_page})"
    elif foundB_page:
        result = f"✅ FOUND B (Pages: {foundB_page})"
    else:
        result = "❌ NOT FOUND"

    results.append(result)

df["Verification"] = results
df.to_excel(output_excel, index=False, engine="openpyxl")

print(f"✅ Done! Results saved in '{output_excel}'")

