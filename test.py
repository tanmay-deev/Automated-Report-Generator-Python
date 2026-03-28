from data_loader import load_file
from analysis import calculate_stats
from charts import generate_charts
from report import generate_pdf
from summary_generator import generate_summary

try:
    data = load_file("marks-single-metric.csv")

    stats, column_used = calculate_stats(data)

    # First create summary text
    summary_text = generate_summary(data, stats)

    # Then generate charts (creates images)
    generate_charts(data, column_used)

    # Finally generate PDF (uses images + summary)
    generate_pdf(stats, summary_text)

    print("Report generated successfully")

except Exception as e:
    print("\n❌ Report generation failed")
    print("Reason:", e)
