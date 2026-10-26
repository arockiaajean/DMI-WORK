import pandas as pd

# ==============================
# CONFIGURATION
# ==============================

input_file = r"ALL CENTRE STUDENT NO AND NAME UPTO APRIL 2026 EXAM.xlsx"
output_file = r"temp.xlsx"

# ==============================
# READ EXCEL FILE
# ==============================

df = pd.read_excel(input_file)

# ==============================
# COPY COLUMN B AND C
# ==============================

new_df = df.iloc[:, 1:3].copy()

# ==============================
# SAVE AS NEW EXCEL FILE
# ==============================

new_df.to_excel(output_file, index=False)

print("Done!")
print("New file created:", output_file)
