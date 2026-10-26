import pandas as pd
import re
from datetime import datetime

# Load the Excel file
df = pd.read_excel("cleaned_results_with_comments.xlsx")  # replace with your file name
column_name = 'comment'  # replace with your actual column name

# Function to extract and standardize the date
def extract_and_format_date(text):
    if pd.isna(text):
        return ""
    
    # Find a date pattern: dd.mm.yyyy, dd.mm.yy, dd/mm/yyyy, dd/mm/yy
    match = re.search(r'(\d{2}[./]\d{2}[./]\d{2,4})', str(text))
    if match:
        date_str = match.group(1)
        # Replace . or / with - for uniformity
        date_str = date_str.replace('.', '-').replace('/', '-')
        # Parse the date, handle 2-digit years
        try:
            if len(date_str.split('-')[2]) == 2:  # e.g., 24 -> 2024
                date_obj = datetime.strptime(date_str, "%d-%m-%y")
            else:
                date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            return date_obj.strftime("%d-%m-%Y")
        except:
            return date_str
    return ""

# Apply the function to create a new column
df['Date'] = df[column_name].apply(extract_and_format_date)

# Save to a new Excel file
df.to_excel("output_with_standardized_dates.xlsx", index=False)
print("Dates extracted and standardized successfully!")

