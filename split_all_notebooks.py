
from pathlib import Path
import json

# STEP 1: Change this to your folder path
folder_path = Path("/home/ajean/PY/PY")

# STEP 2: Find all Jupyter Notebook files in the folder
notebook_files = list(folder_path.glob("*.ipynb"))

if not notebook_files:
    print("No .ipynb files found in:", folder_path)

# STEP 3: Process each notebook
for notebook_file in notebook_files:

    print("\nProcessing:", notebook_file.name)

    # Read the notebook
    with open(notebook_file, "r", encoding="utf-8") as file:
        notebook = json.load(file)

    # Get notebook name without .ipynb
    notebook_name = notebook_file.stem

    # Get all cells
    cells = notebook.get("cells", [])

    # STEP 4: Split cells into separate Python files
    for serial_no, cell in enumerate(cells, start=1):

        # Get cell contents
        source = cell.get("source", "")

        if isinstance(source, list):
            source = "".join(source)

        # Convert Markdown cells to Python comments
        if cell.get("cell_type") != "code":
            source = "\n".join(
                "# " + line if line.strip() else "#"
                for line in source.splitlines()
            )

        # Create output filename
        output_file = folder_path / f"{serial_no}.{notebook_name}.py"

        # Save the cell
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(source)
            file.write("\n")

        print("Created:", output_file.name)

print("\nAll notebooks processed!")
