import os
import shutil
from math import ceil

# ===== SETTINGS =====
source_folder = r"C:\Users\USER\python\main campus 2026"   # change this
output_folder = r"divide_Output"  # change this
number_of_folders = 6
# ====================

# Create output folder
os.makedirs(output_folder, exist_ok=True)

# Get all files only
files = [
    f for f in os.listdir(source_folder)
    if os.path.isfile(os.path.join(source_folder, f))
]

total_files = len(files)

if total_files == 0:
    print("No files found.")
    exit()

# Calculate files per folder
files_per_folder = ceil(total_files / number_of_folders)

print(f"Total files: {total_files}")
print(f"Files per folder: {files_per_folder}")

# Create folders and move files
for i in range(number_of_folders):
    folder_name = f"Part_{i+1}"
    folder_path = os.path.join(output_folder, folder_name)

    os.makedirs(folder_path, exist_ok=True)

    start = i * files_per_folder
    end = start + files_per_folder

    for file_name in files[start:end]:
        src = os.path.join(source_folder, file_name)
        dst = os.path.join(folder_path, file_name)

        shutil.move(src, dst)   # use shutil.copy() if you want copy instead

print("Done تقسیم files into 5 folders.")
