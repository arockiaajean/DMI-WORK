
import pandas as pd
from tqdm import tqdm

input_file = "all centre cleaned.csv"
output_file = "all result cleaned 2.csv"
chunk_size = 1000

# Count rows for the progress bar
print("Counting rows...")
with open(input_file, "r", encoding="utf-8-sig", newline="") as f:
    total_rows = sum(1 for _ in f) - 1

total_chunks = (max(total_rows, 0) + chunk_size - 1) // chunk_size

# Process the CSV in small batches
first_chunk = True

for df in tqdm(
    pd.read_csv(input_file, chunksize=chunk_size, encoding="utf-8-sig"),
    total=total_chunks,
    desc="Cleaning seventh column"
):
    if df.shape[1] < 7:
        raise ValueError("The CSV file has fewer than 7 columns.")

    # Remove all whitespace from the seventh column
    col = df.columns[6]
    df[col] = df[col].astype("string").str.replace(r"\s+", "", regex=True)

    # Write each batch to the output CSV
    df.to_csv(
        output_file,
        mode="w" if first_chunk else "a",
        index=False,
        header=first_chunk,
        encoding="utf-8"
    )

    first_chunk = False

print("Completed! Output saved to:", output_file)

