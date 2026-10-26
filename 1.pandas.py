import pandas as pd

# Input Excel file (where all student rows are stored)
input_file = r"E:\filtered_results_09.xlsx"

# Output Excel file (each student in a separate sheet)
output_file = r"E:\RESULT SHEET WISE.xlsx"

# Read the Excel file
df = pd.read_excel(input_file, dtype=str)

# Assume the first column is Student Number (adjust if different)
student_col = df.columns[0]

# Write each student row to a separate sheet
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for student_no, row in df.iterrows():
        sheet_name = str(row[student_col]).strip()[:31]  # Excel sheet name limit
        student_df = pd.DataFrame([row])  # keep entire row
        student_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"✅ Done! Saved to {output_file}")

