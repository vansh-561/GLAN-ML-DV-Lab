"""
=============================================================================
Experiment 3: Bar & Line Series with Data Labels and Interactive Tooltips
Objective:
    - Use sales / stock time-series data.
    - Generate category bar charts with explicit data labels and custom hover tooltips.
    - Create time-trend multi-line charts with range sliders, markers, and tooltips.
    - Construct a combined dual-axis Bar + Line series figure.
    - Export interactive HTML visualizations using Plotly.
=============================================================================
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_output_dir():
    """Ensure the outputs directory exists and return its path."""
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_time_series_data():
    """Generates a structured monthly retail sales dataset spanning 24 months across 4 categories."""
    np.random.seed(101)
    dates = pd.date_range(start="2023-01-01", periods=24, freq="MS")
    categories = ["Consumer Electronics", "Corporate Furniture", "Office Supplies", "Smart Home Tech"]

    data = []
    base_sales = {
        "Consumer Electronics": 45000,
        "Corporate Furniture": 32000,
        "Office Supplies": 18000,
        "Smart Home Tech": 26000
    }
    growth_rates = {
        "Consumer Electronics": 1.03,
        "Corporate Furniture": 1.015,
        "Office Supplies": 1.01,
        "Smart Home Tech": 1.04
    }

    for i, dt in enumerate(dates):
        for cat in categories:
            trend = base_sales[cat] * (growth_rates[cat] ** i)
            seasonality = 1.0 + 0.15 * np.sin(2 * np.pi * dt.month / 12)
            noise = np.random.uniform(0.92, 1.08)
            sales = round(trend * seasonality * noise, 2)
            margin_rate = np.random.uniform(0.18, 0.32)
            profit = round(sales * margin_rate, 2)
            units = int(sales / np.random.uniform(50, 200))

            data.append({
                "Date": dt,
                "Month_Year": dt.strftime("%b %Y"),
                "Category": cat,
                "Sales": sales,
                "Profit": profit,
                "Units_Sold": units,
                "Profit_Margin_Pct": round((profit / sales) * 100, 2)
            })

    df = pd.DataFrame(data)
    print(f"[INFO] Time-series dataset generated: {len(df)} records across {len(categories)} categories.")
    return df


def plot_category_bar_chart(df, output_dir):
    """
    Creates an interactive category bar chart with formatted data labels and
    rich hovertooltips showing Sales, Profit, and Profit Margin.
    """
    print("\n" + "=" * 60)
    print(" 1. CREATING INTERACTIVE CATEGORY BAR CHART ")
    print("=" * 60)

    category_agg = df.groupby("Category").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Units_Sold": "sum"
    }).reset_index()

    category_agg["Profit_Margin_Pct"] = ((category_agg["Profit"] / category_agg["Sales"]) * 100).round(2)
    category_agg["Formatted_Sales"] = category_agg["Sales"].apply(lambda x: f"${x:,.0f}")
    category_agg["Formatted_Profit"] = category_agg["Profit"].apply(lambda x: f"${x:,.0f}")

    print(category_agg[["Category", "Sales", "Profit", "Profit_Margin_Pct"]])

    fig = px.bar(
        category_agg,
        x="Category",
        y="Sales",
        color="Profit_Margin_Pct",
        color_continuous_scale="Tealgrn",
        text="Formatted_Sales",
        title="<b>Annual Sales Performance by Category</b><br><sup>Color scale depicts Average Profit Margin %</sup>",
        labels={"Sales": "Total Sales (USD)", "Profit_Margin_Pct": "Profit Margin (%)"}
    )

    # Enhance hover tooltip and data labels
    fig.update_traces(
        textposition="outside",
        textfont_size=12,
        hovertemplate=(
            "<b>Category:</b> %{x}<br>" +
            "<b>Total Revenue:</b> $%{y:,.2f}<br>" +
            "<b>Profit Margin:</b> %{marker.color:.2f}%<extra></extra>"
        )
    )

    fig.update_layout(
        template="plotly_white",
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        xaxis_title="<b>Product Category</b>",
        yaxis_title="<b>Revenue (USD)</b>",
        margin=dict(t=70, b=40, l=60, r=40)
    )

    output_path = os.path.join(output_dir, "exp3_category_bar.html")
    fig.write_html(output_path)
    print(f"[SAVED] Category Bar Chart saved to: {output_path}")


def plot_time_trend_line_chart(df, output_dir):
    """
    Creates an interactive multi-line time series chart showing sales trends
    over time across categories with markers and range slider.
    """
    print("\n" + "=" * 60)
    print(" 2. CREATING INTERACTIVE TIME-SERIES LINE CHART ")
    print("=" * 60)

    fig = px.line(
        df,
        x="Date",
        y="Sales",
        color="Category",
        markers=True,
        line_shape="spline",
        title="<b>Monthly Category Sales Trajectory (2023 - 2024)</b><br><sup>Explore trend curves with interactive slider and hover inspectors</sup>",
        labels={"Sales": "Monthly Sales (USD)", "Date": "Timeline"}
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>" +
            "Date: %{x|%B %Y}<br>" +
            "Sales Volume: $%{y:,.2f}<extra></extra>"
        ),
        marker=dict(size=7)
    )

    # Add range slider and selector buttons
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=6, label="6 Months", step="month", stepmode="backward"),
                    dict(count=1, label="1 Year", step="year", stepmode="backward"),
                    dict(step="all", label="All Time")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=80, b=40, l=60, r=40)
    )

    output_path = os.path.join(output_dir, "exp3_trend_line.html")
    fig.write_html(output_path)
    print(f"[SAVED] Time-trend Line Chart saved to: {output_path}")


def plot_combined_bar_line_series(df, output_dir):
    """
    Creates a dual-axis combined chart:
    - Primary Y-axis: Monthly Total Sales (Bar Series)
    - Secondary Y-axis: Overall Profit Margin % (Line Series)
    """
    print("\n" + "=" * 60)
    print(" 3. CREATING DUAL-AXIS COMBINED BAR & LINE SERIES ")
    print("=" * 60)

    monthly_summary = df.groupby("Date").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()
    monthly_summary["Profit_Margin_Pct"] = (monthly_summary["Profit"] / monthly_summary["Sales"]) * 100
    monthly_summary["Month_Label"] = monthly_summary["Date"].dt.strftime("%b %y")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Bar chart on primary axis
    fig.add_trace(
        go.Bar(
            x=monthly_summary["Month_Label"],
            y=monthly_summary["Sales"],
            name="Total Sales ($)",
            marker_color="#1f77b4",
            opacity=0.75,
            hovertemplate="Month: %{x}<br>Sales: $%{y:,.2f}<extra></extra>"
        ),
        secondary_y=False
    )

    # Add Line chart on secondary axis
    fig.add_trace(
        go.Scatter(
            x=monthly_summary["Month_Label"],
            y=monthly_summary["Profit_Margin_Pct"],
            name="Profit Margin (%)",
            mode="lines+markers",
            marker=dict(color="#d62728", size=8),
            line=dict(color="#d62728", width=3),
            hovertemplate="Month: %{x}<br>Margin: %{y:.2f}%<extra></extra>"
        ),
        secondary_y=True
    )

    fig.update_layout(
        title="<b>Monthly Sales Revenue vs Profit Margin Ratio</b><br><sup>Combined Dual-Axis Series</sup>",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"),
        margin=dict(t=75, b=40, l=60, r=60)
    )

    fig.update_yaxes(title_text="<b>Monthly Revenue (USD)</b>", tickprefix="$", tickformat=",.0f", secondary_y=False)
    fig.update_yaxes(title_text="<b>Profit Margin (%)</b>", ticksuffix="%", secondary_y=True)

    output_path = os.path.join(output_dir, "exp3_combined_bar_line.html")
    fig.write_html(output_path)
    print(f"[SAVED] Combined Dual-Axis Series saved to: {output_path}")


def main():
    print("Starting Experiment 3: Bar & Line Series with Interactive Tooltips...")
    output_dir = get_output_dir()
    df = generate_time_series_data()

    plot_category_bar_chart(df, output_dir)
    plot_time_trend_line_chart(df, output_dir)
    plot_combined_bar_line_series(df, output_dir)

    print("\n[SUCCESS] Experiment 3 completed successfully.")


if __name__ == "__main__":
    main()
