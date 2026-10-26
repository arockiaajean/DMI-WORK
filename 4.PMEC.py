#convert txt to csc and add the date and merge with old data base
import re
import csv

# Ask the user to enter the input TXT file path
input_file = input("Enter the TXT file path: ").strip()

# Output CSV file
output_file = "E956_payroll.csv"

# The four columns we want to keep
headers = [
    "Employee Number",
    "Name",
    "NRC Number",
    "Total (K)"
]

# Pattern to identify employee records
pattern = re.compile(
    r"^\s*(\d{8})\s+(\d{8})\s+(.*?)\s+"
    r"(\d{6}/\d{2}/\d)\s+(.*?)\s+(\d{6})\s+"
    r"([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+(\d+)\s+(\d+)\s*$"
)

with open(input_file, "r", encoding="utf-8", errors="replace") as txt_file, \
     open(output_file, "w", newline="", encoding="utf-8-sig") as csv_file:

    writer = csv.writer(csv_file)
    writer.writerow(headers)

    for line in txt_file:
        # Remove the outer | symbols
        line = line.strip().strip("|")

        # Skip short lines and headings
        if len(line) <= 38:
            continue

        # Employee data starts after the area and sub-area fields
        employee_data = line[38:]

        match = pattern.match(employee_data)

        if match:
            employee_number = match.group(1)
            name = match.group(3).strip()
            nrc_number = match.group(4)
            total = match.group(8).replace(",", "")

            writer.writerow([
                employee_number,
                name,
                nrc_number,
                total
            ])

print("Conversion completed!")
print("Output file:", output_file)

import csv
import os

# Ask for the CSV file path
input_file = ("E956_payroll.csv")

# Ask for the two values
value_5 = input("Enter the value for the 5th column: ")
value_6 = input("Enter the value for the 6th column: ")

# Create the output file name
output_file = os.path.splitext(input_file)[0] + "_updated.csv"

# Read the CSV and write the updated file
with open(input_file, "r", newline="", encoding="cp1252") as infile:

    reader = csv.reader(infile)

    with open(output_file, "w", newline="", encoding="utf-8-sig") as outfile:

        writer = csv.writer(outfile)

        for row in reader:
            # Add values to columns 5 and 6
            row.extend([value_5, value_6])

            writer.writerow(row)

print("\nCompleted successfully!")
print("Output file:", output_file)

import csv
import os

# Ask for the paths of both CSV files
file_a = input("Enter the path of old CSV file: ").strip()
file_b = ("E956_payroll_updated.csv")

# Create the output file name
output_file = input("Enter the Latest all pmec detailts name: ").strip()

# Read both files and merge them
with open(file_a, "r", newline="", encoding="cp1252") as a, \
     open(file_b, "r", newline="", encoding="cp1252") as b, \
     open(output_file, "w", newline="", encoding="utf-8-sig") as out:

    reader_a = csv.reader(a)
    reader_b = csv.reader(b)
    writer = csv.writer(out)

    # Copy all rows from file A, including its header
    for row in reader_a:
        writer.writerow(row)

    # Skip the header of file B
    next(reader_b, None)

    # Append the remaining rows from file B
    for row in reader_b:
        writer.writerow(row)

print("\nFiles merged successfully!")
print("Output file:", output_file)

