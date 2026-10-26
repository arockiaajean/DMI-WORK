import pandas as pd
from rapidfuzz import fuzz
from pathlib import Path

# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = r"temp.xlsx"
OUTPUT_FILE = r"temp2.xlsx"

# Keyword that must be found first
REQUIRED_KEYWORD = r"F:\documnets\PMEC"

# Locations to search for
LOCATIONS = [
    "CHIPATA",
    "LUSAKA",
    "KABWE",
    "KASAMA",
    "KITWE",
    "LIVINGSTON",
    "MANSA",
    "MONGU",
    "MPIKA",
    "SOLWEZI"
]

# Fuzzy matching threshold
# 90 = strict
# 85 = moderate
# 80 = more tolerant of spelling mistakes
FUZZY_THRESHOLD = 85


# ============================================================
# FUNCTION TO FIND LOCATION
# ============================================================

def find_location(row):
    """
    Search one Excel row.

    First:
        Check whether C:\\Users exists anywhere in the row.

    Then:
        Search for one of the location names,
        allowing spelling mistakes.
    """

    # Convert all cells in the row to text
    cells = []

    for value in row:
        if pd.notna(value):
            cells.append(str(value).upper())

    # --------------------------------------------------------
    # STEP 1: Check for C:\Users
    # --------------------------------------------------------

    required_found = any(
        REQUIRED_KEYWORD.upper() in cell
        for cell in cells
    )

    if not required_found:
        return ""

    # --------------------------------------------------------
    # STEP 2: Search for locations
    # --------------------------------------------------------

    found_locations = []

    for location in LOCATIONS:

        for cell in cells:

            # Exact match / keyword contained in cell
            if location in cell:
                found_locations.append(location)
                break

            # ------------------------------------------------
            # Fuzzy matching
            # ------------------------------------------------

            # Split cell into words
            words = cell.replace(",", " ").replace(
                ".", " "
            ).split()

            for word in words:

                score = fuzz.ratio(
                    location,
                    word
                )

                if score >= FUZZY_THRESHOLD:
                    found_locations.append(location)
                    break

            if location in found_locations:
                break

    # Remove duplicates while keeping order
    found_locations = list(dict.fromkeys(found_locations))

    # Return all locations found
    return ", ".join(found_locations)


# ============================================================
# READ EXCEL
# ============================================================

print("Reading Excel file...")

df = pd.read_excel(INPUT_FILE)

print(f"Rows found: {len(df)}")
print(f"Columns found: {len(df.columns)}")


# ============================================================
# CREATE NEW COLUMN A
# ============================================================

print("Searching rows...")

results = []

for index, row in df.iterrows():

    result = find_location(row)

    results.append(result)

    # Progress
    if (index + 1) % 1000 == 0:
        print(f"Processed {index + 1} rows...")


# ============================================================
# INSERT RESULT AS COLUMN A
# ============================================================

df.insert(
    0,
    "Location",
    results
)


# ============================================================
# SAVE NEW EXCEL FILE
# ============================================================

df.to_excel(
    OUTPUT_FILE,
    index=False
)

print()
print("========================================")
print("DONE")
print("========================================")
print(f"Output file: {OUTPUT_FILE}")
