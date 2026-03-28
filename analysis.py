def is_id_column(series):
    name = series.name.lower()

    # Strong keyword filtering
    id_keywords = [
        "id", "number", "no", "code",
        "order", "customer", "product",
        "ean", "index"
    ]

    for word in id_keywords:
        if word in name:
            return True

    # High uniqueness ratio (almost every row unique)
    unique_ratio = series.nunique() / len(series)
    if unique_ratio > 0.9:
        return True

    return False


def calculate_stats(df):
    
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.empty:
        raise ValueError("No numeric columns found in the dataset")

    # Remove ID-like columns
    valid_numeric = [
        col for col in numeric_df.columns
        if not is_id_column(numeric_df[col])
    ]

    if not valid_numeric:
        raise ValueError("Only identifier columns found. No meaningful data to analyze.")

    # -------- MULTI METRIC MODE --------
    if len(valid_numeric) > 1:
        averages = numeric_df[valid_numeric].mean()

        best_subject = averages.idxmax()
        worst_subject = averages.idxmin()

        stats = {
            "Mode": "Multi-Metric",
            "Analyzed Columns": valid_numeric,
            "Best Performing Metric": best_subject,
            "Best Average": round(averages.max(), 2),
            "Weakest Metric": worst_subject,
            "Weakest Average": round(averages.min(), 2)
        }

        return stats, valid_numeric

    # -------- SINGLE METRIC MODE --------
    target_column = valid_numeric[0]

    stats = {
        "Mode": "Single-Metric",
        "Analyzed Column": target_column,
        "Total": numeric_df[target_column].sum(),
        "Average": numeric_df[target_column].mean(),
        "Maximum": numeric_df[target_column].max(),
        "Minimum": numeric_df[target_column].min(),
    }

    return stats, target_column