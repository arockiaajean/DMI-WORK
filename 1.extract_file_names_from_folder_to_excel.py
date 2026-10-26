import os
from openpyxl import Workbook

# 1. Give the path of your folder
folder_path = "/home/ajean/Downloads/photo NOVE 2026 GRADUANDS/All Photos"

# 2. Create a new Excel workbook
workbook = Workbook()

# 3. Select the first worksheet
sheet = workbook.active

# 4. Give a heading to the first column
sheet["A1"] = "File Name"

# 5. Get all files from the folder
files = os.listdir(folder_path)

# 6. Start writing filenames from row 2
row = 2

# 7. Go through every item in the folder
for file in files:

    # 8. Create the complete path
    full_path = os.path.join(folder_path, file)

    # 9. Check whether it is actually a file
    if os.path.isfile(full_path):

        # 10. Write the filename into Excel
        sheet.cell(row=row, column=1, value=file)

        # 11. Move to the next row
        row += 1

# 12. Save the Excel file
output_file = "/home/ajean/Downloads/photo NOVE 2026 GRADUANDS/file_names.xlsx"
workbook.save(output_file)

# 13. Tell us where the Excel file was created
print("Finished!")
print("Excel file created at:")
print(output_file)
