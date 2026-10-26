import pandas as pd
import re
from rapidfuzz import fuzz
from tqdm import tqdm

# ============================================================
# CONFIGURATION
# ============================================================

input_file = r"temp 2.xlsx"
output_file = r"temp 3.xlsx"

# Minimum score required to consider it a match
MATCH_THRESHOLD = 70


# ============================================================
# FUNCTION 1: CLEAN THE NAME
# ============================================================

def clean_name(name):
    """
    Converts a name into a standard format.
    """

    if pd.isna(name):
        return ""

    name = str(name).upper()

    # Remove special characters
    name = re.sub(r"[^A-Z\s]", " ", name)

    # Remove extra spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name


# ============================================================
# FUNCTION 2: CREATE NAME INFORMATION
# ============================================================

def name_parts(name):
    """
    Breaks a name into individual words.
    """

    name = clean_name(name)

    if not name:
        return []

    return name.split()


# ============================================================
# FUNCTION 3: CHECK NAME MATCH
# ============================================================

def compare_names(name1, name2):

    name1 = clean_name(name1)
    name2 = clean_name(name2)

    if not name1 or not name2:
        return 0

    parts1 = name_parts(name1)
    parts2 = name_parts(name2)

    # --------------------------------------------------------
    # Direct fuzzy comparison
    # --------------------------------------------------------

    score1 = fuzz.token_set_ratio(name1, name2)

    # --------------------------------------------------------
    # Compare initials
    # --------------------------------------------------------

    # Example:
    # SIMELENI CHIYOTA
    # S CHIYOTA

    initials1 = " ".join(word[0] for word in parts1)
    initials2 = " ".join(word[0] for word in parts2)

    initial_score = fuzz.ratio(initials1, initials2)

    # --------------------------------------------------------
    # Check whether the last name matches
    # --------------------------------------------------------

    last_score = 0

    if parts1 and parts2:

        last1 = parts1[-1]
        last2 = parts2[-1]

        last_score = fuzz.ratio(last1, last2)

    # --------------------------------------------------------
    # Check individual words
    # --------------------------------------------------------

    word_scores = []

    for word2 in parts2:

        best_score = 0

        for word1 in parts1:

            score = fuzz.ratio(word1, word2)

            if score > best_score:
                best_score = score

        word_scores.append(best_score)

    if word_scores:
        word_score = sum(word_scores) / len(word_scores)
    else:
        word_score = 0

    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    final_score = max(
        score1,
        word_score,
        (last_score * 0.7 + initial_score * 0.3)
    )

    return round(final_score)


# ============================================================
# READ EXCEL FILE
# ============================================================

print("Reading Excel file...")

df = pd.read_excel(input_file)

print(f"Total rows: {len(df):,}")


# ============================================================
# MAKE SURE THERE ARE AT LEAST 3 COLUMNS
# ============================================================

if len(df.columns) < 3:
    raise ValueError(
        "The Excel file must contain at least 3 columns."
    )


# ============================================================
# CREATE COLUMN E
# ============================================================

# Column B = index 1
# Column C = index 2
#
# We will create:
# Column E = Match Result

result_column = []


# ============================================================
# PROCESS ROWS
# ============================================================

for index, row in tqdm(
    df.iterrows(),
    total=len(df),
    desc="Matching names"
):

    # Column B
    name_column_2 = row.iloc[1]

    # Column C
    name_column_3 = row.iloc[2]

    # Compare names
    score = compare_names(
        name_column_2,
        name_column_3
    )

    # --------------------------------------------------------
    # Decide MATCH / NO MATCH
    # --------------------------------------------------------

    if score >= MATCH_THRESHOLD:

        result = f"MATCH - {score}"

    else:

        result = f"NO MATCH - {score}"

    result_column.append(result)


# ============================================================
# PUT RESULT INTO COLUMN E
# ============================================================

# If Column E already exists, replace it
# Otherwise create it

if len(df.columns) >= 5:

    df.iloc[:, 4] = result_column

else:

    # Add empty columns until Column E exists
    while len(df.columns) < 4:
        df[f"Extra_{len(df.columns)+1}"] = ""

    df["MATCH RESULT"] = result_column


# ============================================================
# SAVE FILE
# ============================================================

print("Saving output...")

df.to_excel(
    output_file,
    index=False
)

print()
print("========================================")
print("PROCESS COMPLETED")
print("========================================")
print(f"Input file : {input_file}")
print(f"Output file: {output_file}")
print("========================================")
