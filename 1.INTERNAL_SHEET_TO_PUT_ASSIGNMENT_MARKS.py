# formate will note change
import os
import random
from openpyxl import load_workbook

ROOT_FOLDER = r"interal sheel dec 2025 1\New folder (2)"
SKIP_KEYWORD = "consolidat"  # covers consolidate / consolidated / misspellings

for root, dirs, files in os.walk(ROOT_FOLDER):
    for file in files:
        if file.lower().endswith(".xlsx"):
            file_path = os.path.join(root, file)
            print(f"Processing: {file_path}")

            wb = load_workbook(file_path)

            for sheet_name in wb.sheetnames:
                if SKIP_KEYWORD in sheet_name.lower():
                    print(f"  Skipped sheet: {sheet_name}")
                    continue

                ws = wb[sheet_name]

                # Start from row 2 (assuming row 1 is header)
                for row in range(2, ws.max_row + 1):
                    student_no = ws.cell(row=row, column=2).value  # Column B

                    if student_no is None:
                        continue

                    student_no = str(student_no)

                    if (
                        len(student_no) == 11 and
                        student_no.isdigit() and
                        student_no[8] == "4"   # 9th character
                    ):
                        ws.cell(row=row, column=4).value = random.randint(7, 10)  # D
                        ws.cell(row=row, column=5).value = random.randint(7, 10)  # E
                        ws.cell(row=row, column=6).value = random.randint(7, 10)  # F

            wb.save(file_path)
            print(f"  ✔ Updated without format change\n")

print("🎉 Done. All files updated safely.")

