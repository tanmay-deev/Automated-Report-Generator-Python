def is_id_column(series):
    name = series.name.lower()
    if "id" in name or "ean" in name or "index" in name or "no" in name:
        return True

    unique_ratio = series.nunique() / len(series)
    if unique_ratio > 0.95:
        return True

    return False


def calculate_stats(df):
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.empty:
        raise ValueError("No numeric columns found in the dataset")

    valid_numeric = []
    for col in numeric_df.columns:
        if not is_id_column(numeric_df[col]):
            valid_numeric.append(col)

    # Fallback: if everything rejected, use best numeric anyway
    if not valid_numeric:
        valid_numeric = list(numeric_df.columns)

    target_column = numeric_df[valid_numeric].var().idxmax()

    if numeric_df[target_column].isna().all():
        raise ValueError("All numeric values are missing or invalid")

    stats = {
        "Analyzed Column": target_column,
        "Total": numeric_df[target_column].sum(),
        "Average": numeric_df[target_column].mean(),
        "Maximum": numeric_df[target_column].max(),
        "Minimum": numeric_df[target_column].min(),
    }

    return stats, target_column
