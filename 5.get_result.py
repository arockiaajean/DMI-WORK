
import csv
from tqdm import tqdm

input_file = r"all result cleaned 2.csv"
output_file = r"all result cleaned 3.csv"

# First pass: count rows for the progress bar
with open(input_file, "r", encoding="utf-8-sig", newline="") as file:
    total_rows = sum(1 for _ in file)

# Second pass: filter rows
kept = 0
deleted = 0

with open(input_file, "r", encoding="utf-8-sig", newline="") as infile, \
     open(output_file, "w", encoding="utf-8-sig", newline="") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in tqdm(reader, total=total_rows, desc="Processing CSV"):
        # Keep rows that have at least 7 columns
        if len(row) < 7:
            writer.writerow(row)
            kept += 1
            continue

        # Delete row if 7th column has more than 2 characters
        if len(row[6].strip()) > 2:
            deleted += 1
        else:
            writer.writerow(row)
            kept += 1

print("\nProcessing completed!")
print("Rows kept:", kept)
print("Rows deleted:", deleted)
print("Output saved to:", output_file)

