import os
import shutil

# 1. Give the path of your main/root folder
source_folder = r"/home/ajean/Downloads/photo NOVE 2026 GRADUANDS"

# 2. Create the output folder called "All Photos"
output_folder = os.path.join(source_folder, "All Photos")
os.makedirs(output_folder, exist_ok=True)

# 3. Go through the main folder and all its subfolders
for root, folders, files in os.walk(source_folder):

    # 4. Don't search inside the "All Photos" folder itself
    if os.path.abspath(root) == os.path.abspath(output_folder):
        continue

    # 5. Go through every file found
    for file in files:

        # 6. Create the complete path of the original file
        source_file = os.path.join(root, file)

        # 7. Create the path where the copied file will go
        destination_file = os.path.join(output_folder, file)

        # 8. If the same filename already exists, create a new name
        if os.path.exists(destination_file):

            name, extension = os.path.splitext(file)
            number = 1

            while True:
                new_name = f"{name}_{number}{extension}"
                destination_file = os.path.join(output_folder, new_name)

                if not os.path.exists(destination_file):
                    break

                number += 1

        # 9. Copy the file
        shutil.copy2(source_file, destination_file)

        # 10. Show what was copied
        print(f"Copied: {source_file} -> {destination_file}")

print("\nFinished!")
print(f"All files are available in: {output_folder}")
