# Data Visualization (DV) & Machine Learning (ML) Lab Coursework

**Author:** Aviral Pandey  
**Repository:** [ML-DV-Lab-Exp---Aviral-Pandey](https://github.com/aviralp1910-bot/ML-DV-Lab-Exp---Aviral-Pandey)

---

## 📁 Repository Structure

```text
├── ML/                                        # Machine Learning Lab Experiments
│   ├── exp1_simple_linear_regression.py       # Exp 1: Simple Linear Regression
│   ├── exp2_multiple_linear_regression.py     # Exp 2: Multiple Linear Regression
│   ├── exp3_logistic_regression.py            # Exp 3: Logistic Regression (Breast Cancer)
│   ├── exp4_regularized_regression.py         # Exp 4: Ridge, Lasso, & ElasticNet Regression
│   ├── exp5_pca_dimensionality_reduction.py   # Exp 5: PCA Dimensionality Reduction (Wine)
│   ├── exp6_support_vector_machine.py         # Exp 6: SVM Classification (Linear, Poly, RBF)
│   ├── exp7_decision_tree_real_world.py       # Exp 7: Decision Tree on Iris Dataset
│   ├── exp8_naive_bayes_classifier.py         # Exp 8: Gaussian Naive Bayes Classifier
│   ├── exp9_kmeans_clustering.py              # Exp 9: K-Means Clustering (Elbow & Silhouette)
│   ├── outputs/                               # Generated High-Res Diagnostic Plots (.png)
│   ├── .gitkeep
│   └── README.md                              # Detailed ML module guide
├── DV/                                        # Data Visualization Lab Experiments
│   ├── exp1_getting_started_views.py          # Exp 1: Table Summary, Bar & Line Charts
│   ├── exp2_data_cleaning_transformation.py   # Exp 2: Missing Values, Types, & Calculated Fields
│   ├── exp3_bar_line_series.py                # Exp 3: Plotly Bar & Line Series with Tooltips
│   ├── exp4_interactive_dashboard.py          # Exp 4: Interactive Retail Dashboard (Dropdowns & Sliders)
│   ├── exp5_geo_visualization.py              # Exp 5: Choropleth & Symbol Maps (Plotly Express)
│   ├── exp6_pie_donut_charts.py               # Exp 6: Olympic Medals Pie & Donut Proportions
│   ├── exp7_heatmaps_treemaps.py              # Exp 7: Correlation Heatmap & Hierarchical Treemap
│   ├── exp8_time_series_forecasting.py        # Exp 8: Moving Averages & Holt-Winters Forecasting
│   └── outputs/                               # Generated High-Res PNGs & Interactive HTMLs
├── requirements.txt                           # Complete project dependencies
├── .gitignore                                 # Standard Git ignore rules
└── README.md                                  # Complete repository documentation
```

---

## 🤖 Part 1: Machine Learning (ML) Experiments Overview

| # | Script Name | Algorithm / Experiment | Dataset | Key Metrics / Highlights | Output Artifacts |
|---|---|---|---|---|---|
| **1** | [`exp1_simple_linear_regression.py`](ML/exp1_simple_linear_regression.py) | **Simple Linear Regression** | Experience vs Salary | $R^2$, MAE, MSE, RMSE, Fitted slope & intercept | `exp1_simple_linear_regression.png` |
| **2** | [`exp2_multiple_linear_regression.py`](ML/exp2_multiple_linear_regression.py) | **Multiple Linear Regression** | Housing Attributes | $R^2$, Adjusted $R^2$, RMSE, Homoscedasticity | `exp2_multiple_linear_regression.png` |
| **3** | [`exp3_logistic_regression.py`](ML/exp3_logistic_regression.py) | **Logistic Regression** | Breast Cancer Wisconsin | Confusion Matrix, Accuracy, Precision, Recall, F1, ROC-AUC | `exp3_logistic_regression.png` |
| **4** | [`exp4_regularized_regression.py`](ML/exp4_regularized_regression.py) | **Regularized Regression** (Ridge, Lasso, ElasticNet) | Collinear Multi-Feature Space | Coefficient Shrinkage, Feature Sparsity, Test RMSE | `exp4_regularized_regression.png` |
| **5** | [`exp5_pca_dimensionality_reduction.py`](ML/exp5_pca_dimensionality_reduction.py) | **Dimensionality Reduction (PCA)** | Wine Recognition (13 features) | Scree Plot, Explained Variance %, 2D projection | `exp5_pca_dimensionality_reduction.png` |
| **6** | [`exp6_support_vector_machine.py`](ML/exp6_support_vector_machine.py) | **Support Vector Machines (SVM)** | Non-Linear Moons | Linear, Poly, RBF Kernels, Support Vector Count | `exp6_support_vector_machine.png` |
| **7** | [`exp7_decision_tree_real_world.py`](ML/exp7_decision_tree_real_world.py) | **Decision Tree Classifier** | Iris Flower Benchmark | Gini Impurity, Full Tree Flowchart, Feature Importance | `exp7_decision_tree.png` |
| **8** | [`exp8_naive_bayes_classifier.py`](ML/exp8_naive_bayes_classifier.py) | **Gaussian Naive Bayes** | Wine Chemical Dataset | Prior $P(Y)$, Class Likelihoods, Posterior $P(Y\|X)$ | `exp8_naive_bayes.png` |
| **9** | [`exp9_kmeans_clustering.py`](ML/exp9_kmeans_clustering.py) | **K-Means Clustering** | Customer Annual Spend | Elbow Method (Inertia), Silhouette Score, Centroids | `exp9_kmeans_clustering.png` |

---

## 📊 Part 2: Data Visualization (DV) Experiments Overview

| # | Script Name | Visualization / Topic | Engine | Output Artifacts |
|---|---|---|---|---|
| **1** | [`exp1_getting_started_views.py`](DV/exp1_getting_started_views.py) | Table Summary, Bar Chart, & Monthly Line Chart | Matplotlib / Seaborn | `exp1_summary_table.png`<br>`exp1_bar_chart.png`<br>`exp1_line_chart.png` |
| **2** | [`exp2_data_cleaning_transformation.py`](DV/exp2_data_cleaning_transformation.py) | Missing Values Imputation & Calculated Fields | Pandas / Matplotlib | `exp2_missing_values_cleaning.png`<br>`exp2_calculated_fields.png` |
| **3** | [`exp3_bar_line_series.py`](DV/exp3_bar_line_series.py) | Category Bar & Spline Line with Range Slider | Plotly Express / Graph Objects | `exp3_category_bar.html`<br>`exp3_trend_line.html`<br>`exp3_combined_bar_line.html` |
| **4** | [`exp4_interactive_dashboard.py`](DV/exp4_interactive_dashboard.py) | Retail Dashboard with Dynamic Dropdowns & KPI Cards | Plotly Subplots | `exp4_retail_dashboard.html` |
| **5** | [`exp5_geo_visualization.py`](DV/exp5_geo_visualization.py) | Global Choropleth & Proportional Symbol Maps | Plotly Express | `exp5_choropleth_map.html`<br>`exp5_symbol_map.html` |
| **6** | [`exp6_pie_donut_charts.py`](DV/exp6_pie_donut_charts.py) | Olympic Medal Share Exploded Pie & Donut KPI | Plotly & Matplotlib | `exp6_pie_donut_charts.html`<br>`exp6_pie_donut_charts.png` |
| **7** | [`exp7_heatmaps_treemaps.py`](DV/exp7_heatmaps_treemaps.py) | Pearson Correlation Matrix & Hierarchical Treemap | Seaborn & Plotly Express | `exp7_correlation_heatmap.png`<br>`exp7_hierarchical_treemap.html` |
| **8** | [`exp8_time_series_forecasting.py`](DV/exp8_time_series_forecasting.py) | Moving Averages (SMA/EMA) & Holt-Winters Forecasting | Statsmodels & Plotly | `exp8_time_series_forecasting.png`<br>`exp8_time_series_forecasting.html` |

---

## 🚀 Setup & Execution Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Experiments

**To run any ML experiment:**
```bash
python ML/exp1_simple_linear_regression.py
python ML/exp2_multiple_linear_regression.py
python ML/exp3_logistic_regression.py
python ML/exp4_regularized_regression.py
python ML/exp5_pca_dimensionality_reduction.py
python ML/exp6_support_vector_machine.py
python ML/exp7_decision_tree_real_world.py
python ML/exp8_naive_bayes_classifier.py
python ML/exp9_kmeans_clustering.py
```

**To run any DV experiment:**
```bash
python DV/exp1_getting_started_views.py
python DV/exp2_data_cleaning_transformation.py
python DV/exp3_bar_line_series.py
python DV/exp4_interactive_dashboard.py
python DV/exp5_geo_visualization.py
python DV/exp6_pie_donut_charts.py
python DV/exp7_heatmaps_treemaps.py
python DV/exp8_time_series_forecasting.py
```

---
*(C) Aviral Pandey - Machine Learning & Data Visualization Coursework*
