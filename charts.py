import matplotlib.pyplot as plt
import pandas as pd

def generate_charts(df, numeric_col):
    # ---------- Chart 1: Histogram ----------
    plt.figure(figsize=(7,5))
    df[numeric_col].dropna().plot(kind="hist", bins=12)
    plt.title(f"Distribution of {numeric_col}")
    plt.xlabel(numeric_col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("output/histogram.png")
    plt.close()

    # ---------- Chart 2: Box Plot ----------
    plt.figure(figsize=(5,4))
    plt.boxplot(df[numeric_col].dropna(), vert=False)
    plt.title(f"Box Plot of {numeric_col}")
    plt.xlabel(numeric_col)
    plt.tight_layout()
    plt.savefig("output/boxplot.png")
    plt.close()

    # ---------- Chart 3: Category-wise ----------
    categories = pd.cut(
        df[numeric_col],
        bins=[-float("inf"), 60, 75, 90, float("inf")],
        labels=["Low", "Average", "Good", "Excellent"]
    )

    category_counts = categories.value_counts().sort_index()

    plt.figure(figsize=(6,4))
    category_counts.plot(kind="bar")
    plt.title(f"Performance Categories based on {numeric_col}")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/categories.png")
    plt.close()
