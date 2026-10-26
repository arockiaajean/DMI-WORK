
import pandas as pd

# Ask for the paths of Excel files A and B
file_a = input("Enter the path of Excel file A: ").strip()
file_b = input("Enter the path of Excel file B: ").strip()

# Read both Excel files
df_a = pd.read_excel(file_a)
df_b = pd.read_excel(file_b)

# Use the first column as the student identifier
student_column = df_a.columns[0]

# Remove duplicate students from file A and B
df_a = df_a.drop_duplicates(subset=[student_column])
df_b = df_b.drop_duplicates(subset=[student_column])

# Get student numbers from file A
students_in_a = set(df_a[student_column].dropna().astype(str).str.strip())

# Remove students from B who are already in A
df_b = df_b[
    ~df_b[student_column].fillna("").astype(str).str.strip().isin(students_in_a)
]

# Save the cleaned file .....
output_file = "B_cleaned.xlsx"
df_b.to_excel(output_file, index=False)

print("Cleaning completed!")
print("Students remaining in B:", len(df_b))
print("Output saved as:", output_file)

