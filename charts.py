import os
import matplotlib.pyplot as plt

def generate_charts(df, columns):
    os.makedirs("output", exist_ok=True)

    # If multiple columns → comparison chart
    if isinstance(columns, list):

        averages = df[columns].mean()

        plt.figure(figsize=(8,5))
        averages.plot(kind='bar')
        plt.title("Average Comparison Across Metrics")
        plt.ylabel("Average Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("output/comparison.png")
        plt.close()

    else:
        # Single metric mode

        # -------- Histogram --------
        plt.figure(figsize=(7,5))
        df[columns].dropna().plot(kind="hist", bins=12)
        plt.title(f"Distribution of {columns}")
        plt.xlabel(columns)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig("output/histogram.png")
        plt.close()

        # -------- Boxplot (FIX) --------
        plt.figure(figsize=(6,4))
        df[columns].dropna().plot(kind="box")
        plt.title(f"Boxplot of {columns}")
        plt.tight_layout()
        plt.savefig("output/boxplot.png")
        plt.close()