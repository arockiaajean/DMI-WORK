# find the student no with nrc
import os
import re
import pandas as pd
from tqdm import tqdm

# ============================================================
# SETTINGS
# ============================================================

# Main Excel file containing NRCs in Column A
NRC_FILE = r"extracted_NRC.xlsx"

# Folder containing all student Excel files
SEARCH_FOLDER = r"C:\Users\USER\Documents\centre data base"

# Output file
OUTPUT_FILE = r"NRC_Student_Numbers the mising 1200 from august txt.xlsx"


# ============================================================
# FUNCTION: NORMALIZE NRC
# ============================================================

def normalize_nrc(value):
    """
    Convert NRC to a consistent format for matching.
    Removes spaces and converts to uppercase.
    """

    if pd.isna(value):
        return ""

    value = str(value).strip().upper()

    # Remove spaces
    value = re.sub(r"\s+", "", value)

    return value


# ============================================================
# FUNCTION: FIND 11 DIGIT STUDENT NUMBER
# ============================================================

def find_student_number(row):
    """
    Search every cell in a row for an exactly 11-digit number.
    """

    for cell in row:

        if pd.isna(cell):
            continue

        # Convert cell to string
        value = str(cell).strip()

        # Remove common formatting spaces
        value = value.replace(" ", "")

        # Check for EXACTLY 11 numeric digits
        if re.fullmatch(r"\d{11}", value):
            return value

    return ""


# ============================================================
# STEP 1: READ NRC FILE
# ============================================================

print("\nReading NRC file...")

nrc_df = pd.read_excel(
    NRC_FILE,
    header=None,
    dtype=str
)

# Column A = index 0
nrc_list = []

for value in nrc_df.iloc[:, 0]:

    nrc = normalize_nrc(value)

    if nrc:
        nrc_list.append(nrc)

# Remove duplicate NRCs but preserve order
nrc_list = list(dict.fromkeys(nrc_list))

print(f"Total NRCs to search: {len(nrc_list)}")


# ============================================================
# STEP 2: FIND ALL EXCEL FILES
# ============================================================

print("\nFinding Excel files...")

excel_files = []

for root, dirs, files in os.walk(SEARCH_FOLDER):

    for file in files:

        # Ignore temporary Excel files
        if file.startswith("~$"):
            continue

        # Excel file extensions
        if file.lower().endswith((".xlsx", ".xls")):

            full_path = os.path.join(root, file)

            # Don't accidentally search the NRC file
            if os.path.abspath(full_path) != os.path.abspath(NRC_FILE):
                excel_files.append(full_path)

print(f"Total Excel files found: {len(excel_files)}")


# ============================================================
# STEP 3: CREATE SEARCH DICTIONARY
# ============================================================

# This will store:
#
# NRC -> Student Number
#
# Example:
# "346783/98/1" -> "20240012345"

results = {}

for nrc in nrc_list:
    results[nrc] = ""


# ============================================================
# STEP 4: SEARCH ALL EXCEL FILES
# ============================================================

print("\nSearching Excel files...\n")

for file_path in tqdm(
    excel_files,
    desc="Processing Excel files",
    unit="file"
):

    try:

        # Read all sheets
        excel_data = pd.read_excel(
            file_path,
            sheet_name=None,
            header=None,
            dtype=str
        )

        # Loop through every sheet
        for sheet_name, df in excel_data.items():

            if df.empty:
                continue

            # ------------------------------------------------
            # Loop through every row
            # ------------------------------------------------

            for row_index, row in df.iterrows():

                # Convert entire row into searchable text
                row_values = []

                for cell in row:

                    if pd.isna(cell):
                        continue

                    value = str(cell).strip()

                    # Normalize spaces for NRC comparison
                    normalized_value = re.sub(
                        r"\s+",
                        "",
                        value.upper()
                    )

                    row_values.append(normalized_value)

                if not row_values:
                    continue

                # ------------------------------------------------
                # Check every NRC
                # ------------------------------------------------

                for nrc in nrc_list:

                    # Skip NRC if already found
                    if results[nrc]:
                        continue

                    # Check if NRC exists in any cell of this row
                    if nrc in row_values:

                        # NRC found
                        student_number = find_student_number(row)

                        if student_number:

                            results[nrc] = student_number

                        break

    except Exception as e:

        print(
            f"\nERROR reading file:\n{file_path}\n"
            f"Reason: {e}\n"
        )


# ============================================================
# STEP 5: CREATE OUTPUT
# ============================================================

print("\nCreating output file...")

output_data = []

for nrc in nrc_list:

    output_data.append({
        "NRC": nrc,
        "Student No": results[nrc]
    })


output_df = pd.DataFrame(output_data)

output_df.to_excel(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# STEP 6: SUMMARY
# ============================================================

found_count = sum(
    1 for value in results.values()
    if value
)

not_found_count = len(nrc_list) - found_count

print("\n" + "=" * 60)
print("SEARCH COMPLETED")
print("=" * 60)

print(f"Total NRCs       : {len(nrc_list)}")
print(f"Student No Found : {found_count}")
print(f"Not Found        : {not_found_count}")

print(f"\nOutput file:")
print(OUTPUT_FILE)

print("=" * 60)
