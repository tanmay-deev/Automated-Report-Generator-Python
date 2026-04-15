import customtkinter as ctk
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyparsing import col
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
app.geometry("1000x700")
app.minsize(800, 600)

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
chart_frame = ctk.CTkScrollableFrame(output_frame)
chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
chart_frame.configure(height=400)
output_frame.pack_propagate(False)

# Dropdown
column_frame = ctk.CTkFrame(control_frame)
column_frame.pack(side="left", padx=10, pady=10, fill="y")
hint = ctk.CTkLabel(
    column_frame,
    text="(Select one or multiple)",
    font=("Arial", 10)
)
column_label = ctk.CTkLabel(
    column_frame,
    text="Select Columns",
    font=("Arial", 14, "bold")
)
hint.pack(anchor="w", padx=5)
column_label.pack(anchor="w", padx=5, pady=5)
scroll_frame = ctk.CTkScrollableFrame(column_frame, width=200, height=150)
scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

column_vars = {}

# Functions
def upload_file():
    global data

    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:
        data = pd.read_csv(file_path)

        
        # Clear old checkboxes
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        column_vars.clear()

        # Create checkboxes
        for col in data.columns:
            var = ctk.BooleanVar()

            chk = ctk.CTkCheckBox(
                scroll_frame,
                text=col,
                variable=var
            )
            chk.pack(anchor="w", padx=5, pady=2)

            column_vars[col] = var

        # Show preview
        output_text.delete("1.0", "end")
        output_text.insert("end", "File loaded successfully!\n\nPreview:\n\n")
        output_text.insert("end", data.head().to_string(index=False))

def get_selected_columns():
    return [col for col, var in column_vars.items() if var.get()]

def generate_report():
    global data

    if data is None:
        output_text.delete("1.0", "end")
        output_text.insert("end", "Please upload a dataset first.")
        return

    selected_columns = get_selected_columns()

    if not selected_columns:
        output_text.delete("1.0", "end")
        output_text.insert("end", "Please select at least one column.")
        return

    output_text.delete("1.0", "end")

    # 🔥 SINGLE METRIC MODE
    if len(selected_columns) == 1:
        col = selected_columns[0]

        output_text.insert("end", f"\n📊 {col.upper()}\n")
        output_text.insert("end", "-" * 25 + "\n")

        if pd.api.types.is_numeric_dtype(data[col]):
            output_text.insert("end", f"Mean: {data[col].mean():.2f}\n")
            output_text.insert("end", f"Max: {data[col].max()}\n")
            output_text.insert("end", f"Min: {data[col].min()}\n")

            output_text.insert("end", "Insights:\n")
            output_text.insert("end", generate_insights(col))

            show_chart(col)  # 🔥 use single chart

        else:
            output_text.insert("end", "Non-numeric column selected.\n")

    # 🔥 MULTI METRIC MODE
    else:
        for col in selected_columns:
            output_text.insert("end", f"\n📊 {col.upper()}\n")
            output_text.insert("end", "-" * 25 + "\n")

            if pd.api.types.is_numeric_dtype(data[col]):
                output_text.insert("end", f"Mean: {data[col].mean():.2f}\n")
                output_text.insert("end", f"Max: {data[col].max()}\n")
                output_text.insert("end", f"Min: {data[col].min()}\n")

                output_text.insert("end", "Insights:\n")
                output_text.insert("end", generate_insights(col) + "\n")
            else:
                output_text.insert("end", "Non-numeric column\n")

        show_individual_charts(selected_columns)

def show_chart(column):
    global chart_canvas

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(4, 5))

    if pd.api.types.is_numeric_dtype(data[column]):
        data[column].plot(kind='hist', bins=10, ax=ax)
        ax.set_title(f"{column} Distribution")
    else:
        data[column].value_counts().head(10).plot(kind='bar', ax=ax)

    chart_container = ctk.CTkFrame(chart_frame)
    chart_container.pack(pady=10)

    chart_canvas = FigureCanvasTkAgg(fig, master=chart_container)
    chart_canvas.draw()

    chart_canvas.get_tk_widget().pack()


def show_individual_charts(columns):
    # Clear old charts
    for widget in chart_frame.winfo_children():
        widget.destroy()

    numeric_cols = [col for col in columns if pd.api.types.is_numeric_dtype(data[col])]

    if not numeric_cols:
        ctk.CTkLabel(chart_frame, text="No numeric columns selected").pack()
        return

    for col in numeric_cols:
        fig, ax = plt.subplots(figsize=(6, 5))

        data[col].plot(kind='hist', bins=10, ax=ax)
        ax.set_title(f"{col} Distribution")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")

        # 🔥 MAIN ROW
        row_frame = ctk.CTkFrame(chart_frame)
        row_frame.pack(fill="x", pady=10, padx=10)

        # 🔥 LEFT → METRICS (fixed width)
        metrics_frame = ctk.CTkFrame(row_frame, width=220)
        metrics_frame.pack(side="left", fill="y", padx=10, pady=10)
        metrics_frame.pack_propagate(False)  # VERY IMPORTANT

        # Data
        mean = data[col].mean()
        max_val = data[col].max()
        min_val = data[col].min()
        insight = generate_insights(col)

        # Content
        ctk.CTkLabel(metrics_frame, text=col.upper(), font=("Arial", 12, "bold")).pack(anchor="w")
        ctk.CTkLabel(metrics_frame, text=f"Mean: {mean:.2f}").pack(anchor="w")
        ctk.CTkLabel(metrics_frame, text=f"Max: {max_val}").pack(anchor="w")
        ctk.CTkLabel(metrics_frame, text=f"Min: {min_val}").pack(anchor="w")
        ctk.CTkLabel(metrics_frame, text="Insights:", font=("Arial", 10, "bold")).pack(anchor="w")
        ctk.CTkLabel(metrics_frame, text=insight, wraplength=200, justify="left").pack(anchor="w")

        # 🔥 RIGHT → CHART (flexible)
        chart_container = ctk.CTkFrame(row_frame)
        chart_container.pack(side="left", padx=10, pady=10)

        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        
        canvas.get_tk_widget().pack(padx=10, pady=10)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        

# def show_multi_chart(columns):
#     # Clear previous charts
#     for widget in chart_frame.winfo_children():
#         widget.destroy()

#     numeric_cols = [col for col in columns if pd.api.types.is_numeric_dtype(data[col])]

#     if not numeric_cols:
#         label = ctk.CTkLabel(chart_frame, text="No numeric columns selected")
#         label.pack()
#         return

#     for col in numeric_cols:
#         fig, ax = plt.subplots(figsize=(5, 3))

#         # Histogram for each column
#         data[col].plot(kind='hist', bins=10, ax=ax)

#         ax.set_title(f"{col} Distribution")
#         ax.set_xlabel(col)
#         ax.set_ylabel("Frequency")

#         canvas = FigureCanvasTkAgg(fig, master=chart_frame)
#         canvas.draw()
#         canvas.get_tk_widget().pack(pady=10)

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

    selected_columns = get_selected_columns()

    if not selected_columns:
        output_text.insert("end", "\nPlease select at least one column.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    # 🔥 Prepare data
    report_data = []

    for col in selected_columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            report_data.append({
                "col": col,
                "mean": data[col].mean(),
                "max": data[col].max(),
                "min": data[col].min(),
                "insights": generate_insights(col)
            })

    # 🔥 Create chart (single or multi)
    chart_paths = []

    numeric_cols = []

    for col in selected_columns:
        try:
            pd.to_numeric(data[col])
            numeric_cols.append(col)
        except:
            pass

    for col in numeric_cols:
        chart_path = f"{col}_chart.png"

        # 🔥 Force numeric conversion
        temp_data = pd.to_numeric(data[col], errors='coerce')

        plt.figure(figsize=(6, 4))
        temp_data.dropna().plot(kind='hist', bins=10)

        plt.title(f"{col} Distribution")

        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()

        chart_paths.append(chart_path)

    # 🔥 Create PDF
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet
    from datetime import datetime

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")

    content = []

    # Header
    content.append(Paragraph("Automated Data Report Generator", styles["Title"]))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"<i>Generated on: {current_time}</i>", styles["Normal"]))
    content.append(Spacer(1, 15))

    content.append(Paragraph("=" * 60, styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Total Records:</b> {len(data)}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # 🔥 Loop for all metrics
    for item in report_data:
        content.append(Paragraph(f"<b>Metric:</b> {item['col']}", styles["Heading2"]))
        content.append(Spacer(1, 5))

        content.append(Paragraph(f"Mean: {item['mean']:.2f}", styles["Normal"]))
        content.append(Paragraph(f"Max: {item['max']}", styles["Normal"]))
        content.append(Paragraph(f"Min: {item['min']}", styles["Normal"]))
        content.append(Spacer(1, 5))

        content.append(Paragraph("Insights:", styles["Normal"]))
        content.append(Paragraph(item['insights'].replace("\n", "<br/>"), styles["Normal"]))
        content.append(Spacer(1, 10))

    # Chart
    content.append(Paragraph("<b>Visualization</b>", styles["Heading2"]))
    content.append(Spacer(1, 10))
    for path in chart_paths:
        content.append(Image(path, width=400, height=250))
        content.append(Spacer(1, 15))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Generated by Automated Report Generator", styles["Italic"]))

    doc.build(content)

    output_text.insert("end", "\nPDF report exported successfully.")


# Buttons (YOU MISSED THESE 🔥)
upload_btn = ctk.CTkButton(control_frame, text="Upload CSV", command=upload_file)
upload_btn.pack(side="left", padx=10, pady=10)

generate_btn = ctk.CTkButton(control_frame, text="Generate Report", command=generate_report)
generate_btn.pack(side="left", padx=10, pady=10)

export_btn = ctk.CTkButton(control_frame, text="Export Report", command=export_report)
export_btn.pack(side="left", padx=10, pady=10)

# Run app
app.mainloop()