"""
=============================================================================
Experiment 7: Correlation Heatmaps (Seaborn) and Hierarchical Treemaps (Plotly)
Objective:
    - Generate a multi-attribute commercial dataset with hierarchical dimensions.
    - Compute and visualize a correlation matrix heatmap using Seaborn with an
      upper-triangle mask and numerical annotations.
    - Construct an interactive Hierarchical Treemap (Category > Subcategory > Region)
      using Plotly where node sizes represent Sales and colors represent Profitability.
    - Save static PNG and interactive HTML outputs.
=============================================================================
"""

import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def get_output_dir():
    """Ensure the outputs directory exists and return its path."""
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_hierarchical_retail_data():
    """Generates a rich retail dataset containing hierarchy and numerical attributes."""
    np.random.seed(42)
    hierarchy_map = {
        "Technology": ["Smartphones", "Laptops", "Accessories", "Printers", "Monitors"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings", "Storage"],
        "Office Supplies": ["Paper", "Binders", "Appliances", "Art Supplies", "Fasteners"]
    }
    regions = ["North", "South", "East", "West"]

    records = []
    for cat, subcats in hierarchy_map.items():
        for sub in subcats:
            for reg in regions:
                n_samples = np.random.randint(15, 30)
                for _ in range(n_samples):
                    unit_price = np.random.uniform(20, 800) if cat == "Technology" else (
                        np.random.uniform(40, 500) if cat == "Furniture" else np.random.uniform(5, 120)
                    )
                    quantity = np.random.randint(1, 15)
                    discount = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.30], p=[0.4, 0.2, 0.15, 0.1, 0.1, 0.05])
                    gross_sales = unit_price * quantity
                    sales = gross_sales * (1 - discount)
                    shipping_cost = round(np.random.uniform(5, 50) + quantity * 1.5, 2)
                    base_margin = np.random.uniform(0.15, 0.45) - (discount * 0.8)
                    profit = round((sales * base_margin) - shipping_cost, 2)
                    cust_age = np.random.randint(20, 68)

                    records.append({
                        "Category": cat,
                        "Subcategory": sub,
                        "Region": reg,
                        "Unit_Price": round(unit_price, 2),
                        "Quantity": quantity,
                        "Discount": discount,
                        "Shipping_Cost": shipping_cost,
                        "Sales": round(sales, 2),
                        "Profit": profit,
                        "Customer_Age": cust_age,
                        "Profit_Margin_Pct": round((profit / sales) * 100, 2) if sales > 0 else 0
                    })

    df = pd.DataFrame(records)
    print(f"[INFO] Hierarchical dataset generated: {len(df):,} transactions across {len(hierarchy_map)} categories.")
    return df


def plot_correlation_heatmap(df, output_dir):
    """
    Computes Pearson correlation matrix and plots a Seaborn heatmap
    with an upper-triangle mask, diverging colormap, and annotations.
    """
    print("\n" + "=" * 60)
    print(" 1. GENERATING SEABORN CORRELATION MATRIX HEATMAP ")
    print("=" * 60)

    numeric_cols = ["Unit_Price", "Quantity", "Discount", "Shipping_Cost", "Sales", "Profit", "Profit_Margin_Pct"]
    corr_matrix = df[numeric_cols].corr().round(2)
    print(corr_matrix)

    # Generate mask for the upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    plt.figure(figsize=(10, 8))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap=cmap,
        vmax=1.0,
        vmin=-1.0,
        center=0,
        annot=True,
        fmt=".2f",
        square=True,
        linewidths=1.2,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation Coefficient"}
    )

    plt.title("Commercial Attributes Correlation Matrix Heatmap", fontsize=14, weight="bold", pad=15)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    output_path = os.path.join(output_dir, "exp7_correlation_heatmap.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[SAVED] Correlation Heatmap saved to: {output_path}")


def plot_hierarchical_treemap(df, output_dir):
    """
    Constructs an interactive hierarchical Treemap using Plotly Express:
    Hierarchy: Category -> Subcategory -> Region
    Tile Size: Total Sales Revenue
    Tile Color: Net Profit ($)
    """
    print("\n" + "=" * 60)
    print(" 2. GENERATING HIERARCHICAL PLOTLY TREEMAP ")
    print("=" * 60)

    # Aggregate by hierarchy nodes
    agg_df = df.groupby(["Category", "Subcategory", "Region"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum"
    }).reset_index()

    agg_df["Profit_Margin_Pct"] = ((agg_df["Profit"] / agg_df["Sales"]) * 100).round(2)

    fig = px.treemap(
        agg_df,
        path=["Category", "Subcategory", "Region"],
        values="Sales",
        color="Profit",
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=0,
        title="<b>Hierarchical Retail Sales Breakdown: Category > Subcategory > Region</b><br><sup>Node Area = Total Sales Volume | Node Color = Net Profit (USD)</sup>"
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>" +
            "Hierarchy: %{id}<br>" +
            "Total Sales: $%{value:,.2f}<br>" +
            "Net Profit: $%{color:,.2f}<extra></extra>"
        ),
        textinfo="label+value+percent parent"
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(t=80, b=30, l=15, r=15),
        coloraxis_colorbar=dict(
            title="<b>Net Profit (USD)</b>",
            tickprefix="$",
            tickformat=",.0f",
            len=0.8
        )
    )

    output_path = os.path.join(output_dir, "exp7_hierarchical_treemap.html")
    fig.write_html(output_path)
    print(f"[SAVED] Hierarchical Treemap saved to: {output_path}")


def main():
    print("Starting Experiment 7: Correlation Heatmaps & Hierarchical Treemaps...")
    output_dir = get_output_dir()
    df = generate_hierarchical_retail_data()

    plot_correlation_heatmap(df, output_dir)
    plot_hierarchical_treemap(df, output_dir)

    print("\n[SUCCESS] Experiment 7 completed successfully.")


if __name__ == "__main__":
    main()
