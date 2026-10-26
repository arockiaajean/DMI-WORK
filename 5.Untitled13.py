
import pandas as pd
import os

# Step 1: Specify the Excel file path
file_path = r"all centre student no and name 11.09.2026_cleaned.xlsx"

# Step 2: Read the Excel file without treating the first row as a header
df = pd.read_excel(file_path, header=None, dtype=str)

# Step 3: Extract the first five characters from the original first column
new_column = df.iloc[:, 0].fillna("").str[:5]

# Step 4: Insert the new column before the first column
df.insert(0, "New Column", new_column)

# Step 5: Create the output file name
output_file = os.path.splitext(file_path)[0] + "_updated.xlsx"

# Step 6: Save the result to Excel
df.to_excel(output_file, index=False, header=False)

# Step 7: Display the result
print("Process completed successfully!")
print("Output file:", output_file)

