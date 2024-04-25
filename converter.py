from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def convert(input_folder, output_pdf=None):
    try:
        if not output_pdf:
            output_pdf = f"{input_folder}.pdf"

        c = canvas.Canvas(output_pdf, pagesize=letter)
        image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.tif')]

        for image_file in image_files:
            img_path = os.path.join(input_folder, image_file)
            img = Image.open(img_path)
            width, height = img.size
            aspect = height / float(width)
            img_width = 500
            img_height = img_width * aspect

            c.drawInlineImage(img_path, 50, 50, width=img_width, height=img_height)

            c.showPage()

        c.save()
        print("PDF created successfully.")
        return True

    except Exception:
        return False
        