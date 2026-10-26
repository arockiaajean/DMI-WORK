import pandas as pd
from tqdm import tqdm

# ==============================
# CONFIGURATION
# ==============================

input_file = r"temp.xlsx"
output_file = r"temp 1.xlsx"

# ==============================
# READ EXCEL FILE
# ==============================

df = pd.read_excel(input_file)

print("Original rows:", len(df))

# ==============================
# CHECK COLUMN 2
# ==============================

rows_to_keep = []

for index, row in tqdm(
    df.iterrows(),
    total=len(df),
    desc="Checking rows"
):
    column_2 = row.iloc[1]

    # Delete if Column 2 is empty
    if pd.isna(column_2) or str(column_2).strip() == "":
        continue

    # Delete if Column 2 is numeric
    if isinstance(column_2, (int, float)) and not isinstance(column_2, bool):
        continue

    # Otherwise keep the row
    rows_to_keep.append(index)

# ==============================
# CREATE CLEAN DATAFRAME
# ==============================

df_clean = df.loc[rows_to_keep]

# ==============================
# SAVE OUTPUT
# ==============================

df_clean.to_excel(output_file, index=False)

print()
print("Original rows :", len(df))
print("Remaining rows:", len(df_clean))
print("Deleted rows  :", len(df) - len(df_clean))
print("Output file   :", output_file)
