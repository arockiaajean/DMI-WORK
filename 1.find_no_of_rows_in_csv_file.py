import csv

# Enter the path of your CSV file
file_path = "ALL PMEC 30_09_2026.csv"

# Open the CSV file
with open(file_path, "r", newline="", encoding="utf-8-sig") as file:

    # Read the CSV file
    reader = csv.reader(file)

    # Count the rows
    row_count = sum(1 for row in reader)

# Display the result
print("Total number of rows:", row_count)

