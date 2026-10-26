
import pandas as pd
import os

# Ask for the file paths
file_a = input("Enter the path of Excel file A: ").strip()
file_b = input("Enter the path of CSV file B: ").strip()

# Read Excel file A
df_a = pd.read_excel(file_a)

# Read CSV file B
df_b = pd.read_csv(file_b, dtype=str, encoding="utf-8-sig")

# Use the first column as the student number
student_column_a = df_a.columns[0]
student_column_b = df_b.columns[0]

# Get student numbers from A
students_in_a = set(
    df_a[student_column_a]
    .dropna()
    .astype(str)
    .str.strip()
)

# Remove students from B who already exist in A
df_b = df_b[
    ~df_b[student_column_b]
    .fillna("")
    .astype(str)
    .str.strip()
    .isin(students_in_a)
]

# Remove duplicate student numbers from B
df_b = df_b.drop_duplicates(subset=[student_column_b])

# Create the output CSV filename
output_file = os.path.splitext(file_b)[0] + "_cleaned.csv"

# Save the cleaned data
df_b.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nCleaning completed!")
print("Students remaining:", len(df_b))
print("Output file:", output_file)

