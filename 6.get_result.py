
import csv
from tqdm import tqdm

input_file = r"all result cleaned 3.csv"
output_file = r"removed duplicates of 7th column.csv"

# Count rows for the progress bar
with open(input_file, "r", encoding="utf-8-sig", newline="") as file:
    total_rows = sum(1 for _ in file)

seen = set()
unique_count = 0
duplicate_count = 0

with open(input_file, "r", encoding="utf-8-sig", newline="") as infile, \
     open(output_file, "w", encoding="utf-8-sig", newline="") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in tqdm(reader, total=total_rows, desc="Processing CSV"):
        if len(row) < 7:
            continue

        value = row[6].strip()

        if value not in seen:
            seen.add(value)
            writer.writerow([value])
            unique_count += 1
        else:
            duplicate_count += 1

print("\nProcessing completed!")
print("Unique values saved:", unique_count)
print("Duplicate values removed:", duplicate_count)
print("Output file:", output_file)

