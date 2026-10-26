# get students no
import os
import re
import pandas as pd
from tqdm import tqdm


# =========================================================
# CONFIGURATION
# =========================================================

root_folder = r"/run/media/ajean/New Volume1/SAMPLE INTERNEL SHEET"

# Output CSV file
output_file = r"all student.csv"

# Error log
error_log = "errors.txt"


# =========================================================
# REGEX FOR STUDENT NUMBER
# =========================================================

# Find exactly 11 digits
student_no_pattern = re.compile(r"\b\d{11}\b")


# =========================================================
# STORAGE
# =========================================================

all_student_numbers = []


# =========================================================
# CLEAR PREVIOUS ERROR LOG
# =========================================================

with open(error_log, "w", encoding="utf-8") as f:
    f.write("=== Error Log ===\n")


# =========================================================
# STEP 1: COLLECT ALL EXCEL FILES
# =========================================================

print("Scanning folders for Excel files...")

excel_files = []

for folderpath, _, filenames in os.walk(root_folder):

    for filename in filenames:

        if (
            filename.lower().endswith((".xlsx", ".xls"))
            and not filename.startswith("~$")
        ):

            excel_files.append(
                os.path.join(folderpath, filename)
            )


total_files = len(excel_files)

print(f"Found {total_files} Excel files to process.")


# =========================================================
# STEP 2: PROCESS ALL FILES
# ONE PROGRESS BAR FOR THE ENTIRE PROCESS
# =========================================================

with tqdm(
    total=total_files,
    desc="Processing entire database",
    unit="file"
) as pbar:

    for filepath in excel_files:

        try:

            # -------------------------------------------------
            # Select Excel engine
            # -------------------------------------------------

            if filepath.lower().endswith(".xls"):

                xls = pd.ExcelFile(
                    filepath,
                    engine="xlrd"
                )

            else:

                xls = pd.ExcelFile(
                    filepath,
                    engine="openpyxl"
                )


            # -------------------------------------------------
            # Process every sheet
            # -------------------------------------------------

            for sheet in xls.sheet_names:

                df = pd.read_excel(
                    filepath,
                    sheet_name=sheet,
                    dtype=str,
                    engine=xls.engine
                )


                # -------------------------------------------------
                # Process every column
                # -------------------------------------------------

                for col in df.columns:

                    for value in df[col].dropna():

                        try:

                            value_str = str(value)

                            # Remove hidden/non-breaking spaces
                            value_str = (
                                value_str
                                .replace("\xa0", "")
                                .replace(" ", "")
                                .strip()
                            )


                            # -------------------------------------------------
                            # Find all 11-digit student numbers
                            # -------------------------------------------------

                            matches = student_no_pattern.findall(
                                value_str
                            )


                            for match in matches:

                                all_student_numbers.append(
                                    [
                                        match,
                                        os.path.basename(filepath),
                                        sheet
                                    ]
                                )


                        except Exception as e:

                            with open(
                                error_log,
                                "a",
                                encoding="utf-8"
                            ) as f:

                                f.write(
                                    f"Error processing value "
                                    f"'{value}' in {filepath} "
                                    f"sheet '{sheet}': {e}\n"
                                )


        except Exception as e:

            with open(
                error_log,
                "a",
                encoding="utf-8"
            ) as f:

                f.write(
                    f"Could not read {filepath}: {e}\n"
                )


        # -------------------------------------------------
        # UPDATE THE SINGLE PROGRESS BAR
        # -------------------------------------------------

        pbar.update(1)


# =========================================================
# STEP 3: SAVE RESULTS AS CSV
# =========================================================

if all_student_numbers:

    df_out = pd.DataFrame(
        all_student_numbers,
        columns=[
            "Student_No",
            "Source_File",
            "Sheet"
        ]
    )


    # Remove duplicate combinations
    df_out.drop_duplicates(
        inplace=True
    )


    # -------------------------------------------------
    # DEBUG: SHOW FIRST 20 RESULTS
    # -------------------------------------------------

    print("\nFirst 20 extracted numbers:")

    print(
        df_out.head(20)
    )


    # -------------------------------------------------
    # SAVE AS CSV
    # -------------------------------------------------

    df_out.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )


    print(
        f"\n✅ Extracted "
        f"{len(df_out)} unique student numbers."
    )

    print(
        f"✅ Saved to: {output_file}"
    )


else:

    print(
        "\n❌ No student numbers found."
    )
