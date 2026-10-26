import xlwings as xw

FILE_PATH = r"filtered_results_kitwe 24.04.2026 1.xlsx"   # <-- change this
SHEET_NAME = "Sheet1"           # <-- change if needed

ROWS = 2245

# Columns used in your macro (as Excel letters)
insert_cols = ["C", "H", "M", "R", "W", "AB", "AG", "AL", "AQ"]

def col_letter(col):
    return col

def run():
    app = xw.App(visible=False)
    wb = xw.Book(FILE_PATH)
    sht = wb.sheets[SHEET_NAME]

    # 1. Insert row 1
    sht.api.Rows(1).Insert()

    # 2. Delete column A
    sht.api.Columns("A").Delete()

    # 3. Process each column insertion + formula fill
    for col in insert_cols:
        sht.api.Columns(col).Insert()

        # put formula in row 2
        sht.range(f"{col}2").formula = f"=R[1]C[1]"

        # autofill down to row 2245
        sht.range(f"{col}2:{col}{ROWS}").formula = sht.range(f"{col}2").formula

    # 4. Convert all formulas to values (like Paste Special Values)
    used = sht.used_range
    used.value = used.value

    # 5. Apply filter (Column A blank)
    sht.api.Range(f"A1:BA{ROWS+2}").AutoFilter(Field=1, Criteria1="=")

    # 6. Delete visible rows except header
    last_row = sht.api.Cells(sht.api.Rows.Count, 1).End(-4162).Row

    for r in range(last_row, 2, -1):
        if sht.range(f"A{r}").value in (None, ""):
            sht.api.Rows(r).Delete()

    # remove filter
    sht.api.AutoFilterMode = False

    wb.save()
    wb.close()
    app.quit()

if __name__ == "__main__":
    run()
