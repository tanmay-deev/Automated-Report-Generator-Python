def generate_summary(df, stats):
    rows, cols = df.shape
    column = stats["Analyzed Column"]

    column_lower = column.lower()

    # Guess domain
    if "percent" in column_lower or "mark" in column_lower or "score" in column_lower:
        domain = "student academic performance"
    elif "salary" in column_lower or "package" in column_lower:
        domain = "student placement and salary data"
    elif "sales" in column_lower or "revenue" in column_lower or "value" in column_lower:
        domain = "business and financial data"
    else:
        domain = "numerical data"

    avg = round(stats["Average"], 2)
    min_val = stats["Minimum"]
    max_val = stats["Maximum"]

    summary = (
        f"The uploaded dataset contains {rows} records and {cols} attributes. "
        f"It represents {domain}. "
        f"The analysis focuses on the '{column}' column. "
        f"The average value is {avg}, with values ranging from {min_val} to {max_val}. "
        f"This indicates a general overview of the dataset's central tendency and spread."
    )

    return summary
