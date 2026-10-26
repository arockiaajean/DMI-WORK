import os
import shutil
import pandas as pd

# === CONFIGURATION ===
excel_file = r"E:\for img sort.xlsx"
image_folder = r"E:\Passport size photo (File responses)"
output_folder = r"E:\filter image"
column_name = "StudentNumber"

# === LOAD EXCEL FILE ===
df = pd.read_excel(excel_file)

# Normalize student numbers (remove spaces, convert to string)
student_numbers = df[column_name].astype(str).str.strip().tolist()

# === CREATE OUTPUT FOLDER ===
os.makedirs(output_folder, exist_ok=True)

# === FILTER IMAGES ===
matched = 0
for filename in os.listdir(image_folder):
    if "_" in filename:  # only process files with "_"
        student_number = filename.split("_")[0].strip()
        
        if student_number in student_numbers:
            src = os.path.join(image_folder, filename)
            dst = os.path.join(output_folder, filename)
            shutil.copy(src, dst)
            matched += 1
        else:
            print(f"⚠️ No match for: {student_number} from file {filename}")

print(f"✅ Filtering complete! {matched} images copied to: {output_folder}")

