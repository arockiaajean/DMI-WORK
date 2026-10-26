import os
import shutil

# 🔹 Change this to your main folder (where all folders are)
source_folder = r"C:\Users\USER\Documents\New folder (4)\New folder"

# 🔹 Where you want all Excel files to go
output_folder = r"main campus 2026"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Counter to avoid file name conflicts
file_count = 0

# Walk through all folders and subfolders
for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith(".xlsx"):
            source_path = os.path.join(root, file)

            # Rename file to avoid overwriting same names
            new_name = f"{file_count}_{file}"
            destination_path = os.path.join(output_folder, new_name)

            shutil.copy2(source_path, destination_path)

            file_count += 1

print(f"Done! {file_count} Excel files copied to {output_folder}")
