import os
from openpyxl import load_workbook, Workbook

# Folder containing Excel files
folder_path = r"/home/ajean/Downloads/all centre august intake 2026 data"

# Output file
output_file = "merged_all_in_one_sheet.xlsx"

# Create new workbook
merged_wb = Workbook()
merged_ws = merged_wb.active
merged_ws.title = "Merged_Data"

current_row = 1

# Loop through all Excel files
for file in os.listdir(folder_path):

    if file.endswith(".xlsx") and not file.startswith("~$"):

        file_path = os.path.join(folder_path, file)

        print(f"Processing: {file}")

        wb = load_workbook(file_path, data_only=True)

        # Loop through all sheets
        for sheet_name in wb.sheetnames:

            ws = wb[sheet_name]

            # Optional title separator
            merged_ws.cell(row=current_row, column=1).value = f"FILE: {file} | SHEET: {sheet_name}"
            current_row += 1

            # Copy all rows
            for row in ws.iter_rows(values_only=True):

                for col_num, value in enumerate(row, start=1):
                    merged_ws.cell(row=current_row, column=col_num, value=value)

                current_row += 1

            # Empty row between sheets
            current_row += 2

# Save output
merged_wb.save(output_file)

print(f"\nDone! Saved as: {output_file}")
