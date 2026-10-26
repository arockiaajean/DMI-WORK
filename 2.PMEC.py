#REMOVE DUPLICATE AND SUMIF
import csv
from collections import defaultdict

# 1. Give the location of your CSV file
input_file = "ALL PMEC 30_10_2026_corrected.csv"

# 2. Name of the output file
output_file = "PMEC sumif.csv"

# 3. Change to True if your CSV has column headings
HAS_HEADER = False

# 4. Store the totals for each unique value in column 3
totals = defaultdict(float)

# Keep the original order of unique values
unique_values = []

# 5. Read the original CSV file
with open(input_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.reader(file)

    # Skip the heading row if one exists
    if HAS_HEADER:
        next(reader, None)

    for row in reader:

        # Skip rows that have fewer than 4 columns
        if len(row) < 4:
            continue

        # Get the value from column 3
        key = row[2].strip()

        # Get the number from column 4
        try:
            amount = float(row[3].replace(",", "").strip())
        except ValueError:
            continue

        # Remember each unique value only once
        if key not in totals:
            unique_values.append(key)

        # SUMIF: add column 4 for matching column 3 values
        totals[key] += amount

# 6. Save the result in a new CSV file
with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    writer.writerow(["Column 3 - Unique Value", "Sum of Column 4"])

    for key in unique_values:
        writer.writerow([key, totals[key]])

print("Finished successfully!")
print("Output saved to:", output_file)
print("Number of unique values:", len(unique_values))

