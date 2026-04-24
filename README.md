# Automated Data Report Generator

A Python-based application that analyzes datasets, generates insights, visualizes data, and exports structured PDF reports — all through an intuitive GUI.

---

## Features

* 📁 Upload CSV datasets
* 📊 Select one or multiple columns for analysis
* 📈 Automatic chart generation (Histogram, Boxplot, Comparison)
* 🧠 Insight generation (mean, skewness, trends)
* 📄 Export detailed PDF reports
* 🖥️ Interactive GUI built with CustomTkinter

---

## 🛠️ Tech Stack

* Python
* Pandas
* Matplotlib
* CustomTkinter
* ReportLab

---

## 📂 Project Structure

```
Automated_Report_Generator/
│
├── data/                     # Sample datasets
│
├── src/
│   ├── core/                # Backend logic
│   │   ├── analysis.py
│   │   ├── charts.py
│   │   ├── data_loader.py
│   │   ├── report.py
│   │   └── summary_generator.py
│   │
│   ├── gui/                 # GUI application
│   │   └── main_gui.py
│   │
│   └── main.py              # Entry point (optional)
│
├── output/                  # Generated reports & charts
│
├── tests/
│   └── test.py
│
├── README.md
└── requirements.txt
```

---

## Installation & Setup

### 1️. Clone the repository

```bash
git clone https://github.com/tanmay-deev/Automated-Report-Generator-Python.git
cd automated-report-generator
```

---

### 2️. Create virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3️. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Run GUI

```bash
python -m src.gui.main_gui
```

---

### Run test script (CLI)

```bash
python -m tests.test
```

---

## How It Works

1. Upload a dataset (CSV format)
2. Select columns for analysis
3. The system:

   * Cleans and processes data
   * Detects meaningful numeric columns
   * Generates statistics and insights
4. Visualizations are created automatically
5. Export results as a structured PDF report

---

## Key Concepts Used

* Data Cleaning & Preprocessing
* Statistical Analysis
* Data Visualization
* GUI Development
* PDF Report Generation

---

## 📌 Example Outputs

* Histogram (distribution of values)
* Boxplot (spread and outliers)
* Comparison charts (multi-metric analysis)
* Auto-generated insights

---

## Dependencies

```
pandas
matplotlib
customtkinter
reportlab
```

---

## Future Improvements

* Support for Excel & JSON files
* Advanced analytics (correlation, trends)
* Interactive charts
* Web-based version

---

## Author

**Tanmay Bonde**
BCA Student | Developer

---

## 📄 License

This project is for educational purposes. Feel free to use and modify it.

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub!
