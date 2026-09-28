import os
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_FOLDER = BASE_DIR / "static" / "exports"
EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)


def save_pdf(layout):
    """Compile comic panels and narration into a multi-page PDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 12, f"Panel {panel['panel']}: {panel['title']}", ln=True, align="C")

        image_path = panel["image_path"]
        if image_path.startswith("/static/"):
            image_path = image_path.replace("/static/", "static/", 1)

        absolute_image = BASE_DIR / image_path
        if absolute_image.exists():
            pdf.image(str(absolute_image), x=15, y=30, w=180)
            pdf.set_y(140)
        else:
            pdf.set_y(35)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 6, f"Image missing: {absolute_image}")

        pdf.set_font("Arial", "", 10)
        clean_text = panel.get("text", "")
        # FPDF's built-in Arial is intentionally used with ASCII-safe text.
        clean_text = clean_text.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 6, clean_text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = EXPORT_FOLDER / filename
    pdf.output(str(pdf_path))
    return f"/static/exports/{filename}"
