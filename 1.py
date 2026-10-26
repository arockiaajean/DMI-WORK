import pandas as pd
import requests
import os
from tqdm import tqdm

# Excel file path
excel_file = r"photos.xlsx"

# Column containing photo URLs
url_column = "Photo_Link"   # Change to your column name

# Output folder
output_folder = "Downloaded_Photos"
os.makedirs(output_folder, exist_ok=True)

# Read Excel
df = pd.read_excel(excel_file)

# Download photos
for i, url in tqdm(enumerate(df[url_column], start=1), total=len(df)):
    try:
        if pd.isna(url):
            continue

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Get file extension
        ext = os.path.splitext(url.split("?")[0])[1]
        if not ext:
            ext = ".jpg"

        filename = os.path.join(output_folder, f"photo_{i}{ext}")

        with open(filename, "wb") as f:
            f.write(response.content)

    except Exception as e:
        print(f"Failed to download {url}: {e}")

print("Download completed!")