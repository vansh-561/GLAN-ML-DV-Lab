"""
=============================================================================
Experiment 5: Geographic Visualization (Choropleth and Symbol Maps)
Objective:
    - Load / generate a country-level COVID-19 / Global Sales dataset with ISO-3 codes.
    - Generate an interactive Choropleth (filled area) map using Plotly Express.
    - Generate an interactive Symbol (bubble / scatter_geo) map using Plotly Express.
    - Customize geographic projections, color scales, hover inspectors, and legends.
    - Export interactive HTML map visualizations.
=============================================================================
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_output_dir():
    """Ensure the outputs directory exists and return its path."""
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def load_geographic_dataset():
    """
    Creates a comprehensive country-level Global Health & Commerce dataset
    with official ISO-3 Alpha codes to guarantee seamless offline mapping.
    """
    country_data = [
        {"country": "United States", "iso_alpha": "USA", "continent": "North America", "confirmed_cases": 103400000, "deaths": 1127000, "vaccination_rate": 81.4, "gdp_per_capita": 76398, "sales_volume": 4200000},
        {"country": "India", "iso_alpha": "IND", "continent": "Asia", "confirmed_cases": 44990000, "deaths": 531900, "vaccination_rate": 74.2, "gdp_per_capita": 2410, "sales_volume": 2850000},
        {"country": "Brazil", "iso_alpha": "BRA", "continent": "South America", "confirmed_cases": 37700000, "deaths": 704000, "vaccination_rate": 87.1, "gdp_per_capita": 8917, "sales_volume": 1450000},
        {"country": "France", "iso_alpha": "FRA", "continent": "Europe", "confirmed_cases": 40100000, "deaths": 167600, "vaccination_rate": 82.8, "gdp_per_capita": 42400, "sales_volume": 1820000},
        {"country": "Germany", "iso_alpha": "DEU", "continent": "Europe", "confirmed_cases": 38400000, "deaths": 174000, "vaccination_rate": 77.9, "gdp_per_capita": 48718, "sales_volume": 2400000},
        {"country": "United Kingdom", "iso_alpha": "GBR", "continent": "Europe", "confirmed_cases": 24600000, "deaths": 228000, "vaccination_rate": 80.5, "gdp_per_capita": 45480, "sales_volume": 2100000},
        {"country": "Japan", "iso_alpha": "JPN", "continent": "Asia", "confirmed_cases": 33800000, "deaths": 74600, "vaccination_rate": 83.6, "gdp_per_capita": 33815, "sales_volume": 3100000},
        {"country": "South Korea", "iso_alpha": "KOR", "continent": "Asia", "confirmed_cases": 34500000, "deaths": 35900, "vaccination_rate": 86.8, "gdp_per_capita": 32422, "sales_volume": 1950000},
        {"country": "Italy", "iso_alpha": "ITA", "continent": "Europe", "confirmed_cases": 26000000, "deaths": 191000, "vaccination_rate": 84.1, "gdp_per_capita": 34776, "sales_volume": 1600000},
        {"country": "Australia", "iso_alpha": "AUS", "continent": "Oceania", "confirmed_cases": 11800000, "deaths": 24000, "vaccination_rate": 88.2, "gdp_per_capita": 64491, "sales_volume": 1350000},
        {"country": "Canada", "iso_alpha": "CAN", "continent": "North America", "confirmed_cases": 4700000, "deaths": 53000, "vaccination_rate": 84.9, "gdp_per_capita": 52722, "sales_volume": 1750000},
        {"country": "South Africa", "iso_alpha": "ZAF", "continent": "Africa", "confirmed_cases": 4070000, "deaths": 102500, "vaccination_rate": 38.5, "gdp_per_capita": 6776, "sales_volume": 620000},
        {"country": "Mexico", "iso_alpha": "MEX", "continent": "North America", "confirmed_cases": 7630000, "deaths": 334000, "vaccination_rate": 66.8, "gdp_per_capita": 10045, "sales_volume": 980000},
        {"country": "Argentina", "iso_alpha": "ARG", "continent": "South America", "confirmed_cases": 10040000, "deaths": 130000, "vaccination_rate": 84.3, "gdp_per_capita": 13686, "sales_volume": 720000},
        {"country": "Nigeria", "iso_alpha": "NGA", "continent": "Africa", "confirmed_cases": 266000, "deaths": 3155, "vaccination_rate": 32.1, "gdp_per_capita": 2184, "sales_volume": 410000},
        {"country": "Egypt", "iso_alpha": "EGY", "continent": "Africa", "confirmed_cases": 516000, "deaths": 24800, "vaccination_rate": 41.6, "gdp_per_capita": 4295, "sales_volume": 530000},
        {"country": "China", "iso_alpha": "CHN", "continent": "Asia", "confirmed_cases": 99300000, "deaths": 121000, "vaccination_rate": 90.5, "gdp_per_capita": 12720, "sales_volume": 5600000},
        {"country": "Spain", "iso_alpha": "ESP", "continent": "Europe", "confirmed_cases": 13900000, "deaths": 121800, "vaccination_rate": 86.5, "gdp_per_capita": 29674, "sales_volume": 1420000},
        {"country": "Saudi Arabia", "iso_alpha": "SAU", "continent": "Asia", "confirmed_cases": 841000, "deaths": 9640, "vaccination_rate": 78.4, "gdp_per_capita": 30436, "sales_volume": 890000},
        {"country": "Indonesia", "iso_alpha": "IDN", "continent": "Asia", "confirmed_cases": 6810000, "deaths": 161900, "vaccination_rate": 66.5, "gdp_per_capita": 4788, "sales_volume": 940000}
    ]

    df = pd.DataFrame(country_data)
    df["case_fatality_rate"] = ((df["deaths"] / df["confirmed_cases"]) * 100).round(2)
    print(f"[INFO] Loaded geographic dataset with {len(df)} countries across all inhabited continents.")
    return df


def generate_choropleth_map(df, output_dir):
    """
    Builds a global Choropleth (filled map) visualizing confirmed cases intensity
    across sovereign nations using Plotly Express.
    """
    print("\n" + "=" * 60)
    print(" 1. GENERATING CHOROPLETH (FILLED) MAP ")
    print("=" * 60)

    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="confirmed_cases",
        hover_name="country",
        hover_data={
            "iso_alpha": False,
            "confirmed_cases": ":,",
            "deaths": ":,",
            "vaccination_rate": ":.1f%",
            "case_fatality_rate": ":.2f%"
        },
        color_continuous_scale="Reds",
        projection="natural earth",
        title="<b>Global COVID-19 Cumulative Confirmed Cases by Country</b><br><sup>Choropleth Filled Polygon Map (ISO-3 Alphas)</sup>"
    )

    fig.update_layout(
        template="plotly_white",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#7f8c8d",
            projection_type="natural earth",
            bgcolor="rgba(245, 247, 250, 0.6)"
        ),
        coloraxis_colorbar=dict(
            title="<b>Confirmed Cases</b>",
            tickformat=",.0s",
            len=0.75,
            thickness=18
        ),
        margin=dict(t=80, b=30, l=10, r=10)
    )

    output_path = os.path.join(output_dir, "exp5_choropleth_map.html")
    fig.write_html(output_path)
    print(f"[SAVED] Choropleth map saved to: {output_path}")


def generate_symbol_map(df, output_dir):
    """
    Builds a global Symbol / Bubble map where:
    - Circle size represents Total Sales Volume / Economic Impact.
    - Circle color represents Continent.
    - Hover inspector shows detailed metrics.
    """
    print("\n" + "=" * 60)
    print(" 2. GENERATING SYMBOL (BUBBLE) MAP ")
    print("=" * 60)

    fig = px.scatter_geo(
        df,
        locations="iso_alpha",
        color="continent",
        hover_name="country",
        size="sales_volume",
        size_max=36,
        hover_data={
            "iso_alpha": False,
            "sales_volume": ":$,.0f",
            "gdp_per_capita": ":$,.0f",
            "vaccination_rate": ":.1f%"
        },
        projection="natural earth",
        title="<b>Global Market Footprint & Commercial Sales Volume</b><br><sup>Symbol / Bubble Proportional Geographic Map</sup>"
    )

    fig.update_layout(
        template="plotly_white",
        geo=dict(
            showland=True,
            landcolor="#e8ecef",
            showocean=True,
            oceancolor="#d4e6f1",
            showcountries=True,
            countrycolor="#bdc3c7",
            showframe=False
        ),
        legend=dict(
            title="<b>Continent</b>",
            orientation="h",
            yanchor="bottom",
            y=-0.08,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=80, b=40, l=10, r=10)
    )

    output_path = os.path.join(output_dir, "exp5_symbol_map.html")
    fig.write_html(output_path)
    print(f"[SAVED] Symbol map saved to: {output_path}")


def main():
    print("Starting Experiment 5: Geographic Visualizations...")
    output_dir = get_output_dir()
    df = load_geographic_dataset()

    generate_choropleth_map(df, output_dir)
    generate_symbol_map(df, output_dir)

    print("\n[SUCCESS] Experiment 5 completed successfully.")


if __name__ == "__main__":
    main()
