import pandas as pd
from docx import Document

# Load Excel files
students = pd.read_excel("students.xlsx")
modules = pd.read_excel("MODULE DETAILS (2).xlsx")
supp = pd.read_excel("supp.xlsx")

# Function to replace text
def replace_text(doc, placeholder, value):
    for para in doc.paragraphs:
        if placeholder in para.text:
            para.text = para.text.replace(placeholder, str(value))

# Loop through each student
for i, stu in students.iterrows():

    student_no = stu["StudentNo"]
    semester = stu["Semester"]
    program = stu["ProgramCode"]

    # Open template
    doc = Document("HALL TICKET.docx")

    # Basic details
    replace_text(doc, "<<REGISTER_NUMBER>>", student_no)
    replace_text(doc, "<<NAME>>", stu["NAME"])
    replace_text(doc, "<<SEMESTER>>", semester)
    replace_text(doc, "<<PROGRAMME>>", program)

    # -------------------------
    # 🎯 REGULAR SUBJECTS
    # -------------------------
    regular = modules[
        (modules["Semester"] == semester) &
        (modules["ProgramCode"] == program)
    ]

    # Fill first 5 modules (adjust based on template)
    for idx, row in enumerate(regular.head(5).itertuples(), start=0):
        replace_text(doc, f"<<MODULE_CODE{'' if idx==0 else idx}>>", row.ModuleCode)
        replace_text(doc, f"<<MODULE_NAME{'' if idx==0 else idx}>>", row._asdict()["ModuleName"])

    # -------------------------
    # 🎯 SUPPLEMENTARY SUBJECTS
    # -------------------------
    sup_data = supp[supp["StudentNo"] == student_no]

    for idx, row in enumerate(sup_data.head(5).itertuples(), start=0):
        replace_text(doc, f"<<MODULE CODE1{'' if idx==0 else idx}>>", row._asdict()["ModuleCode"])
        replace_text(doc, f"<<MODULE NAME1{'' if idx==0 else idx}>>", row._asdict()["ModuleName"])

    # Save file
    doc.save(f"HallTicket_{student_no}.docx")

print("✅ All hall tickets generated!")
