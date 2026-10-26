import os
import re
import shutil
# step 3 arrage the file according to the semester
ROOT_FOLDER = r"Generated_Attendance_Sheets KITWE AUG 2026-END 1"

# Regex to capture semester (Sem1, Sem2, etc.)
pattern = re.compile(r"(Sem\d+)")

for root, dirs, files in os.walk(ROOT_FOLDER):
    for file in files:
        file_path = os.path.join(root, file)

        # Skip if already inside a Sem folder
        if re.search(r"Sem\d+", root):
            continue

        # Find semester in filename
        match = pattern.search(file)

        if match:
            sem_folder = match.group(1)  # e.g., Sem2

            # Create Sem folder INSIDE the current folder
            dest_folder = os.path.join(root, sem_folder)
            os.makedirs(dest_folder, exist_ok=True)

            # Move file into that folder
            try:
                shutil.move(file_path, os.path.join(dest_folder, file))
                print(f"Moved: {file} → {root}\\{sem_folder}")
            except Exception as e:
                print(f"Error moving {file}: {e}")

print("Done organizing per folder!")
