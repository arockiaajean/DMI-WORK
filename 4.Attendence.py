import os
import shutil
# step 2 arrage the files according to the program.
# Change this to your folder path
BASE_DIR = r"Generated_Attendance_Sheets KITWE AUG 2026-END 1"

for filename in os.listdir(BASE_DIR):
    if not filename.lower().endswith((".pdf", ".docx", ".doc", ".txt")):
        continue  # skip non-files if needed
    
    file_path = os.path.join(BASE_DIR, filename)
    
    if os.path.isfile(file_path):
        # Extract folder name → everything before "_Sem"
        if "_Sem" in filename:
            folder_name = filename.split("_Sem")[0]
        else:
            continue  # skip if pattern not found
        
        # Make folder if not exists
        folder_path = os.path.join(BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Move file
        shutil.move(file_path, os.path.join(folder_path, filename))
        print(f"Moved: {filename} → {folder_name}/")

print("Task Completed!")

