import customtkinter as ctk
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image
from datetime import datetime

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# App window
app = ctk.CTk()
app.title("Automated Data Report Generator")
app.geometry("900x600")

# Global data
data = None
chart_canvas = None  # to manage chart updates

# Title
title = ctk.CTkLabel(app, text="Automated Report Generator", font=("Arial", 24))
title.pack(pady=20)

# Frames
control_frame = ctk.CTkFrame(app)
control_frame.pack(pady=10, padx=20, fill="x")

output_frame = ctk.CTkFrame(app)
output_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Output box
output_text = ctk.CTkTextbox(output_frame, height=150)
output_text.pack(fill="x", padx=10, pady=10)

# Chart area (separate from text)
chart_frame = ctk.CTkFrame(output_frame)
chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Dropdown
dropdown = ctk.CTkOptionMenu(control_frame, values=["No Data"])
dropdown.pack(side="left", padx=10)

# Functions
def upload_file():
    global data

    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:
        data = pd.read_csv(file_path)

        # Update dropdown dynamically
        columns = list(data.columns)
        dropdown.configure(values=columns)
        dropdown.set(columns[0])

        # Show preview
        output_text.delete("1.0", "end")
        output_text.insert("end", "File loaded successfully!\n\nPreview:\n\n")
        output_text.insert("end", data.head().to_string(index=False))


def generate_report():
    global data

    if data is None:
        output_text.delete("1.0", "end")
        output_text.insert("end", "Please upload a dataset first.")
        return

    selected_metric = dropdown.get()

    output_text.delete("1.0", "end")
    output_text.insert("end", f"Generating report for: {selected_metric}\n\n")

    if selected_metric in data.columns:
        output_text.insert("end", f"Mean: {data[selected_metric].mean():.2f}\n")
        output_text.insert("end", f"Max: {data[selected_metric].max()}\n")
        output_text.insert("end", f"Min: {data[selected_metric].min()}\n")
        output_text.insert("end", "\nInsights:\n")
        output_text.insert("end", generate_insights(selected_metric))

        show_chart(selected_metric)
    else:
        output_text.insert("end", "Selected column not found in dataset.")


def show_chart(column):
    global chart_canvas

    # Clear previous chart
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(5, 3))

    # 🔥 Check if column is numeric
    if pd.api.types.is_numeric_dtype(data[column]):
        data[column].plot(kind='hist', bins=10, ax=ax)
        ax.set_title(f"{column} Distribution (Histogram)")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
    else:
        data[column].value_counts().head(10).plot(kind='bar', ax=ax)
        ax.set_title(f"{column} Distribution (Top Categories)")
        ax.set_xlabel(column)
        ax.set_ylabel("Count")

    chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(fill="both", expand=True)

def generate_insights(column):
    if not pd.api.types.is_numeric_dtype(data[column]):
        return "Insights available only for numeric data."

    mean = data[column].mean()
    median = data[column].median()

    insight = ""

    # Basic interpretation
    if mean < 3:
        insight += "Low average values observed.\n"
    elif mean < 7:
        insight += "Moderate average values observed.\n"
    else:
        insight += "High average values observed.\n"

    # Skewness check
    if mean > median:
        insight += "Data is slightly right-skewed.\n"
    elif mean < median:
        insight += "Data is slightly left-skewed.\n"
    else:
        insight += "Data is fairly symmetric.\n"

    return insight

def export_report():
    global data
    

    if data is None:
        output_text.insert("end", "\nPlease upload data first.")
        return

    selected_metric = dropdown.get()

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    if selected_metric not in data.columns:
        output_text.insert("end", "\nInvalid column selected.")
        return

    # Calculations
    mean = data[selected_metric].mean()
    max_val = data[selected_metric].max()
    min_val = data[selected_metric].min()

    insights = generate_insights(selected_metric)

    # 🔥 Step 1: Save chart as image
    chart_path = "temp_chart.png"

    plt.figure(figsize=(6, 4))

    if pd.api.types.is_numeric_dtype(data[selected_metric]):
        data[selected_metric].plot(kind='hist', bins=10)
        plt.title(f"{selected_metric} Distribution")
    else:
        data[selected_metric].value_counts().head(10).plot(kind='bar')
        plt.title(f"{selected_metric} Top Categories")

    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    # 🔥 Step 2: Create PDF
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")

    content = []

    # 🔥 New Header (replace old title)
    content.append(Paragraph("Automated Data Report Generator", styles["Title"]))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"<i>Generated on: {current_time}</i>", styles["Normal"]))
    content.append(Spacer(1, 15))

    # Optional divider
    content.append(Paragraph("=" * 60, styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Selected Metric:</b> {selected_metric}", styles["Normal"]))
    content.append(Paragraph(f"<b>Total Records:</b> {len(data)}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>STATISTICAL SUMMARY</b>", styles["Heading2"]))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"Mean Value: {mean:.2f}", styles["Normal"]))
    content.append(Paragraph(f"Maximum Value: {max_val}", styles["Normal"]))
    content.append(Paragraph(f"Minimum Value: {min_val}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>INSIGHTS</b>", styles["Heading2"]))
    content.append(Spacer(1, 5))
    content.append(Paragraph(insights.replace("\n", "<br/>"), styles["Normal"]))
    content.append(Spacer(1, 15))

    # 🔥 Step 3: Add chart to PDF
    content.append(Paragraph("<b>VISUALIZATION</b>", styles["Heading2"]))
    content.append(Spacer(1, 10))
    content.append(Image(chart_path, width=400, height=250))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Generated by Automated Report Generator", styles["Italic"]))

    doc.build(content)

    output_text.insert("end", "\nPDF report with chart exported successfully.")


# Buttons (YOU MISSED THESE 🔥)
upload_btn = ctk.CTkButton(control_frame, text="Upload CSV", command=upload_file)
upload_btn.pack(side="left", padx=10, pady=10)

generate_btn = ctk.CTkButton(control_frame, text="Generate Report", command=generate_report)
generate_btn.pack(side="left", padx=10, pady=10)

export_btn = ctk.CTkButton(control_frame, text="Export Report", command=export_report)
export_btn.pack(side="left", padx=10, pady=10)

# Run app
app.mainloop()