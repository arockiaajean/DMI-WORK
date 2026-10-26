
from pathlib import Path

# Get the folder where this script is located
folder = Path(__file__).parent

# Find all Python files in this folder
for file in folder.glob("*.py"):

    # Replace spaces in the filename with underscores
    new_name = file.name.replace(" ", "_")

    # Rename only if the name needs changing
    if new_name != file.name:

        new_path = file.with_name(new_name)

        # Avoid overwriting an existing file
        if new_path.exists():
            print(f"Skipped: {new_name} already exists")
            continue

        file.rename(new_path)
        print(f"Renamed: {file.name} -> {new_name}")

print("Finished!")
