from docx import Document
import os

def merge_docx(input_folder, output_file):
    # Create a new empty document (OUTPUT)
    merged_document = Document()

    # Get all .docx files from folder (INPUT)
    files = [f for f in os.listdir(input_folder) if f.endswith('.docx')]
    
    # Sort files (optional but recommended)
    files.sort()

    for index, file in enumerate(files):
        file_path = os.path.join(input_folder, file)
        sub_doc = Document(file_path)

        # Copy content
        for element in sub_doc.element.body:
            merged_document.element.body.append(element)

        # Add page break between documents (except last)
        if index < len(files) - 1:
            merged_document.add_page_break()

    # Save final merged file (OUTPUT)
    merged_document.save(output_file)


# 🔽 Example usage
input_folder = r"C:\Users\USER\Downloads\Sem 5 DONE"       # INPUT folder
output_file = r"SOLVESI 5.docx"      # OUTPUT file

merge_docx(input_folder, output_file)
print("done")
