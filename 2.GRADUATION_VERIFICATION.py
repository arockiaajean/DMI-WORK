import pymupdf  # PyMuPDF

input_pdf = r"CE 1.pdf"
output_pdf = r"CE T1.pdf"

doc = fitz.open(input_pdf)
new_doc = fitz.open()

# Define crop boxes (x0, y0, x1, y1)
# IMPORTANT: adjust if your coordinates represent different corners
crop_areas = [
    (496,32,572,120),   # from your points (assumed rectangle)
    (20,380,570,519)   # example second area (edit as needed)
]

for page in doc:
    for rect in crop_areas:
        x0, y0, x1, y1 = rect

        clip = fitz.Rect(x0, y0, x1, y1)

        # Create new page with same size as crop
        new_page = new_doc.new_page(width=clip.width, height=clip.height)

        # Copy cropped region into new page
        new_page.show_pdf_page(
            fitz.Rect(0, 0, clip.width, clip.height),
            doc,
            page.number,
            clip=clip
        )

new_doc.save(output_pdf)
new_doc.close()
doc.close()

print("Done! Cropped PDF saved.")
