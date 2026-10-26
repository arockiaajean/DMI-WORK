import pandas as pd
import re
from pathlib import Path

# ============================================================
# SETTINGS
# ============================================================

input_file = r"C:\Users\USER\Downloads\NRC Missing (1).xlsx"
output_file = r"extracted_NRC.xlsx"

# NRC pattern:
# Example: 123456/78/1
NRC_PATTERN = r"\b\d{6}/\d{2}/\d\b"


# ============================================================
# EXTRACT NRCs
# ============================================================

all_nrcs = []

# Read all sheets
excel_file = pd.ExcelFile(input_file)

for sheet_name in excel_file.sheet_names:

    print(f"Processing sheet: {sheet_name}")

    df = pd.read_excel(
        input_file,
        sheet_name=sheet_name,
        header=None,
        dtype=str
    )

    # Check every cell
    for row in df.itertuples(index=False):

        for cell in row:

            if pd.isna(cell):
                continue

            cell = str(cell)

            # Find NRCs inside the cell
            matches = re.findall(NRC_PATTERN, cell)

            all_nrcs.extend(matches)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

all_nrcs = list(dict.fromkeys(all_nrcs))


# ============================================================
# CREATE OUTPUT
# ============================================================

output_df = pd.DataFrame({
    "NRC": all_nrcs
})

output_df.to_excel(
    output_file,
    index=False
)


print("\n===================================")
print("Extraction completed!")
print(f"Total NRCs found: {len(all_nrcs)}")
print(f"Output file: {output_file}")
print("===================================")
