import pandas as pd

# Input and Output file paths
input_file = r"/home/ajean/Downloads/IN VCAMPUS -NOT IN CIRCULAR.xlsx"
output_file = r"IN VCAMPUS -NOT IN CIRCULAR.xlsx"

# Read all sheets into a dictionary
all_sheets = pd.read_excel(input_file, sheet_name=None)

# Merge all sheets
merged_df = pd.concat(all_sheets.values(), ignore_index=True)

# Save to new Excel file
merged_df.to_excel(output_file, index=False)

print("All sheets merged successfully!")

