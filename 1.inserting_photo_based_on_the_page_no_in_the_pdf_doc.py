import fitz
import os

PDF_FILE = r"C:\Users\USER\Downloads\TIME TABLE-week-2-APRIL 2026-new-final-updated.pdf"
PHOTO_FOLDER = r"C:\Users\USER\Pictures\graduant missing\New folder"
OUTPUT_FILE = r"temp.pdf"

# PHOTO POSITION
PHOTO_X = 430
PHOTO_Y = 95
PHOTO_WIDTH = 90
PHOTO_HEIGHT = 110

# Open PDF
pdf = fitz.open(PDF_FILE)

# Loop through pages
for page_number in range(len(pdf)):

    page = pdf[page_number]

    # page number starts from 1
    image_name = f"{page_number + 1}.png"

    image_path = os.path.join(PHOTO_FOLDER, image_name)

    if os.path.exists(image_path):

        rect = fitz.Rect(
            PHOTO_X,
            PHOTO_Y,
            PHOTO_X + PHOTO_WIDTH,
            PHOTO_Y + PHOTO_HEIGHT
        )

        page.insert_image(rect, filename=image_path)

        print(f"Inserted: {image_name}")

    else:
        print(f"Missing: {image_name}")

# Save final PDF
pdf.save(OUTPUT_FILE)
pdf.close()

print("DONE")
