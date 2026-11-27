"""
=============================================================================
Experiment 6: Proportional Composition with Pie and Donut Charts
Objective:
    - Load / generate Olympic Games country-wise medal tally data.
    - Create an exploded, customized Pie chart displaying medal proportions.
    - Create an interactive Donut chart with a center KPI summary.
    - Produce comparative side-by-side composition views (Gold vs Total share).
    - Save both interactive HTML (Plotly) and high-resolution PNG (Matplotlib).
=============================================================================
"""

import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_output_dir():
    """Ensure the outputs directory exists and return its path."""
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def load_olympic_medal_data():
    """Returns official Olympic Games country medal tallies."""
    medals_data = [
        {"nation": "United States", "gold": 40, "silver": 44, "bronze": 42, "total": 126},
        {"nation": "China", "gold": 40, "silver": 27, "bronze": 24, "total": 91},
        {"nation": "Japan", "gold": 20, "silver": 12, "bronze": 13, "total": 45},
        {"nation": "Australia", "gold": 18, "silver": 19, "bronze": 16, "total": 53},
        {"nation": "France", "gold": 16, "silver": 26, "bronze": 22, "total": 64},
        {"nation": "Netherlands", "gold": 15, "silver": 7, "bronze": 12, "total": 34},
        {"nation": "Great Britain", "gold": 14, "silver": 22, "bronze": 29, "total": 65},
        {"nation": "South Korea", "gold": 13, "silver": 9, "bronze": 10, "total": 32},
        {"nation": "Italy", "gold": 12, "silver": 13, "bronze": 15, "total": 40},
        {"nation": "Germany", "gold": 12, "silver": 13, "bronze": 8, "total": 33},
        {"nation": "Rest of the World", "gold": 139, "silver": 140, "bronze": 194, "total": 473}
    ]
    df = pd.DataFrame(medals_data)
    print(f"[INFO] Loaded Olympic Medals dataset ({len(df)} entries, Total Medals: {df['total'].sum()}).")
    return df


def create_plotly_pie_and_donut(df, output_dir):
    """
    Constructs an interactive 2-panel Plotly figure:
    - Left: Exploded Pie Chart showing Gold Medal Share.
    - Right: Donut Chart showing Overall Medal Share with Center Annotation.
    """
    print("\n" + "=" * 60)
    print(" 1. GENERATING INTERACTIVE PLOTLY PIE & DONUT CHARTS ")
    print("=" * 60)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "pie"}]],
        subplot_titles=(
            "<b>Gold Medal Dominance (Pie Chart)</b>",
            "<b>Total Medal Distribution (Donut Chart)</b>"
        )
    )

    palette = [
        "#f1c40f", "#e67e22", "#3498db", "#2ecc71", "#9b59b6",
        "#1abc9c", "#e74c3c", "#34495e", "#d35400", "#27ae60", "#95a5a6"
    ]

    # Pull/explode top 2 nations in Pie chart
    pull_values = [0.12 if i < 2 else 0.0 for i in range(len(df))]

    # 1. Pie Chart for Gold Medals
    fig.add_trace(
        go.Pie(
            labels=df["nation"],
            values=df["gold"],
            name="Gold Medals",
            pull=pull_values,
            marker=dict(colors=palette, line=dict(color="#ffffff", width=2)),
            textinfo="label+percent",
            textposition="inside",
            hovertemplate="<b>%{label}</b><br>Gold Medals: %{value}<br>Gold Share: %{percent}<extra></extra>"
        ),
        row=1, col=1
    )

    # 2. Donut Chart for Total Medals
    total_medals_sum = df["total"].sum()
    fig.add_trace(
        go.Pie(
            labels=df["nation"],
            values=df["total"],
            hole=0.55,
            name="Total Medals",
            marker=dict(colors=palette, line=dict(color="#ffffff", width=2)),
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>" +
                "Total Medals: %{value}<br>" +
                "Proportion: %{percent}<extra></extra>"
            )
        ),
        row=1, col=2
    )

    # Center label for Donut chart
    fig.add_annotation(
        text=f"<b>Total</b><br>{total_medals_sum:,}<br><span style='font-size:10px;'>Medals</span>",
        x=0.81, y=0.5,
        font_size=14,
        showarrow=False,
        align="center"
    )

    fig.update_layout(
        title=dict(
            text="<b>Olympic Games Proportional Medal Composition</b><br><sup>Comparative Analysis of Gold vs Overall Medal Shares</sup>",
            x=0.5,
            xanchor="center",
            y=0.96
        ),
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(t=80, b=80, l=40, r=40)
    )

    output_path = os.path.join(output_dir, "exp6_pie_donut_charts.html")
    fig.write_html(output_path)
    print(f"[SAVED] Interactive HTML saved to: {output_path}")


def create_matplotlib_pie_and_donut(df, output_dir):
    """
    Renders high-resolution side-by-side Pie and Donut charts using Matplotlib
    for immediate static reporting and lab record submission.
    """
    print("\n" + "=" * 60)
    print(" 2. GENERATING HIGH-RES MATPLOTLIB PIE & DONUT FIGURE ")
    print("=" * 60)

    # Filter to top 6 + Combined Others for cleaner static labels
    top_df = df.iloc[:6].copy()
    others_total = df.iloc[6:]["total"].sum()
    others_gold = df.iloc[6:]["gold"].sum()

    combined_df = pd.concat([
        top_df,
        pd.DataFrame([{"nation": "Other Nations", "gold": others_gold, "silver": 0, "bronze": 0, "total": others_total}])
    ], ignore_index=True)

    colors = ["#f39c12", "#e74c3c", "#3498db", "#2ecc71", "#9b59b6", "#1abc9c", "#95a5a6"]
    explode = [0.08, 0.08, 0, 0, 0, 0, 0]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel 1: Pie Chart (Gold)
    wedges1, texts1, autotexts1 = ax1.pie(
        combined_df["gold"],
        labels=combined_df["nation"],
        autopct="%1.1f%%",
        startangle=140,
        explode=explode,
        colors=colors,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
        textprops=dict(fontsize=9, weight="bold")
    )
    for at in autotexts1:
        at.set_color("white")
        at.set_fontsize(8)
    ax1.set_title("Gold Medals Share (Pie Chart)", fontsize=13, weight="bold", pad=12)

    # Panel 2: Donut Chart (Total)
    wedges2, texts2, autotexts2 = ax2.pie(
        combined_df["total"],
        labels=combined_df["nation"],
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=1.5),
        textprops=dict(fontsize=9, weight="bold")
    )
    for at in autotexts2:
        at.set_color("white")
        at.set_fontsize(8)

    # Center text for donut
    ax2.text(0, 0, f"Total\n{df['total'].sum():,}\nMedals", ha="center", va="center", fontsize=11, weight="bold")
    ax2.set_title("Total Medals Share (Donut Chart)", fontsize=13, weight="bold", pad=12)

    plt.suptitle("Olympic Medal Distribution Proportions", fontsize=16, weight="bold", y=1.02)
    output_path = os.path.join(output_dir, "exp6_pie_donut_charts.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Static PNG saved to: {output_path}")


def main():
    print("Starting Experiment 6: Pie and Donut Charts...")
    output_dir = get_output_dir()
    df = load_olympic_medal_data()

    create_plotly_pie_and_donut(df, output_dir)
    create_matplotlib_pie_and_donut(df, output_dir)

    print("\n[SUCCESS] Experiment 6 completed successfully.")


if __name__ == "__main__":
    main()
