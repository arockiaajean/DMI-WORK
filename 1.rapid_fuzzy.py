# COMPARE TWO NAMES WITH DIFFERNT FILE.
import pandas as pd
from rapidfuzz import process, fuzz
from tqdm import tqdm
import re

# ============================================================
# 1. FILE NAMES
# ============================================================

FIRST_FILE = r"first_file.xlsx"
STUDENT_FILE = r"student_file.xlsx"
OUTPUT_FILE = r"matched_students.xlsx"


# ============================================================
# 2. COLUMN NAMES
# ============================================================

# Change these to match your actual Excel column names

FIRST_NAME_COLUMN = "Name"

STUDENT_NO_COLUMN = "Student No"
STUDENT_NAME_COLUMN = "Name"


# ============================================================
# 3. READ EXCEL FILES
# ============================================================

df_first = pd.read_excel(FIRST_FILE)
df_students = pd.read_excel(STUDENT_FILE)

print("First file rows:", len(df_first))
print("Student file rows:", len(df_students))


# ============================================================
# 4. CLEAN NAME FUNCTION
# ============================================================

def clean_name(name):
    """
    Makes names easier to compare.
    """

    if pd.isna(name):
        return ""

    name = str(name)

    # Convert to lowercase
    name = name.lower()

    # Remove extra spaces
    name = re.sub(r"\s+", " ", name)

    # Remove special characters
    name = re.sub(r"[^a-z\s]", "", name)

    # Remove spaces at beginning/end
    name = name.strip()

    return name


# ============================================================
# 5. CREATE CLEAN NAMES
# ============================================================

df_first["clean_name"] = df_first[FIRST_NAME_COLUMN].apply(clean_name)

df_students["clean_name"] = df_students[STUDENT_NAME_COLUMN].apply(clean_name)


# ============================================================
# 6. CREATE LIST OF STUDENT NAMES
# ============================================================

student_names = df_students["clean_name"].tolist()


# ============================================================
# 7. MATCH NAMES
# ============================================================

results = []

print("\nMatching names...")

for first_name, clean_first_name in tqdm(
    zip(
        df_first[FIRST_NAME_COLUMN],
        df_first["clean_name"]
    ),
    total=len(df_first)
):

    # If the name is empty
    if not clean_first_name:

        results.append({
            "Name from First File": first_name,
            "Matching Student No": "",
            "Name from Student File": "",
            "Score": 0
        })

        continue


    # Find the best matching student name
    match = process.extractOne(
        clean_first_name,
        student_names,
        scorer=fuzz.token_sort_ratio
    )


    # match contains:
    # match[0] = matched name
    # match[1] = score
    # match[2] = position/index


    matched_name = match[0]
    score = match[1]
    student_index = match[2]


    # Get student information
    student_no = df_students.iloc[student_index][STUDENT_NO_COLUMN]
    student_file_name = df_students.iloc[student_index][STUDENT_NAME_COLUMN]


    # Save result
    results.append({
        "Name from First File": first_name,
        "Matching Student No": student_no,
        "Name from Student File": student_file_name,
        "Score": round(score, 2)
    })


# ============================================================
# 8. CREATE OUTPUT DATAFRAME
# ============================================================

output_df = pd.DataFrame(results)


# ============================================================
# 9. SAVE RESULT
# ============================================================

output_df.to_excel(
    OUTPUT_FILE,
    index=False
)


print("\n====================================")
print("Matching completed!")
print("Output file:", OUTPUT_FILE)
print("Total names:", len(output_df))
print("====================================")
