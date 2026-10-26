#TO CHECK INDIVIDUALY
import pandas as pd

file_path = r"ALL PMEC 30_10_2026_corrected.csv"
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip()

df['AMOUNT'] = pd.to_numeric(df['AMOUNT'], errors='coerce')

# Keep DATE as datetime (DO NOT format yet)
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce', dayfirst=True)

search_value = input("Enter Employee No or NRC: ").strip()

filtered_df = df[
    (df['EMPLOYEE NO'].astype(str) == search_value) |
    (df['NRC'].astype(str) == search_value)
].copy()  # ✅ important to avoid warnings

if not filtered_df.empty:

    # ✅ Sort by date
    filtered_df = filtered_df.sort_values(by='DATE')

    print("\n--- Payment Records ---")

    # ✅ Format only for display
    display_df = filtered_df.copy()
    display_df['DATE'] = display_df['DATE'].dt.strftime('%d:%m:%Y')
    print(display_df)

    total_paid = filtered_df['AMOUNT'].sum()
    print("\nTotal Amount Paid:", total_paid)

    total_paid = filtered_df['AMOUNT'].sum()
    total_paid_after_deduction = total_paid * 0.975

    print("\nTotal Amount Paid after 2.5% deduction: {:.2f}".format(total_paid_after_deduction))

    # --- DATE LOGIC ---

    # Normalize to month start
    filtered_df['MONTH_START'] = filtered_df['DATE'].values.astype('datetime64[M]')

    start_date = filtered_df['MONTH_START'].min()
    end_date = filtered_df['MONTH_START'].max()

    print("\nStart Date:", start_date.date())
    print("End Date:", end_date.date())

    # Expected monthly dates
    expected_dates = pd.date_range(start=start_date, end=end_date, freq='MS')

    # Actual dates
    actual_dates = set(filtered_df['MONTH_START'])

    # Missing months
    missing_dates = sorted(set(expected_dates) - actual_dates)

    if missing_dates:
        print("\nMissing Payments (1st of each month expected):")
        for d in missing_dates:
            print(d.date())
        print("\nNumber of Missing Payments:", len(missing_dates))
    else:
        print("\nNo missing payments.")

else:
    print("No records found.")
