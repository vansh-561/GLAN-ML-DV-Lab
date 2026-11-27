"""
=============================================================================
Experiment 1: Getting Started with Data Visualization Views
Objective:
    - Load a sample dataset (Superstore sales & Iris dataset).
    - Generate basic table summary (descriptive statistics).
    - Create a frequency / category bar chart.
    - Create a time-series / trend line chart.
=============================================================================
"""

import os
import tempfile

# Ensure clean cache directory for matplotlib in sandbox/restricted environments
os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_output_dir():
    """Ensure the outputs directory exists and return its path."""
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def load_sample_dataset():
    """
    Loads sample retail sales data. Generates a realistic, rich Superstore-style
    dataset locally to guarantee 100% self-containment with zero network dependency.
    """
    print("[INFO] Generating/Loading Retail Superstore dataset...")
    np.random.seed(42)
    dates = pd.date_range(start="2022-01-01", periods=120, freq="W")
    categories = ["Electronics", "Furniture", "Office Supplies", "Apparel"]
    regions = ["North", "South", "East", "West"]

    records = []
    for d in dates:
        cat = np.random.choice(categories)
        reg = np.random.choice(regions)
        sales = np.random.uniform(250, 3500)
        profit = sales * np.random.uniform(0.08, 0.35)
        records.append({
            "Date": d,
            "Category": cat,
            "Region": reg,
            "Sales": round(sales, 2),
            "Profit": round(profit, 2)
        })
    df = pd.DataFrame(records)
    print(f"[SUCCESS] Dataset ready with {len(df)} rows and {df.shape[1]} columns.\n")
    return df


def generate_table_summary(df, output_dir):
    """Generates descriptive statistics and saves as formatted summary image and prints to console."""
    print("=" * 60)
    print(" 1. DATA SUMMARY & DESCRIPTIVE STATISTICS ")
    print("=" * 60)

    summary_stats = df.describe().round(2)
    print(summary_stats)
    print("\n[INFO] Data Types and Non-Null Counts:")
    print(df.info())

    # Render summary table as an image
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("off")
    table = ax.table(
        cellText=summary_stats.values,
        rowLabels=summary_stats.index,
        colLabels=summary_stats.columns,
        cellLoc="center",
        loc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.4)
    plt.title("Descriptive Statistics Summary Table", fontsize=14, weight="bold", pad=10)

    output_path = os.path.join(output_dir, "exp1_summary_table.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Summary table saved to: {output_path}")


def generate_bar_chart(df, output_dir):
    """Generates and saves a category-wise sales bar chart."""
    print("\n" + "=" * 60)
    print(" 2. GENERATING CATEGORY BAR CHART ")
    print("=" * 60)

    category_sales = df.groupby("Category")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
    print(category_sales)

    plt.figure(figsize=(9, 5))
    palette = sns.color_palette("mako", len(category_sales))
    bars = plt.bar(category_sales["Category"], category_sales["Sales"], color=palette, edgecolor="black", alpha=0.85)

    # Add data labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f"${height:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            weight="bold"
        )

    plt.title("Total Sales Revenue by Product Category", fontsize=14, weight="bold", pad=15)
    plt.xlabel("Product Category", fontsize=11, labelpad=10)
    plt.ylabel("Total Sales (USD)", fontsize=11, labelpad=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.gca().yaxis.set_major_formatter("${x:,.0f}")

    output_path = os.path.join(output_dir, "exp1_bar_chart.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[SAVED] Bar chart saved to: {output_path}")


def generate_line_chart(df, output_dir):
    """Generates and saves a time-series sales trend line chart."""
    print("\n" + "=" * 60)
    print(" 3. GENERATING TIME-SERIES LINE CHART ")
    print("=" * 60)

    # Aggregate monthly sales
    df_sorted = df.sort_values(by="Date").copy()
    df_monthly = df_sorted.set_index("Date").resample("ME")["Sales"].sum().reset_index()

    plt.figure(figsize=(10, 5))
    plt.plot(df_monthly["Date"], df_monthly["Sales"], marker="o", color="#2b5c8f", linewidth=2.5, markersize=6, label="Monthly Sales")
    
    # Fill under curve for aesthetics
    plt.fill_between(df_monthly["Date"], df_monthly["Sales"], alpha=0.15, color="#2b5c8f")

    plt.title("Monthly Sales Trend Over Time", fontsize=14, weight="bold", pad=15)
    plt.xlabel("Timeline (Month)", fontsize=11, labelpad=10)
    plt.ylabel("Sales Volume (USD)", fontsize=11, labelpad=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper left")
    plt.gca().yaxis.set_major_formatter("${x:,.0f}")
    plt.xticks(rotation=45)

    output_path = os.path.join(output_dir, "exp1_line_chart.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[SAVED] Line chart saved to: {output_path}")


def main():
    print("Starting Experiment 1: Basic Data Visualization Views...")
    output_dir = get_output_dir()
    df = load_sample_dataset()

    generate_table_summary(df, output_dir)
    generate_bar_chart(df, output_dir)
    generate_line_chart(df, output_dir)

    print("\n[SUCCESS] Experiment 1 completed successfully.")


if __name__ == "__main__":
    main()
