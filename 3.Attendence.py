import os
import win32com.client

# to delete the 2nd page.
FOLDER_PATH = r"Generated_Attendance_Sheets mpika"

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

for root, dirs, files in os.walk(FOLDER_PATH):
    for file in files:
        if file.endswith(".docx") or file.endswith(".doc"):

            file_path = os.path.abspath(os.path.join(root, file))
            print("Processing:", file_path)

            try:
                doc = word.Documents.Open(file_path)

                pages = doc.ComputeStatistics(2)

                if pages >= 2:
                    # Go to start of page 2
                    start_range = doc.GoTo(What=1, Which=1, Count=2)  # wdGoToPage
                    
                    # Go to start of page 3 (end of page 2)
                    try:
                        end_range = doc.GoTo(What=1, Which=1, Count=3)
                        doc.Range(start_range.Start, end_range.Start).Delete()
                    except:
                        # If page 3 doesn't exist → delete till end of doc
                        doc.Range(start_range.Start, doc.Content.End).Delete()

                    doc.Save()
                    print("Deleted page 2:", file)

                else:
                    print("Skipped (only 1 page):", file)

                doc.Close()

            except Exception as e:
                print(f"Error with {file}: {e}")

word.Quit()

print("Done!")
