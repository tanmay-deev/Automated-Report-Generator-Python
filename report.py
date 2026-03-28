from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

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
    # -------- Charts Section --------
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 2*cm, "Data Visualizations")

    if stats["Mode"] == "Multi-Metric":

        # Only comparison chart
        c.drawImage(
            "output/comparison.png",
            2*cm,
            height - 12*cm,
            width=14*cm,
            height=8*cm
        )

    else:
        # Single metric charts
        c.drawImage(
            "output/histogram.png",
            2*cm,
            height - 9*cm,
            width=14*cm,
            height=6*cm
        )

        c.drawImage(
            "output/boxplot.png",
            2*cm,
            height - 16*cm,
            width=10*cm,
            height=4*cm
        )

        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2*cm, height - 2*cm, "Category-wise Analysis")

        # c.drawImage(
        #     "output/categories.png",
        #     2*cm,
        #     height - 14*cm,
        #     width=12*cm,
        #     height=8*cm
        # )

    c.save()
