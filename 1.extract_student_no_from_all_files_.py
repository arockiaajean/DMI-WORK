import os
import re
import pandas as pd

# === CONFIGURATION ===
root_folder = r"C:\Users\USER\Downloads\New folder\HALL TICKET MAY 2025 EXCEL - AJEEN"   # change this
output_file = r"all student.xlsx"
error_log = "errors.txt"

# regex to find 11-digit sequences anywhere in the cell
student_no_pattern = re.compile(r"\b\d{11}\b")

all_student_numbers = []

# clear previous error log
with open(error_log, "w", encoding="utf-8") as f:
    f.write("=== Error Log ===\n")

# --- Step 1: collect all Excel files ---
excel_files = []
for folderpath, _, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.lower().endswith((".xlsx", ".xls")) and not filename.startswith("~$"):
            excel_files.append(os.path.join(folderpath, filename))

total_files = len(excel_files)
print(f"Found {total_files} Excel files to process.")

# --- Step 2: process files ---
for idx, filepath in enumerate(excel_files, start=1):
    try:
        # select engine
        if filepath.lower().endswith(".xls"):
            xls = pd.ExcelFile(filepath, engine="xlrd")
        else:
            xls = pd.ExcelFile(filepath, engine="openpyxl")

        for sheet in xls.sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet, dtype=str, engine=xls.engine)
            for col in df.columns:
                for value in df[col].dropna():
                    try:
                        value_str = str(value)
                        # remove hidden/non-breaking spaces
                        value_str = value_str.replace("\xa0", "").replace(" ", "").strip()
                        # find all 11-digit sequences
                        matches = student_no_pattern.findall(value_str)
                        for match in matches:
                            all_student_numbers.append([match, os.path.basename(filepath), sheet])
                    except Exception as e:
                        with open(error_log, "a", encoding="utf-8") as f:
                            f.write(f"Error processing value '{value}' in {filepath} sheet '{sheet}': {e}\n")

    except Exception as e:
        with open(error_log, "a", encoding="utf-8") as f:
            f.write(f"Could not read {filepath}: {e}\n")

    # --- progress ---
    percent = (idx / total_files) * 100
    print(f"Progress: {percent:.2f}% ({idx}/{total_files} files)")

# --- Step 3: save results ---
if all_student_numbers:
    df_out = pd.DataFrame(all_student_numbers, columns=["Student_No", "Source_File", "Sheet"])
    df_out.drop_duplicates(inplace=True)

    print("\nFirst 20 extracted numbers (debug):")
    print(df_out.head(20))  # check data

    df_out.to_excel(output_file, index=False, sheet_name="Student_Numbers", engine="openpyxl")
    print(f"\n✅ Extracted {len(df_out)} unique student numbers. Saved to {output_file}")
else:
    print("\n❌ No student numbers found.")

