
import pandas as pd
import os

# Ask for the paths of CSV files A and B
file_a = ("/home/ajean/Downloads/Graduation Books/extracted_11_digit_numbers.xlsx")
file_b = ("all centre student no and name 11.09.2026.xlsx")

# Read both CSV files without headers
df_a = pd.read_csv(file_a, header=None, dtype=str)
df_b = pd.read_csv(file_b, header=None, dtype=str)

# The first column (index 0) contains student numbers
student_column = 0

# Remove duplicate student numbers from both files
df_a = df_a.drop_duplicates(subset=[student_column])
df_b = df_b.drop_duplicates(subset=[student_column])

# Get student numbers from file A
students_in_a = set(
    df_a[student_column]
    .dropna()
    .str.strip()
)

# Remove rows from B if the student number exists in A
df_b = df_b[
    ~df_b[student_column]
    .fillna("")
    .str.strip()
    .isin(students_in_a)
    == False
]

# Create the output filename
output_file = "B_cleaned.csv"

# Save the cleaned data without adding a header
df_b.to_csv(output_file, index=False, header=False)

print("Cleaning completed!")
print("Students remaining in B:", len(df_b))
print("Output saved as:", os.path.abspath(output_file))

