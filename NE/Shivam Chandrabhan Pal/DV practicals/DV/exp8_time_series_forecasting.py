"""
=============================================================================
Experiment 8: Time-Series Analysis, Moving Averages, and Trend Forecasting
Objective:
    - Generate continuous sales / stock time-series data with trend & seasonality.
    - Compute rolling moving averages (7-period SMA, 30-period EMA, Bollinger Bands).
    - Fit a statistical forecasting model (Exponential Smoothing / Holt-Winters
      via statsmodels) to project future demand with confidence intervals.
    - Export both static high-res visualization (Matplotlib) and interactive
      time-series chart with range sliders and tooltips (Plotly).
=============================================================================
"""

import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def get_output_dir():
    """Ensure the outputs directory exists and return its path."""
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_time_series_data():
    """Generates daily historical commercial sales records over 2 years."""
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2024-10-31", freq="D")
    n = len(dates)

    # Components: Upward linear trend + Annual/Weekly seasonality + Gaussian noise
    t = np.arange(n)
    trend = 1200 + 1.8 * t
    annual_seasonality = 180 * np.sin(2 * np.pi * t / 365.25)
    weekly_seasonality = 90 * np.cos(2 * np.pi * t / 7)
    noise = np.random.normal(0, 65, n)

    sales = np.maximum(200, trend + annual_seasonality + weekly_seasonality + noise)

    df = pd.DataFrame({
        "Date": dates,
        "Sales": np.round(sales, 2)
    }).set_index("Date")

    print(f"[INFO] Generated historical daily time-series: {len(df)} days ({df.index.min().date()} to {df.index.max().date()}).")
    return df


def calculate_moving_averages(df):
    """Computes Rolling Simple Moving Average, Exponential Moving Average, and Bollinger Bands."""
    data = df.copy()
    data["SMA_7"] = data["Sales"].rolling(window=7, min_periods=1).mean()
    data["SMA_30"] = data["Sales"].rolling(window=30, min_periods=1).mean()
    data["EMA_30"] = data["Sales"].ewm(span=30, adjust=False).mean()

    # Bollinger Bands (20-day rolling mean +/- 2 standard deviations)
    rolling_20 = data["Sales"].rolling(window=20, min_periods=1)
    data["BB_Mid"] = rolling_20.mean()
    rolling_std = rolling_20.std().fillna(0)
    data["BB_Upper"] = data["BB_Mid"] + (2 * rolling_std)
    data["BB_Lower"] = np.maximum(0, data["BB_Mid"] - (2 * rolling_std))

    return data


def generate_forecast(df, forecast_days=60):
    """
    Fits Holt-Winters Exponential Smoothing model and projects future sales
    along with estimated 95% confidence intervals.
    """
    print("\n" + "=" * 60)
    print(f" FITTING STATISTICAL FORECASTING MODEL (HORIZON: {forecast_days} DAYS) ")
    print("=" * 60)

    # Resample to weekly or ensure consistent daily frequency for statsmodels
    series = df["Sales"].asfreq("D").ffill()

    try:
        model = ExponentialSmoothing(
            series,
            trend="add",
            seasonal="add",
            seasonal_periods=7,
            initialization_method="estimated"
        ).fit()

        forecast_vals = model.forecast(forecast_days)
        # Residual variance for standard error estimation
        resid_std = np.std(model.resid)
    except Exception as e:
        print(f"[WARN] Holt-Winters fallback to linear trend ({e})")
        x = np.arange(len(series))
        poly = np.polyfit(x, series.values, 1)
        future_x = np.arange(len(series), len(series) + forecast_days)
        forecast_vals = pd.Series(np.polyval(poly, future_x), index=pd.date_range(start=series.index[-1] + pd.Timedelta(days=1), periods=forecast_days, freq="D"))
        resid_std = np.std(series.values - np.polyval(poly, x))

    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=forecast_days, freq="D")
    forecast_df = pd.DataFrame({
        "Forecast": np.round(forecast_vals.values, 2),
        "Upper_CI": np.round(forecast_vals.values + 1.96 * resid_std, 2),
        "Lower_CI": np.round(np.maximum(0, forecast_vals.values - 1.96 * resid_std), 2)
    }, index=future_dates)

    print(f"[SUCCESS] Forecast produced for {len(forecast_df)} forward days.")
    print(f"Mean Historical Sales: ${df['Sales'].mean():,.2f}")
    print(f"Projected Mean Future Sales: ${forecast_df['Forecast'].mean():,.2f}")
    return forecast_df


def plot_static_forecast(df, forecast_df, output_dir):
    """Renders high-resolution time-series chart with actuals, rolling averages, and forecast."""
    plt.figure(figsize=(14, 7))

    # Plot actuals and rolling averages
    plt.plot(df.index, df["Sales"], color="#bdc3c7", alpha=0.55, linewidth=1, label="Daily Actual Sales")
    plt.plot(df.index, df["SMA_7"], color="#3498db", linewidth=1.8, label="7-Day SMA")
    plt.plot(df.index, df["EMA_30"], color="#9b59b6", linewidth=2.2, label="30-Day EMA Trend")

    # Plot Bollinger bands fill
    plt.fill_between(df.index, df["BB_Lower"], df["BB_Upper"], color="#3498db", alpha=0.1, label="Bollinger Bands (20-day +/- 2σ)")

    # Plot forecast
    plt.plot(forecast_df.index, forecast_df["Forecast"], color="#e74c3c", linewidth=2.5, linestyle="--", label="Holt-Winters Statistical Forecast")
    plt.fill_between(forecast_df.index, forecast_df["Lower_CI"], forecast_df["Upper_CI"], color="#e74c3c", alpha=0.2, label="95% Forecast Confidence Interval")

    # Demarcation line
    plt.axvline(x=df.index[-1], color="#2c3e50", linestyle=":", linewidth=2, label="Forecast Horizon Boundary")

    plt.title("Commercial Sales Time-Series Analysis, Moving Averages & Holt-Winters Forecast", fontsize=14, weight="bold", pad=15)
    plt.xlabel("Timeline", fontsize=11, labelpad=10)
    plt.ylabel("Sales Volume (USD)", fontsize=11, labelpad=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.gca().yaxis.set_major_formatter("${x:,.0f}")
    plt.legend(loc="upper left", frameon=True, fontsize=9)

    output_path = os.path.join(output_dir, "exp8_time_series_forecasting.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[SAVED] Static time-series forecast plot saved to: {output_path}")


def plot_interactive_forecast(df, forecast_df, output_dir):
    """Creates an interactive Plotly time-series forecast with range slider and hover inspector."""
    fig = go.Figure()

    # Historical Actuals
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Sales"],
        name="Daily Actual Sales",
        mode="lines",
        line=dict(color="#bdc3c7", width=1),
        opacity=0.6,
        hovertemplate="Date: %{x|%Y-%m-%d}<br>Sales: $%{y:,.2f}<extra></extra>"
    ))

    # 7-day SMA
    fig.add_trace(go.Scatter(
        x=df.index, y=df["SMA_7"],
        name="7-Day SMA",
        mode="lines",
        line=dict(color="#2980b9", width=2),
        hovertemplate="7-Day SMA: $%{y:,.2f}<extra></extra>"
    ))

    # 30-day EMA
    fig.add_trace(go.Scatter(
        x=df.index, y=df["EMA_30"],
        name="30-Day EMA",
        mode="lines",
        line=dict(color="#8e44ad", width=2.5),
        hovertemplate="30-Day EMA: $%{y:,.2f}<extra></extra>"
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_df.index, y=forecast_df["Forecast"],
        name="Projected Forecast",
        mode="lines+markers",
        line=dict(color="#e74c3c", width=2.5, dash="dash"),
        marker=dict(size=4),
        hovertemplate="Forecast Date: %{x|%Y-%m-%d}<br>Forecast: $%{y:,.2f}<extra></extra>"
    ))

    # Upper CI
    fig.add_trace(go.Scatter(
        x=forecast_df.index, y=forecast_df["Upper_CI"],
        name="95% Upper Bound",
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))

    # Lower CI with fill
    fig.add_trace(go.Scatter(
        x=forecast_df.index, y=forecast_df["Lower_CI"],
        name="95% Confidence Interval",
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(231, 76, 60, 0.2)",
        hovertemplate="Lower 95% Bound: $%{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        title="<b>Interactive Sales Time-Series Forecasting & Moving Average Bands</b><br><sup>Statistical Holt-Winters Model with 60-Day Forward Forecast Horizon</sup>",
        template="plotly_white",
        hovermode="x unified",
        yaxis=dict(title="<b>Sales Revenue (USD)</b>", tickprefix="$", tickformat=",.0f"),
        xaxis=dict(
            title="<b>Timeline</b>",
            rangeslider=dict(visible=True),
            rangeselector=dict(
                buttons=list([
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="All")
                ])
            )
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80, b=40, l=60, r=40)
    )

    output_path = os.path.join(output_dir, "exp8_time_series_forecasting.html")
    fig.write_html(output_path)
    print(f"[SAVED] Interactive Plotly forecast saved to: {output_path}")


def main():
    print("Starting Experiment 8: Time-Series Forecasting & Moving Averages...")
    output_dir = get_output_dir()
    df_raw = generate_time_series_data()
    df_ma = calculate_moving_averages(df_raw)
    forecast_df = generate_forecast(df_raw, forecast_days=60)

    plot_static_forecast(df_ma, forecast_df, output_dir)
    plot_interactive_forecast(df_ma, forecast_df, output_dir)

    print("\n[SUCCESS] Experiment 8 completed successfully.")


if __name__ == "__main__":
    main()
