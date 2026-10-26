import os
from openpyxl import load_workbook

# Main folder containing Excel files
main_folder = r"C:\Users\USER\Downloads\Sem 5 DONE\New folder\GPA"

# Output folder
output_folder = os.path.join(main_folder, "OUTPUT")
os.makedirs(output_folder, exist_ok=True)

# Excel file extensions
excel_extensions = (".xlsx", ".xlsm")

# Loop through main folder and all subfolders
for root, folders, files in os.walk(main_folder):

    # Don't process the OUTPUT folder again
    folders[:] = [folder for folder in folders if folder != "OUTPUT"]

    for file in files:

        # Check if the file is an Excel file
        if not file.lower().endswith(excel_extensions):
            continue

        input_file = os.path.join(root, file)

        print(f"Processing: {input_file}")

        try:
            # Load workbook
            keep_vba = file.lower().endswith(".xlsm")
            wb = load_workbook(input_file, keep_vba=keep_vba)

            # Process every sheet
            for ws in wb.worksheets:

                # Insert a new row at the top
                ws.insert_rows(1)

                # Put sheet name in A1
                ws["A1"] = ws.title

            # Create a unique output filename
            output_file = os.path.join(output_folder, file)

            # Save
            wb.save(output_file)

            print(f"Completed: {file}")

        except Exception as e:
            print(f"ERROR processing {file}: {e}")

print("\nAll files have been processed.")
