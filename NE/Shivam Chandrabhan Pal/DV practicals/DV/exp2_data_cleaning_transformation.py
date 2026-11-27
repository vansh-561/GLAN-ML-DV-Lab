"""
=============================================================================
Experiment 2: Data Cleaning and Transformation with Pandas
Objective:
    - Load/create a raw, messy dataset with missing values, dirty column names,
      and mixed data types.
    - Demonstrate identifying and imputing missing values (numeric & categorical).
    - Standardize and rename column names to clean snake_case.
    - Transform and convert incorrect data types (string to float/datetime/category).
    - Engineer calculated fields (Total Revenue, Net Profit, Profit Margin %).
    - Visualize data cleaning results and engineered feature distributions.
=============================================================================
"""

import os
import tempfile

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


def create_messy_dataset():
    """Generates an intentionally raw, uncleaned dataset with typical data anomalies."""
    raw_data = {
        " Order_ID # ": ["ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005", "ORD-006", "ORD-007", "ORD-008", "ORD-009", "ORD-010"],
        "Customer Name": ["Alice Smith", "Bob Jones", "Charlie Brown", np.nan, "Emma Watson", "Frank Miller", "Grace Hopper", "Hank Pym", np.nan, "Jack Ryan"],
        "Order-Date": ["2023-01-15", "2023/02/18", "12-03-2023", "2023-04-20", "2023/05/22", "2023-06-30", "2023-07-11", "2023/08/19", "2023-09-05", "2023-10-12"],
        " Item_Price ($) ": ["$1,250.00", "$45.50", "$890.00", "$320.00", np.nan, "$2,100.00", "$150.00", "$75.00", "$430.00", "$1,150.00"],
        "Units Ordered": ["5", "12", np.nan, "3", "8", "2", "15", np.nan, "4", "7"],
        "Discount %": [0.10, 0.05, 0.00, np.nan, 0.15, 0.20, 0.05, 0.00, 0.10, np.nan],
        "Category ": ["Technology", "Office Supplies", "Furniture", "Technology", np.nan, "Technology", "Office Supplies", "Furniture", "Office Supplies", "Furniture"],
        "Region_Code": ["North", "South", "East", "West", "North", "South", np.nan, "West", "East", "North"]
    }
    return pd.DataFrame(raw_data)


def clean_and_transform(df_raw):
    """
    Applies comprehensive data cleaning and transformation:
    1. Rename columns to snake_case.
    2. Convert types (remove '$', commas, parse numbers and dates).
    3. Impute missing values.
    4. Create calculated fields.
    """
    df = df_raw.copy()
    print("=" * 65)
    print(" 1. INITIAL MESSY DATASET ")
    print("=" * 65)
    print(df)
    print("\nMissing values per column before cleaning:")
    missing_before = df.isna().sum()
    print(missing_before)

    # 1. Column Renaming
    print("\n" + "-" * 65)
    print(" 2. COLUMN RENAMING & STANDARDIZATION ")
    print("-" * 65)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("#", "")
        .str.replace("-", "_")
        .str.replace("($)", "", regex=False)
        .str.replace("%", "rate")
        .str.strip("_")
    )
    print("Cleaned column names:", list(df.columns))

    # 2. Data Type Conversions
    print("\n" + "-" * 65)
    print(" 3. DATA TYPE PARSING & CONVERSION ")
    print("-" * 65)
    # Parse price: remove '$' and commas, convert to float
    df["item_price"] = df["item_price"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    df["item_price"] = pd.to_numeric(df["item_price"], errors="coerce")

    # Parse units ordered to numeric
    df["units_ordered"] = pd.to_numeric(df["units_ordered"], errors="coerce")

    # Parse order_date to standard datetime format
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")

    # 3. Missing Value Handling
    print("\n" + "-" * 65)
    print(" 4. MISSING VALUE IMPUTATION ")
    print("-" * 65)
    # Fill categorical missing values
    df["customer_name"] = df["customer_name"].fillna("Guest Customer")
    df["category"] = df["category"].fillna(df["category"].mode()[0])
    df["region_code"] = df["region_code"].fillna("Unassigned")

    # Fill numerical missing values with median
    median_price = df["item_price"].median()
    df["item_price"] = df["item_price"].fillna(median_price)

    median_units = df["units_ordered"].median()
    df["units_ordered"] = df["units_ordered"].fillna(median_units).astype(int)

    # Fill discount with 0.00 (no discount default)
    df["discount_rate"] = df["discount_rate"].fillna(0.0)

    missing_after = df.isna().sum()
    print("Missing values after cleaning:")
    print(missing_after)

    # 4. Creating Calculated Fields
    print("\n" + "-" * 65)
    print(" 5. CREATING CALCULATED FIELDS ")
    print("-" * 65)
    # Gross Revenue
    df["gross_revenue"] = df["item_price"] * df["units_ordered"]
    # Total Revenue after discount
    df["net_revenue"] = df["gross_revenue"] * (1 - df["discount_rate"])
    # Estimated Cost (assumed 65% of base price) and Net Profit
    df["estimated_cost"] = (df["item_price"] * 0.65) * df["units_ordered"]
    df["net_profit"] = df["net_revenue"] - df["estimated_cost"]
    # Profit Margin Percentage
    df["profit_margin_pct"] = (df["net_profit"] / df["net_revenue"]) * 100
    # Date parts
    df["order_month"] = df["order_date"].dt.strftime("%B")
    df["order_quarter"] = df["order_date"].dt.to_period("Q").astype(str)

    # Round numerical calculated fields
    df["gross_revenue"] = df["gross_revenue"].round(2)
    df["net_revenue"] = df["net_revenue"].round(2)
    df["net_profit"] = df["net_profit"].round(2)
    df["profit_margin_pct"] = df["profit_margin_pct"].round(2)

    print(df[["order_id", "customer_name", "item_price", "units_ordered", "net_revenue", "net_profit", "profit_margin_pct"]])
    return df, missing_before, missing_after


def visualize_cleaning_results(missing_before, missing_after, df_clean, output_dir):
    """Visualizes missing values before vs after and calculated metric distributions."""
    # Plot 1: Missing values comparison
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(missing_before))
    width = 0.35

    ax.bar(x - width / 2, missing_before.values, width, label="Before Cleaning (Raw)", color="#e74c3c", alpha=0.85)
    ax.bar(x + width / 2, missing_after.values, width, label="After Cleaning (Cleaned)", color="#2ecc71", alpha=0.85)

    ax.set_ylabel("Null / Missing Count", fontsize=11, labelpad=10)
    ax.set_title("Missing Values Treatment: Before vs After Data Cleaning", fontsize=13, weight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels([col[:12] for col in missing_before.index], rotation=35, ha="right", fontsize=9)
    ax.legend(frameon=True)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    path1 = os.path.join(output_dir, "exp2_missing_values_cleaning.png")
    plt.tight_layout()
    plt.savefig(path1, dpi=300)
    plt.close()
    print(f"[SAVED] Missing values comparison plot saved to: {path1}")

    # Plot 2: Calculated Fields (Net Revenue vs Profit Margin by Category)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    category_summary = df_clean.groupby("category").agg({
        "net_revenue": "sum",
        "net_profit": "sum",
        "profit_margin_pct": "mean"
    }).reset_index()

    # Barplot for Net Revenue & Net Profit
    x_cat = np.arange(len(category_summary))
    w = 0.35
    ax1.bar(x_cat - w / 2, category_summary["net_revenue"], w, label="Net Revenue ($)", color="#3498db")
    ax1.bar(x_cat + w / 2, category_summary["net_profit"], w, label="Net Profit ($)", color="#f39c12")
    ax1.set_xticks(x_cat)
    ax1.set_xticklabels(category_summary["category"], fontsize=10)
    ax1.set_title("Calculated Net Revenue & Profit by Category", fontsize=12, weight="bold")
    ax1.yaxis.set_major_formatter("${x:,.0f}")
    ax1.legend()
    ax1.grid(axis="y", linestyle="--", alpha=0.6)

    # Barplot for Profit Margin %
    bars = ax2.bar(category_summary["category"], category_summary["profit_margin_pct"], color="#9b59b6", alpha=0.85, edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                     textcoords="offset points", ha="center", weight="bold")
    ax2.set_title("Average Profit Margin (%) by Category", fontsize=12, weight="bold")
    ax2.set_ylabel("Profit Margin (%)")
    ax2.grid(axis="y", linestyle="--", alpha=0.6)

    path2 = os.path.join(output_dir, "exp2_calculated_fields.png")
    plt.tight_layout()
    plt.savefig(path2, dpi=300)
    plt.close()
    print(f"[SAVED] Calculated fields distribution saved to: {path2}")


def main():
    print("Starting Experiment 2: Data Cleaning and Transformation...")
    output_dir = get_output_dir()
    df_raw = create_messy_dataset()
    df_clean, missing_before, missing_after = clean_and_transform(df_raw)
    visualize_cleaning_results(missing_before, missing_after, df_clean, output_dir)
    print("\n[SUCCESS] Experiment 2 completed successfully.")


if __name__ == "__main__":
    main()
