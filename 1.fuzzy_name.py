import pandas as pd
from rapidfuzz import fuzz, process

# === FILE PATHS ===
file_a = r"A.xlsx"  # File A: has column 'Name'
file_b = r"B.xlsx"  # File B: has columns 'Name', 'Student No', 'Result'

# === READ FILES ===
df_a = pd.read_excel(file_a)
df_b = pd.read_excel(file_b)

# Clean up names
df_a['Name'] = df_a['Name'].astype(str).str.strip().str.lower()
df_b['Name'] = df_b['Name'].astype(str).str.strip().str.lower()

# Prepare for matching
names_b = df_b['Name'].tolist()

# Lists for results
matched_name_b = []
matched_no = []
matched_score = []

for name in df_a['Name']:
    best_match = process.extractOne(name, names_b, scorer=fuzz.token_sort_ratio)
    if best_match:
        match_name, score, index = best_match
        matched_score.append(score)
        if score >= 70:  # Accept matches above 70%
            matched_name_b.append(df_b.loc[index, 'Name'])
            matched_no.append(df_b.loc[index, 'Student No'])
        else:
            matched_name_b.append(None)
            matched_no.append(None)
    else:
        matched_name_b.append(None)
        matched_no.append(None)
        matched_score.append(0)

# === CREATE RESULT DATAFRAME ===
result_df = pd.DataFrame({
    'Name (A.xlsx)': df_a['Name'],
    'Name (B.xlsx)': matched_name_b,
    'Matched_Student_No': matched_no,
    'Match_Score': matched_score
})

# === SAVE OUTPUT ===
output_file = r"STATMENT NAME MATCHING WITH RESULT november 2025 statement.xlsx"
result_df.to_excel(output_file, index=False)
print(f"✅ Matching completed! Saved as: {output_file}")

