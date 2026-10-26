
import os
import pandas as pd
from tqdm import tqdm

# 1. Set the main folder
folder_path = r"/home/ajean/Downloads/CMM/New folder"

# 2. Set the output file
output_file = os.path.join(
    folder_path, "Merged_Results.xlsx"
)

# 3. Find all Excel files recursively
excel_files = []

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith((".xlsx", ".xls")):
            full_path = os.path.join(root, file)

            # Avoid reading the output file again
            if os.path.abspath(full_path) != os.path.abspath(output_file):
                excel_files.append(full_path)

print(f"Total Excel files found: {len(excel_files)}")

# 4. Store all data here
all_data = []

# 5. Process each Excel file
for file_path in tqdm(excel_files, desc="Processing files"):

    try:
        # Open the workbook
        excel = pd.ExcelFile(file_path)

        # Read every sheet
        for sheet_name in excel.sheet_names:

            try:
                df = pd.read_excel(
                    excel,
                    sheet_name=sheet_name
                )

                # Skip completely empty sheets
                if df.empty:
                    continue

                # Add source information
                df.insert(0, "Source_File",
                          os.path.basename(file_path))
                df.insert(1, "Source_Sheet",
                          sheet_name)

                # Store the data
                all_data.append(df)

            except Exception as e:
                print(
                    f"\nError in sheet {sheet_name}: {e}"
                )

        excel.close()

    except Exception as e:
        print(f"\nCould not read {file_path}: {e}")

# 6. Merge all collected data
if all_data:

    print("\nCombining all data...")

    merged_df = pd.concat(
        all_data,
        ignore_index=True,
        sort=False
    )

    # 7. Export to Excel
    merged_df.to_excel(
        output_file,
        index=False,
        engine="openpyxl"
    )

    print("\nMerging completed!")
    print(f"Total rows: {len(merged_df)}")
    print(f"Total columns: {len(merged_df.columns)}")
    print(f"Output saved at: {output_file}")

else:
    print("No data found in the Excel files.")
