import os
import pandas as pd

# === CONFIGURATION ===
excel_file = r"chanfing file name.xlsx"  # Excel file with old/new names
files_folder = r"C:\Users\USER\Downloads\New folder (5)\PMEC EXTRACT\2026"          # Folder containing the files

# Read Excel (assuming first row has column headers "OldName" and "NewName")
df = pd.read_excel(excel_file)

# Loop through Excel rows and rename files
for index, row in df.iterrows():
    old_name = row['OldName']
    new_name = row['NewName']
    
    old_path = os.path.join(files_folder, old_name)
    new_path = os.path.join(files_folder, new_name)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} → {new_name}")
    else:
        print(f"File not found: {old_name}")

print("✅ All renaming complete!")

