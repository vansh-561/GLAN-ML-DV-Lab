"""
=============================================================================
Experiment 4: Interactive Retail Dashboard with Dropdowns and Sliders
Objective:
    - Build an interactive, comprehensive Retail Executive Dashboard using Plotly.
    - Provide interactive dropdown menus for dynamic filtering by Region.
    - Provide category view toggles and timeline date range sliders.
    - Display key performance indicators (KPIs) alongside multi-chart visual panels:
        1. Sales & Profit Timeline Trend (Line/Area)
        2. Category-wise Sales & Margin (Grouped Bar)
        3. Regional Performance Breakdown (Donut)
    - Export a standalone, self-contained HTML dashboard.
=============================================================================
"""

import os
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_output_dir():
    """Ensure the outputs directory exists and return its path."""
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_retail_dashboard_data():
    """Generates multi-regional, multi-category retail transactions across 2023-2024."""
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
    regions = ["North", "South", "East", "West"]
    categories = ["Technology", "Furniture", "Office Supplies"]

    rows = []
    for d in dates:
        # Sample 3-5 orders per day
        n_orders = np.random.randint(3, 6)
        for _ in range(n_orders):
            reg = np.random.choice(regions, p=[0.30, 0.25, 0.25, 0.20])
            cat = np.random.choice(categories, p=[0.40, 0.35, 0.25])
            base = 450 if cat == "Technology" else (280 if cat == "Furniture" else 120)
            sales = round(float(np.random.exponential(base) + 20), 2)
            margin_rate = np.random.uniform(0.12, 0.38)
            profit = round(sales * margin_rate, 2)
            quantity = np.random.randint(1, 10)

            rows.append({
                "Date": d,
                "Month": d.strftime("%Y-%m"),
                "Year": d.year,
                "Region": reg,
                "Category": cat,
                "Sales": sales,
                "Profit": profit,
                "Quantity": quantity
            })

    df = pd.DataFrame(rows)
    print(f"[INFO] Retail dashboard dataset ready: {len(df):,} transactions recorded.")
    return df


def build_interactive_dashboard(df, output_dir):
    """
    Constructs an interactive executive dashboard figure using Plotly subplots,
    dropdown updatemenus for Region filtering, and Date Range Sliders.
    """
    print("\n" + "=" * 65)
    print(" BUILDING INTERACTIVE RETAIL DASHBOARD FIGURE ")
    print("=" * 65)

    regions = ["All Regions", "North", "South", "East", "West"]
    categories = sorted(df["Category"].unique())

    # Pre-aggregate data for "All Regions" and each specific region
    data_by_region = {}
    for r in regions:
        sub_df = df if r == "All Regions" else df[df["Region"] == r]
        # Monthly timeline
        monthly = sub_df.groupby("Month").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        # Category breakdown
        cat_agg = sub_df.groupby("Category").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
        # Region distribution
        reg_agg = sub_df.groupby("Region")["Sales"].sum().reset_index()
        # KPIs
        total_sales = sub_df["Sales"].sum()
        total_profit = sub_df["Profit"].sum()
        avg_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
        total_orders = len(sub_df)

        data_by_region[r] = {
            "monthly": monthly,
            "category": cat_agg,
            "region_dist": reg_agg,
            "kpis": (total_sales, total_profit, avg_margin, total_orders)
        }

    # Create subplots grid:
    # Row 1: KPI Indicator cards
    # Row 2: Sales & Profit Timeline (span 2 cols) | Regional Donut
    # Row 3: Category Sales & Profit Bar Chart (span 3 cols)
    fig = make_subplots(
        rows=3, cols=3,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
            [{"type": "scatter", "colspan": 2}, None, {"type": "pie"}],
            [{"type": "bar", "colspan": 3}, None, None]
        ],
        subplot_titles=(
            "", "", "",
            "<b>Monthly Revenue & Profit Trajectory</b>", "<b>Regional Share</b>",
            "<b>Sales & Profitability Breakdown by Category</b>"
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )

    # 1. Traces for default "All Regions"
    all_data = data_by_region["All Regions"]
    tot_s, tot_p, avg_m, tot_ord = all_data["kpis"]

    # KPI 1: Revenue
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=tot_s,
            number={"prefix": "$", "valueformat": ",.0f"},
            title={"text": "<b>Total Net Revenue</b><br><span style='font-size:0.8em;color:gray'>2023-2024 Overall</span>"},
            domain={"row": 0, "column": 0}
        ),
        row=1, col=1
    )

    # KPI 2: Profit
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=tot_p,
            number={"prefix": "$", "valueformat": ",.0f"},
            title={"text": "<b>Total Net Profit</b><br><span style='font-size:0.8em;color:gray'>2023-2024 Overall</span>"},
            domain={"row": 0, "column": 1}
        ),
        row=1, col=2
    )

    # KPI 3: Margin %
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=avg_m,
            number={"suffix": "%", "valueformat": ".2f"},
            title={"text": "<b>Blended Profit Margin</b><br><span style='font-size:0.8em;color:gray'>Efficiency Ratio</span>"},
            domain={"row": 0, "column": 2}
        ),
        row=1, col=3
    )

    # Timeline - Sales Line
    fig.add_trace(
        go.Scatter(
            x=all_data["monthly"]["Month"],
            y=all_data["monthly"]["Sales"],
            name="Monthly Sales",
            mode="lines+markers",
            line=dict(color="#1f77b4", width=3),
            fill="tozeroy",
            fillcolor="rgba(31, 119, 180, 0.12)",
            hovertemplate="Month: %{x}<br>Sales: $%{y:,.0f}<extra></extra>"
        ),
        row=2, col=1
    )

    # Timeline - Profit Line
    fig.add_trace(
        go.Scatter(
            x=all_data["monthly"]["Month"],
            y=all_data["monthly"]["Profit"],
            name="Monthly Profit",
            mode="lines+markers",
            line=dict(color="#2ca02c", width=2.5, dash="dash"),
            hovertemplate="Month: %{x}<br>Profit: $%{y:,.0f}<extra></extra>"
        ),
        row=2, col=1
    )

    # Regional Donut Chart
    fig.add_trace(
        go.Pie(
            labels=all_data["region_dist"]["Region"],
            values=all_data["region_dist"]["Sales"],
            hole=0.5,
            name="Region Share",
            marker=dict(colors=["#3498db", "#e74c3c", "#f1c40f", "#2ecc71"]),
            hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Share: %{percent}<extra></extra>"
        ),
        row=2, col=3
    )

    # Category Bar Chart - Sales
    fig.add_trace(
        go.Bar(
            x=all_data["category"]["Category"],
            y=all_data["category"]["Sales"],
            name="Category Sales",
            marker_color="#2b5c8f",
            text=all_data["category"]["Sales"].apply(lambda v: f"${v:,.0f}"),
            textposition="auto",
            hovertemplate="Category: %{x}<br>Sales: $%{y:,.0f}<extra></extra>"
        ),
        row=3, col=1
    )

    # Category Bar Chart - Profit
    fig.add_trace(
        go.Bar(
            x=all_data["category"]["Category"],
            y=all_data["category"]["Profit"],
            name="Category Profit",
            marker_color="#27ae60",
            text=all_data["category"]["Profit"].apply(lambda v: f"${v:,.0f}"),
            textposition="auto",
            hovertemplate="Category: %{x}<br>Profit: $%{y:,.0f}<extra></extra>"
        ),
        row=3, col=1
    )

    # Configure Dropdown Menu for Region Filter
    dropdown_buttons = []
    for r in regions:
        d = data_by_region[r]
        tot_s, tot_p, avg_m, _ = d["kpis"]

        # Define trace updates for this region
        button = dict(
            method="update",
            label=f"Region: {r}",
            args=[
                {
                    # Trace 0: KPI Revenue
                    "value": [tot_s, tot_p, avg_m, d["monthly"]["Sales"], d["monthly"]["Profit"], d["region_dist"]["Sales"], d["category"]["Sales"], d["category"]["Profit"]],
                    "x": [None, None, None, d["monthly"]["Month"], d["monthly"]["Month"], None, d["category"]["Category"], d["category"]["Category"]],
                    "y": [None, None, None, d["monthly"]["Sales"], d["monthly"]["Profit"], None, d["category"]["Sales"], d["category"]["Profit"]],
                    "labels": [None, None, None, None, None, d["region_dist"]["Region"], None, None],
                    "text": [None, None, None, None, None, None, d["category"]["Sales"].apply(lambda v: f"${v:,.0f}"), d["category"]["Profit"].apply(lambda v: f"${v:,.0f}")]
                },
                {
                    "title": f"<b>Retail Performance Executive Dashboard</b> — Filtered by: <i>{r}</i>"
                }
            ]
        )
        dropdown_buttons.append(button)

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=dropdown_buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.01,
                xanchor="left",
                y=1.15,
                yanchor="top",
                bgcolor="#ffffff",
                bordercolor="#cccccc",
                font=dict(size=12, color="#333333")
            )
        ],
        title=dict(
            text="<b>Retail Performance Executive Dashboard</b> — Filtered by: <i>All Regions</i>",
            font=dict(size=20),
            x=0.5,
            xanchor="center",
            y=0.98
        ),
        template="plotly_white",
        height=1000,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5),
        margin=dict(t=120, b=80, l=60, r=40)
    )

    # Add range slider to timeline axis
    fig.update_xaxes(rangeslider=dict(visible=True, thickness=0.05), row=2, col=1)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=2, col=1)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=3, col=1)

    output_path = os.path.join(output_dir, "exp4_retail_dashboard.html")
    fig.write_html(output_path, include_plotlyjs="cdn")
    print(f"[SAVED] Interactive Dashboard saved to: {output_path}")


def main():
    print("Starting Experiment 4: Interactive Retail Dashboard...")
    output_dir = get_output_dir()
    df = generate_retail_dashboard_data()
    build_interactive_dashboard(df, output_dir)
    print("\n[SUCCESS] Experiment 4 completed successfully.")


if __name__ == "__main__":
    main()
