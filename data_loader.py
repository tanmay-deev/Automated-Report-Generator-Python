import pandas as pd
import os

def load_file(filepath):
    ext = os.path.splitext(filepath)[1]

    if ext == ".csv":
        try:
            df = pd.read_csv(filepath, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, encoding="latin1")
    elif ext == ".xlsx":
        df = pd.read_excel(filepath)
    elif ext == ".xls":
        df = pd.read_excel(filepath)
    elif ext == ".tsv":
        df = pd.read_csv(filepath, sep="\t")
    elif ext == ".txt":
        df = pd.read_csv(filepath)
    else:
        raise Exception("Unsupported file format")

    # Only try to convert columns that look numeric
    for col in df.columns:
        if df[col].dtype == object:
            temp = df[col].astype(str).str.replace(",", "")
            numeric_version = pd.to_numeric(temp, errors="coerce")

            # If more than 50% values are numeric → keep numeric
            if numeric_version.notna().mean() > 0.5:
                df[col] = numeric_version

    return df
