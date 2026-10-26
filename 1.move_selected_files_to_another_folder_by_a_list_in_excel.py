import os
import shutil
import pandas as pd

# === Step 1: Set your paths ===
source_folder = r"/home/ajean/Downloads/photo NOVE 2026 GRADUANDS/All Photos"
destination_folder = r"/home/ajean/Downloads/GRADUATION PHOTO SEGREGATION/3 YEARS OLD"
excel_file = r"Book2.xlsx"

# === Step 2: Read file names from Excel ===
# Assuming the Excel has a column 'FileName' or the first column has file names
df = pd.read_excel(excel_file)
file_names = df.iloc[:, 0].astype(str).tolist()  # first column to list

# === Step 3: Create destination folder if not exists ===
os.makedirs(destination_folder, exist_ok=True)

# === Step 4: Move matching files ===
for file_name in file_names:
    src_path = os.path.join(source_folder, file_name)
    
    # if file exists in source, move it
    if os.path.exists(src_path):
        shutil.move(src_path, os.path.join(destination_folder, file_name))
        print(f"✅ Moved: {file_name}")
    else:
        print(f"⚠️ File not found: {file_name}")

print("\n🎉 File moving process completed!")

