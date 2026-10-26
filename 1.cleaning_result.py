import pandas as pd

# Load your Excel file
file_path = r"filtered_results_MPIKA.xlsx"   # change this
df = pd.read_excel(file_path)

# ---- STEP 1: Separate student info and module data ----
# Adjust these columns based on your file
student_cols = df.iloc[:, :2]   # e.g., Student No, Name, etc.
module_data = df.iloc[:, 2:]    # rest are module columns

# ---- STEP 2: Define chunk size ----
chunk_size = 5  # module_code, mark1, mark2, total, grade

modules = []

expected_cols = ["module_code", "mark1", "mark2", "total", "grade"]

# ---- STEP 3: Loop through module columns ----
for i in range(0, module_data.shape[1], chunk_size):
    chunk = module_data.iloc[:, i:i+chunk_size].copy()
    
    # Skip incomplete chunks
    if chunk.shape[1] != chunk_size:
        print(f"Skipping chunk at index {i}, found {chunk.shape[1]} columns")
        continue
    
    # Rename columns
    chunk.columns = expected_cols
    
    # Combine with student info
    merged = pd.concat([student_cols, chunk], axis=1)
    
    # Remove rows where module_code is missing (optional cleanup)
    merged = merged[merged["module_code"].notna()]
    
    modules.append(merged)

# ---- STEP 4: Combine all modules ----
final_df = pd.concat(modules, ignore_index=True)

# ---- STEP 5: Save output ----
output_file = r"cleaned solvezi result.xlsx"
final_df.to_excel(output_file, index=False)

print("Processing complete. File saved as:", output_file)
