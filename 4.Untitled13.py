
import pandas as pd
import os

# Step 1: Specify the Excel file paths
file_a = r"/home/ajean/Downloads/Graduation Books/extracted_11_digit_numbers.xlsx"
file_b = r"all centre student no and name 11.09.2026.xlsx"

# Step 2: Read both Excel files without headers
df_a = pd.read_excel(file_a, header=None, dtype=str)
df_b = pd.read_excel(file_b, header=None, dtype=str)

# Step 3: Get student numbers from the first column of A
student_numbers_a = set(
    df_a.iloc[:, 0].dropna().str.strip()
)

# Step 4: Remove from B student numbers found in A
filtered_df = df_b[
    ~df_b.iloc[:, 0].fillna("").str.strip().isin(student_numbers_a)
].copy()

# Step 5: Remove duplicate student numbers from B
filtered_df = filtered_df.drop_duplicates(
    subset=filtered_df.columns[0],
    keep="first"
)

# Step 6: Save the output Excel file
output_file = os.path.splitext(file_b)[0] + "_cleaned.xlsx"

filtered_df.to_excel(
    output_file,
    index=False,
    header=False
)

# Step 7: Display the results
print("Process completed successfully!")
print("Original rows in B:", len(df_b))
print("Remaining rows:", len(filtered_df))
print("Output file:", output_file)

