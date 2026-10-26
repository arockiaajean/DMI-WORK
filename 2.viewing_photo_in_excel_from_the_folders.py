import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from PIL import Image as PILImage

# ==============================
# SETTINGS
# ==============================
IMAGE_FOLDER = r"F:\NOV GRADUATION 2026 PHOTOS"      # <-- Change this
OUTPUT_FILE = "Images.xlsx"

CELL_WIDTH = 18
CELL_HEIGHT = 100

IMAGE_WIDTH = 120
IMAGE_HEIGHT = 100

# ==============================

wb = Workbook()
ws = wb.active
ws.title = "Photo List"

# Headers
ws["A1"] = "File Name"
ws["B1"] = "Photo"

# Column size
ws.column_dimensions["A"].width = 30
ws.column_dimensions["B"].width = CELL_WIDTH

row = 2

for filename in sorted(os.listdir(IMAGE_FOLDER)):

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        filepath = os.path.join(IMAGE_FOLDER, filename)

        # File name in Column A
        ws.cell(row=row, column=1).value = os.path.splitext(filename)[0]

        # Set row height
        ws.row_dimensions[row].height = CELL_HEIGHT

        # Insert image
        img = Image(filepath)

        # Resize image
        img.width = IMAGE_WIDTH
        img.height = IMAGE_HEIGHT

        # Put image exactly in B cell
        cell = f"B{row}"
        img.anchor = cell

        # Make image move and resize with cell
        img.placement = "moveAndSize"

        ws.add_image(img)

        row += 1


wb.save(OUTPUT_FILE)

print("Completed:", OUTPUT_FILE)
