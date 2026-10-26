# filterd results
import os
import pandas as pd
from tqdm import tqdm


# =========================================================
# 1. PATHS
# =========================================================

# Main folder containing all Excel files and subfolders
main_folder = r"F:\RESULTS UPDATE"

# Master student list
master_file = r"all student.xlsx"


# =========================================================
# 2. LOAD MASTER STUDENT NUMBERS
# =========================================================

print("Loading master student list...")

master_df = pd.read_excel(master_file)

# Take the first column as student numbers
# Convert everything to string so comparison is easier
student_numbers = set(
    master_df.iloc[:, 0].astype(str).str.strip()
)

print(f"Total student numbers loaded: {len(student_numbers)}")


# =========================================================
# 3. FIND ALL EXCEL FILES FIRST
# =========================================================

print("Scanning folders for Excel files...")

excel_files = []

for root, dirs, files in os.walk(main_folder):
    for file in files:

        if file.lower().endswith((".xlsx", ".xls")):

            file_path = os.path.join(root, file)

            # Don't accidentally process the master file
            if os.path.abspath(file_path) != os.path.abspath(master_file):
                excel_files.append(file_path)


print(f"Total Excel files found: {len(excel_files)}")


# =========================================================
# 4. PREPARE FINAL RESULTS
# =========================================================

all_matches = []


# =========================================================
# 5. PROCESS ALL FILES WITH ONE PROGRESS BAR
# =========================================================

with tqdm(
    total=len(excel_files),
    desc="Processing entire database",
    unit="file"
) as pbar:

    for file_path in excel_files:

        try:

            # -------------------------------------------------
            # Read Excel file
            # -------------------------------------------------

            df = pd.read_excel(
                file_path,
                dtype=str
            )


            # -------------------------------------------------
            # Find MODULE CODE row
            # -------------------------------------------------

            module_code_row = None

            for _, row in df.iterrows():

                row_text = " ".join(
                    str(x)
                    for x in row.values
                    if pd.notna(x)
                )

                if "CODE" in row_text.upper():

                    module_code_row = list(row.values)

                    break


            # -------------------------------------------------
            # Check every row for student numbers
            # -------------------------------------------------

            for _, row in df.iterrows():

                row_text = " ".join(
                    str(x)
                    for x in row.values
                    if pd.notna(x)
                )

                found_sn = None

                # Check student numbers
                for sn in student_numbers:

                    if sn in row_text:

                        found_sn = sn

                        break


                # -------------------------------------------------
                # Student number found
                # -------------------------------------------------

                if found_sn:

                    # Save the student row
                    row_data = list(row.values)

                    # Add source file path
                    row_data.append(file_path)

                    all_matches.append(row_data)


                    # Save MODULE CODE row
                    if module_code_row:

                        all_matches.append(module_code_row)


        except Exception as e:

            print(f"\nSkipping {file_path}: {e}")


        # -------------------------------------------------
        # Update ONE progress bar
        # -------------------------------------------------

        pbar.update(1)


# =========================================================
# 6. SAVE RESULTS
# =========================================================

if all_matches:

    result_df = pd.DataFrame(all_matches)

    output_file = (
        "dec.csv"
    )

    result_df.to_csv(
        output_file,
        index=False,
        header=False
    )

    print("\n✅ Finished!")
    print(f"Results saved to: {output_file}")
    print(f"Total result rows: {len(all_matches)}")

else:

    print("\n⚠️ No matching student numbers found.")
