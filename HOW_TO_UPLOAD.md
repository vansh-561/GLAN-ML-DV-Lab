# 🚀 Student Lab Submission Guide: How to Upload Your Files

This guide explains how to upload your Machine Learning (ML) and Data Visualization (DV) lab experiment files to this repository.

---

## 📋 Allowed File Formats

| Lab | Accepted File Types | Description |
|---|---|---|
| **Machine Learning Lab** | `.ipynb`, `.py` | Jupyter Notebook or Python script |
| **Data Visualization Lab** | `.pbix`, `.ipynb` | Power BI report file, Python notebook, or Tableau workbook (`.twbx`) |

---

## 📁 Recommended Folder Organization

Inside your personal folder (`<Section>/<Your Name>/`), you can either place your files directly or organize them by lab:

```text
ND/ or NE/
└── <Your Name>/
    ├── ML_Lab/
    │   ├── ML_Exp1_Simple_Linear_Regression.ipynb
    │   ├── ML_Exp2_Multiple_Linear_Regression.ipynb
    │   └── ...
    └── DV_Lab/
        ├── DV_Exp1_Getting_Started.pbix
        ├── DV_Exp2_Interactive_Dashboard.pbix
        └── ...
```

### 🏷️ Recommended File Naming Convention
- **ML Lab**: `ML_Exp<No>_<Topic_Name>.<extension>`
  - *Example:* `ML_Exp1_Simple_Linear_Regression.ipynb` or `ML_Exp3_Logistic_Regression.py`
- **DV Lab**: `DV_Exp<No>_<Topic_Name>.<extension>`
  - *Example:* `DV_Exp1_Getting_Started.pbix` or `DV_Exp5_GeoVisualization.ipynb`

---

## 🌐 Method 1: Upload via GitHub Web Interface (Easiest)

If you prefer uploading directly from your web browser:

1. **Open the Repository:**
   - Go to [GLAN-ML-DV-Lab on GitHub](https://github.com/vansh-561/GLAN-ML-DV-Lab).

2. **Navigate to Your Section & Folder:**
   - Click on your section: **`ND/`** or **`NE/`**.
   - Find and click on your **own name folder** (e.g., `NE/Aditya Chaudhary/`).

3. **Upload Your File:**
   - In the top right corner of the file list, click on **`Add file`** ▾ and select **`Upload files`**.
   - Drag and drop your file(s) (`.ipynb`, `.py`, `.pbix`) into the upload box, or click **choose your files**.

4. **Commit the Changes:**
   - Scroll down to the **Commit changes** box.
   - Enter a brief message, for example:
     > `Add ML Experiment 1 - Simple Linear Regression`
   - Ensure **"Commit directly to the `main` branch"** is selected (or create a new branch / pull request if instructed).
   - Click the green **`Commit changes`** button.

---

## 💻 Method 2: Upload via Git Command Line / VS Code

If you are using Git from your local machine:

1. **Clone the Repository (first time only):**
   ```bash
   git clone https://github.com/vansh-561/GLAN-ML-DV-Lab.git
   cd GLAN-ML-DV-Lab
   ```

2. **Pull the Latest Changes (always before adding new work):**
   ```bash
   git pull origin main
   ```

3. **Copy Your Experiment Files:**
   - Place your `.ipynb`, `.py`, or `.pbix` files into your folder:
     - For Section ND: `ND/<Your Name>/`
     - For Section NE: `NE/<Your Name>/`

4. **Stage and Commit Your Files:**
   ```bash
   # Stage only your folder
   git add "ND/<Your Name>/"   # or "NE/<Your Name>/"

   # Commit with a clear message
   git commit -m "Add ML Exp 1 - <Your Name>"
   ```

5. **Push Your Changes:**
   ```bash
   git push origin main
   ```

---

## ⚠️ Important Rules & Best Practices

1. **Respect Others' Folders:**
   - **Only** add or edit files inside your own designated folder. Never modify, delete, or overwrite another student's folder or root files.
2. **File Size Limit (100 MB):**
   - GitHub has a strict **100 MB file size limit**.
   - Power BI (`.pbix`) files can sometimes get large if datasets are imported. Ensure your `.pbix` file is under 100 MB.
   - Clear large cell outputs (especially images/large data frames) in `.ipynb` before saving to keep file sizes small.
3. **Do Not Upload Giant Datasets:**
   - Only upload your code, notebooks, and report files. If you used an external dataset, include a download link or markdown description rather than pushing large raw CSVs.
4. **Code Quality:**
   - Ensure your code has proper comments, headings, and clear outputs explaining the observations.
