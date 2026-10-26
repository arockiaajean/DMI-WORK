import pandas as pd
import re
from rapidfuzz import fuzz

# === SETTINGS ===
INPUT_FILE = r"output_with_standardized_dates.xlsx"
OUTPUT_FILE = r"temp.xlsx"
COLUMN_NAME = "D"   # Column with comments
THRESHOLD = 80      # Fuzzy match score (0–100)

# Target keywords
KEYWORDS = ["aug", "dec"]

# === CLEAN FUNCTION ===
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]', '', text)  # remove spaces, hyphens, symbols
    return text

# === MATCH FUNCTION ===
def is_pmec(text):
    cleaned = clean_text(text)
    
    for keyword in KEYWORDS:
        score = fuzz.partial_ratio(cleaned, keyword)
        if score >= THRESHOLD:
            return "PMEC"
    
    return ""

# === LOAD EXCEL ===
df = pd.read_excel(INPUT_FILE)

# If column is letter (D), convert to index
col_index = ord(COLUMN_NAME.upper()) - ord('A')
target_column = df.columns[col_index]

# === APPLY FUNCTION ===
df["F"] = df[target_column].apply(is_pmec)

# === SAVE FILE ===
df.to_excel(OUTPUT_FILE, index=False)

print("✅ Done! Output saved as:", OUTPUT_FILE)
