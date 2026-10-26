import pandas as pd
from tqdm import tqdm

# ==============================
# FILE SETTINGS
# ==============================

input_file = r"ALL CENTRE STUDENT NO AND NAME UPTO APRIL 2026 EXAM.xlsx"
output_file = r"temp.xlsx"


# ==============================
# READ EXCEL FILE
# ==============================

print("Reading Excel file...")
df = pd.read_excel(input_file)

print(f"Total rows: {len(df)}")


# ==============================
# CHECK COLUMN B
# ==============================

keep_rows = []

for index, row in tqdm(
    df.iterrows(),
    total=len(df),
    desc="Checking Column B"
):
    value = row.iloc[1]   # Column B

    # Keep the row if Column B is not blank
    if pd.notna(value) and str(value).strip() != "":
        keep_rows.append(index)


# ==============================
# KEEP ONLY VALID ROWS
# ==============================

df_cleaned = df.loc[keep_rows]


# ==============================
# SAVE FILE
# ==============================

df_cleaned.to_excel(output_file, index=False)

print("\nDone!")
print(f"Original rows : {len(df)}")
print(f"Remaining rows: {len(df_cleaned)}")
print(f"Deleted rows  : {len(df) - len(df_cleaned)}")
print(f"Output file   : {output_file}")
