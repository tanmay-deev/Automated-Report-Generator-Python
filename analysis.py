import pandas as pd

# ---------- Helper Function: Detect ID-like Columns ----------
def is_id_column(series):
    name = series.name.lower()

    # Keyword-based filtering
    id_keywords = [
        "id", "number", "no", "code",
        "order", "customer", "product",
        "ean", "index"
    ]

    for word in id_keywords:
        if word in name:
            return True

    # High uniqueness ratio (but avoid small dataset issue)
    unique_ratio = series.nunique() / len(series)
    if unique_ratio > 0.9 and series.nunique() > 20:
        return True

    return False


# ---------- Main Function ----------
def calculate_stats(df):

    # Step 1: Remove obvious non-analytical columns
    ignore_keywords = ["id", "year", "date"]

    valid_columns = [
        col for col in df.select_dtypes(include=['number']).columns
        if not any(word in col.lower() for word in ignore_keywords)
    ]

    # Use filtered numeric dataframe
    numeric_df = df[valid_columns]

    if numeric_df.empty:
        raise ValueError("No numeric columns found in the dataset")

    # Step 2: Remove ID-like columns based on data pattern
    valid_numeric = [
        col for col in numeric_df.columns
        if not is_id_column(numeric_df[col])
    ]

    if not valid_numeric:
        raise ValueError("Only identifier columns found. No meaningful data to analyze.")

    # ---------- MULTI METRIC MODE ----------
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

    # ---------- SINGLE METRIC MODE ----------
    target_column = valid_numeric[0]

    stats = {
        "Mode": "Single-Metric",
        "Analyzed Column": target_column,
        "Total": round(numeric_df[target_column].sum(), 2),
        "Average": round(numeric_df[target_column].mean(), 2),
        "Maximum": numeric_df[target_column].max(),
        "Minimum": numeric_df[target_column].min(),
    }

    return stats, target_column