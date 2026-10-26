import pandas as pd
from rapidfuzz import fuzz

# =========================
# FILE PATHS
# =========================
file1_path = r"file1dec.xlsx"   # Statement + Code
file2_path = r"file2dec.xlsx"   # Student No, Student Name, Code
output_path = "FINAL_OUTPUT.xlsx"

# =========================
# READ EXCEL FILES
# =========================
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# Rename columns clearly
df1.columns = ["STATEMENT", "CODE"]
df2.columns = ["STUDENT_NO", "STUDENT_NAME", "CODE"]

# Ensure CODE is string (exact match safety)
df1["CODE"] = df1["CODE"].astype(str)
df2["CODE"] = df2["CODE"].astype(str)

# =========================
# MATCHING
# =========================
output_rows = []

for _, row1 in df1.iterrows():
    statement = str(row1["STATEMENT"])
    code = row1["CODE"]

    best_match_name = ""
    best_score = 0

    # Filter File 2 by exact CODE
    df2_code_match = df2[df2["CODE"] == code]

    for _, row2 in df2_code_match.iterrows():
        student_name = str(row2["STUDENT_NAME"])

        score = fuzz.partial_ratio(student_name.lower(), statement.lower())

        if score >= 30 and score > best_score:
            best_score = score
            best_match_name = student_name

    # Append ALL statements (matched or not)
    output_rows.append({
        "STATEMENT": statement,
        "CODE": code,
        "STUDENT NAME": best_match_name,
        "MATCH SCORE": best_score if best_match_name else ""
    })

# =========================
# OUTPUT TO EXCEL
# =========================
output_df = pd.DataFrame(output_rows)
output_df.to_excel(output_path, index=False)

print("✅ Process completed successfully")
print(f"📁 Output file created: {output_path}")

