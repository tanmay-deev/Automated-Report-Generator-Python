from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os


def generate_pdf(stats, summary_text, pdf_path="output/report.pdf"):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # -------- Page 1: Title --------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2*cm, height - 2*cm, "Automated Data Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(2*cm, height - 3*cm, "Generated using Python")

    # -------- Auto Summary --------
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2*cm, height - 5*cm, "Dataset Summary")

    c.setFont("Helvetica", 11)
    text_obj = c.beginText(2*cm, height - 6.5*cm)

    for line in summary_text.split(". "):
        text_obj.textLine(line.strip())

    c.drawText(text_obj)

    # -------- Stats --------
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2*cm, height - 11*cm, "Statistical Summary")

    c.setFont("Helvetica", 11)
    y = height - 12.5*cm

    for key, value in stats.items():
        c.drawString(2*cm, y, f"{key}: {value}")
        y -= 0.7*cm

    # -------- Page 2: Charts --------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 2*cm, "Data Visualizations")

    if stats["Mode"] == "Multi-Metric":

        img_path = "output/comparison.png"
        if os.path.exists(img_path):
            c.drawImage(
                img_path,
                2*cm,
                height - 12*cm,
                width=14*cm,
                height=8*cm
            )
        else:
            c.drawString(2*cm, height - 5*cm, "Comparison chart not available.")

    else:
        # -------- Histogram --------
        hist_path = "output/histogram.png"
        if os.path.exists(hist_path):
            c.drawImage(
                hist_path,
                2*cm,
                height - 9*cm,
                width=14*cm,
                height=6*cm
            )
        else:
            c.drawString(2*cm, height - 5*cm, "Histogram not available.")

        # -------- Boxplot --------
        box_path = "output/boxplot.png"
        if os.path.exists(box_path):
            c.drawImage(
                box_path,
                2*cm,
                height - 16*cm,
                width=10*cm,
                height=4*cm
            )
        else:
            c.drawString(2*cm, height - 12*cm, "Boxplot not available.")

        # -------- Category Page (optional) --------
        # Currently disabled because categories.png not generated
        # You can enable later when implemented

    c.save()