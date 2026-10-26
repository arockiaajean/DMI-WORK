import openpyxl
import os


# ============================================================
# SETTINGS
# ============================================================

# Maximum width of a column when displaying results
MAX_COLUMN_WIDTH = 30


# ============================================================
# 1. GET EXCEL FILE
# ============================================================

input_file = input("Enter the Excel file path: ").strip()

# Remove quotation marks if the user copied the path with quotes
input_file = input_file.strip('"').strip("'")


# ============================================================
# 2. CHECK WHETHER FILE EXISTS
# ============================================================

if not os.path.isfile(input_file):
    print("\nERROR: File not found.")
    print("Please check the file path.")
    exit()


# ============================================================
# 3. GET SEARCH VALUE
# ============================================================

search_value = input("\nEnter what you want to search for: ").strip()

if search_value == "":
    print("\nERROR: Search value cannot be empty.")
    exit()


# Convert search value to lowercase
search_value = search_value.lower()


# ============================================================
# 4. OPEN EXCEL FILE
# ============================================================

print("\nOpening Excel file...")
print("Please wait...")

try:

    workbook = openpyxl.load_workbook(
        input_file,
        read_only=True,
        data_only=True
    )

except Exception as e:

    print("\nERROR: Could not open the Excel file.")
    print(e)
    exit()


print("Excel file opened successfully.")


# ============================================================
# 5. VARIABLES
# ============================================================

total_matches = 0


# ============================================================
# 6. SEARCH ALL SHEETS
# ============================================================

for sheet in workbook.worksheets:

    print(f"\nSearching: {sheet.title}")

    # Read rows one by one
    rows = sheet.iter_rows(values_only=True)

    # --------------------------------------------------------
    # Get the first row as headers
    # --------------------------------------------------------

    try:
        headers = next(rows)

    except StopIteration:
        # Empty sheet
        continue


    # Convert headers to readable text

    headers = [
        str(header) if header is not None else f"Column {i + 1}"
        for i, header in enumerate(headers)
    ]


    # --------------------------------------------------------
    # Search each row
    # --------------------------------------------------------

    for row_number, row in enumerate(rows, start=2):

        found = False


        # ----------------------------------------------------
        # Search every cell in the row
        # ----------------------------------------------------

        for cell in row:

            if cell is not None:

                cell_text = str(cell).lower()

                # Partial match
                if search_value in cell_text:

                    found = True
                    break


        # ----------------------------------------------------
        # If this row contains the search value
        # ----------------------------------------------------

        if found:

            total_matches += 1


            print("\n")
            print("=" * 100)

            print(f"Sheet : {sheet.title}")
            print(f"Row   : {row_number}")

            print("=" * 100)


            # =================================================
            # CREATE DISPLAY DATA
            # =================================================

            display_row = []

            for value in row:

                if value is None:
                    display_row.append("")
                else:
                    display_row.append(str(value))


            # -------------------------------------------------
            # Make sure headers and row have same length
            # -------------------------------------------------

            number_of_columns = max(
                len(headers),
                len(display_row)
            )


            while len(headers) < number_of_columns:
                headers.append(
                    f"Column {len(headers) + 1}"
                )


            while len(display_row) < number_of_columns:
                display_row.append("")


            # =================================================
            # CALCULATE COLUMN WIDTHS
            # =================================================

            column_widths = []


            for i in range(number_of_columns):

                header_length = len(headers[i])
                value_length = len(display_row[i])

                width = max(
                    header_length,
                    value_length
                )

                # Limit very long columns
                width = min(
                    width,
                    MAX_COLUMN_WIDTH
                )

                column_widths.append(width)


            # =================================================
            # PRINT HEADERS
            # =================================================

            header_line = ""

            for i in range(number_of_columns):

                header = headers[i]

                # Cut long header
                header = header[:MAX_COLUMN_WIDTH]

                header_line += (
                    header.ljust(column_widths[i])
                    + " | "
                )


            print(header_line)


            # =================================================
            # PRINT SEPARATOR
            # =================================================

            separator = ""

            for width in column_widths:

                separator += (
                    "-" * width
                    + "-+-"
                )


            print(separator)


            # =================================================
            # PRINT MATCHING ROW
            # =================================================

            row_line = ""

            for i in range(number_of_columns):

                value = display_row[i]

                # Cut very long values
                if len(value) > MAX_COLUMN_WIDTH:

                    value = (
                        value[:MAX_COLUMN_WIDTH - 3]
                        + "..."
                    )


                row_line += (
                    value.ljust(column_widths[i])
                    + " | "
                )


            print(row_line)


# ============================================================
# 7. CLOSE WORKBOOK
# ============================================================

workbook.close()


# ============================================================
# 8. FINAL RESULT
# ============================================================

print("\n")
print("=" * 100)

print(f"TOTAL MATCHING ROWS: {total_matches}")

print("=" * 100)


if total_matches == 0:

    print("\nNo matching rows were found.")

else:

    print(
        f"\nSearch completed. "
        f"{total_matches} matching row(s) found."
    )
