#filtered result


import os
import pandas as pd
# file for results
# path to your folder
main_folder = r"C:\Users\USER\Documents\centre data base"
# path to your master student list
master_file = r"all student.xlsx"

# load student numbers
master_df = pd.read_excel(master_file)
student_numbers = set(master_df.iloc[:, 0].astype(str))  # first column

# prepare final results
all_matches = []

# walk through all subfolders
for root, dirs, files in os.walk(main_folder):
    for file in files:
        if file.endswith((".xlsx", ".xls")):
            file_path = os.path.join(root, file)
            try:
                df = pd.read_excel(file_path, dtype=str)  # read as text

                # try to find the MODULE CODE row once per file
                module_code_row = None
                for _, row in df.iterrows():
                    row_text = " ".join(str(x) for x in row.values if pd.notna(x))
                    if "CODE" in row_text.upper():
                        module_code_row = list(row.values)
                        break

                # now check each row for student numbers
                for _, row in df.iterrows():
                    row_text = " ".join(str(x) for x in row.values if pd.notna(x))
                    found_sn = None
                    for sn in student_numbers:
                        if sn in row_text:
                            found_sn = sn
                            break
                    if found_sn:
                        # save student row
                        row_data = list(row.values)
                        row_data.append(file_path)  # keep file source
                        all_matches.append(row_data)

                        # save module code row (if found)
                        if module_code_row:
                            all_matches.append(module_code_row)
            except Exception as e:
                print(f"Skipping {file_path}: {e}")

# save results
if all_matches:
    result_df = pd.DataFrame(all_matches)
    #result_df.to_excel("FOUND THE NRC BY THE CENTRE final 200 10.09.2026 11.30 nrc.xlsx", index=False, header=False)
    result_df.to_csv("FOUND THE NRC BY THE CENTRE final 200 10.09.2026 11.30 nrc.csv", index=False, header=False)
    print("✅ Finished! Results saved in filtered_results.xlsx")
else:
    print("⚠️ No matching student numbers found.")

