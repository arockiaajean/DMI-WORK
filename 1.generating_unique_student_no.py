import pandas as pd
from tqdm import tqdm

# ============================================================
# CONFIGURATION
# ============================================================

# File containing COMPLETE student numbers
complete_file = r"complete_students.xlsx"

# File containing INCOMPLETE student numbers
incomplete_file = r"incomplete_students.xlsx"

# Output file
output_file = r"completed_student_numbers.xlsx"


# ============================================================
# STEP 1: READ COMPLETE STUDENT NUMBERS
# ============================================================

print("Reading complete student numbers...")

complete_df = pd.read_excel(
    complete_file,
    dtype=str
)

# Take Column A
complete_numbers = complete_df.iloc[:, 0].fillna("").astype(str).str.strip()


# ============================================================
# STEP 2: CREATE A SET FOR FAST SEARCH
# ============================================================

# Set makes checking whether a student number exists very fast
used_numbers = set(complete_numbers)

print(f"Complete student numbers found: {len(used_numbers)}")


# ============================================================
# STEP 3: READ INCOMPLETE STUDENT NUMBERS
# ============================================================

print("Reading incomplete student numbers...")

incomplete_df = pd.read_excel(
    incomplete_file,
    dtype=str
)

incomplete_numbers = (
    incomplete_df.iloc[:, 0]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ============================================================
# STEP 4: GENERATE UNIQUE STUDENT NUMBERS
# ============================================================

results = []

print("Generating unique student numbers...")

for incomplete in tqdm(
    incomplete_numbers,
    total=len(incomplete_numbers),
    desc="Processing"
):

    # Skip empty cells
    if incomplete == "":
        results.append({
            "Incomplete Student No": "",
            "Completed Student No": ""
        })
        continue

    # Remove .0 if Excel has converted the number
    if incomplete.endswith(".0"):
        incomplete = incomplete[:-2]

    # We expect the incomplete number to have 9 digits
    if len(incomplete) != 9 or not incomplete.isdigit():

        results.append({
            "Incomplete Student No": incomplete,
            "Completed Student No": "INVALID"
        })

        continue

    # Start series from 01
    series = 1

    while True:

        # Create the 2-digit series
        series_number = f"{series:02d}"

        # Combine incomplete number + series
        candidate = incomplete + series_number

        # Check if candidate is already used
        if candidate not in used_numbers:

            # We found a unique number
            results.append({
                "Incomplete Student No": incomplete,
                "Completed Student No": candidate
            })

            # IMPORTANT:
            # Add it to used_numbers so it cannot be
            # generated again for another student.
            used_numbers.add(candidate)

            break

        # Already exists, try next series
        series += 1

        # Safety limit
        if series > 99:
            results.append({
                "Incomplete Student No": incomplete,
                "Completed Student No": "NO UNIQUE NUMBER"
            })
            break


# ============================================================
# STEP 5: CREATE OUTPUT DATAFRAME
# ============================================================

output_df = pd.DataFrame(results)


# ============================================================
# STEP 6: SAVE TO EXCEL
# ============================================================

output_df.to_excel(
    output_file,
    index=False
)

print()
print("==========================================")
print("PROCESS COMPLETED")
print("==========================================")
print(f"Output file: {output_file}")
print(f"Rows processed: {len(incomplete_numbers)}")
