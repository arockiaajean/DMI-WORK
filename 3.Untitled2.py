import pandas as pd
from docx import Document
import os

# 1. LOAD THE EXCEL FILES WITH SPECIFIC COLUMN NAMES
df_students = pd.read_excel('students.xlsx')
df_modules = pd.read_excel('MODULE DETAILS (2).xlsx')
df_supp = pd.read_excel('supp.xlsx')

def generate_hall_ticket(student_row):
    template_path = 'HALL TICKET.docx'
    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        return

    doc = Document(template_path)
    
    # Extract Student Info from Excel File 1
    reg_no = str(student_row['STUDENT NO'])
    name = student_row['STUDENT NAME']
    sem = str(student_row['SEMESTER'])
    prog_code = student_row['PROGRAM CODE']
    
    # Get Program Name from Excel File 2 using Program Code
    prog_match = df_modules[df_modules['PROGRAM CODE'] == prog_code]
    prog_name = prog_match['PROGRAM NAME'].iloc[0] if not prog_match.empty else "N/A"

    # 2. REPLACE HEADER PLACEHOLDERS 
    # This checks both paragraphs and tables for header placeholders
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if '<<REGISTER_NUMBER>>' in cell.text:
                    cell.text = cell.text.replace('<<REGISTER_NUMBER>>', reg_no)
                if '<<NAME>>' in cell.text:
                    cell.text = cell.text.replace('<<NAME>>', name)
                if '<<PROGRAMME>>' in cell.text:
                    cell.text = cell.text.replace('<<PROGRAMME>>', prog_name)
                if '<<SEMESTER>>' in cell.text:
                    cell.text = cell.text.replace('<<SEMESTER>>', sem)

    # 3. FILTER MODULES
    # Regular Modules (Excel File 2): Filter by Program Code AND Semester 
    reg_mods = df_modules[(df_modules['PROGRAM CODE'] == prog_code) & 
                          (df_modules['SEMESTER'] == int(sem))]
    
    # Supp Modules (Excel File 3): Filter by Student No 
    supp_mods = df_supp[df_supp['STUDENT NO'] == int(reg_no)]

    # 4. POPULATE THE MODULE TABLE 
    # Usually the module list is the second table in the document
    if len(doc.tables) > 1:
        module_table = doc.tables[1] 
    else:
        module_table = doc.tables[0]
    
    reg_list = reg_mods.values.tolist()
    supp_list = supp_mods.values.tolist()
    
    num_rows = max(len(reg_list), len(supp_list))
    
    # Fill existing rows starting from the third row (index 2) 
    for i in range(num_rows):
        if i + 2 < len(module_table.rows):
            row_cells = module_table.rows[i+2].cells
        else:
            row_cells = module_table.add_row().cells
            
        # Fill Regular Columns: Sem, Code, Name (Indices 0, 1, 2) 
        if i < len(reg_list):
            row_cells[0].text = str(reg_list[i][2])  # C3 SEMESTER
            row_cells[1].text = str(reg_list[i][0])  # C1 MODULE CODE
            row_cells[2].text = str(reg_list[i][1])  # C2 MODULE NAME
            
        # Fill Supp Columns: Sem (N/A), Code, Name (Indices 3, 4, 5) 
        if i < len(supp_list):
            row_cells[3].text = "SUPP"                # Indicating Supplementary
            row_cells[4].text = str(supp_list[i][2])  # C3 MODULE CODE
            row_cells[5].text = str(supp_list[i][3])  # C4 MODULE NAME

    # 5. SAVE THE INDIVIDUAL HALL TICKET
    output_name = f"Hall_Ticket_{reg_no}.docx"
    doc.save(output_name)
    print(f"Successfully generated: {output_name}")

# EXECUTION
for _, row in df_students.iterrows():
    generate_hall_ticket(row)
