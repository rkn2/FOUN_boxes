# Analysis Plan for Fort Union Degradation

## 1. Data Preparation
- **Load Data**: Use `2023_12_8_targeted_eval.csv`.
- **Preprocessing**:
    - Drop coordinate columns (`point 1` to `point 9`) as they are raw spatial data.
    - Set `Unnamed: 0` as the Index (Block ID).
    - Check for and handle missing values (e.g., replace `-1` with `NaN` or appropriate value if `-1` indicates missing/not applicable).
    - Verify data types (ensure numeric columns are actually numeric).

## 2. Exploratory Data Analysis (EDA)
- **Distributions**: Plot histograms of key degradation metrics (`Wall Rank`, `Total Scr`, `Coat Loss`) to understand their spread.
- **Correlation Matrix**:
    - Calculate correlations between degradation metrics and continuous features (`Height`, `PC mean`).
    - Calculate correlations between degradation metrics and binary treatment variables.
    - Visualize with a heatmap to identify strong positive/negative associations.

## 3. Factor Analysis (Degradation Index)
- **Objective**: Reduce the multiple degradation scores (`Sill 1`, `Coat 1 Cracking`, `Cap Deterioration`, etc.) into a smaller number of latent factors (e.g., "Structural Integrity", "Surface Wear").
- **Method**:
    - Use `FactorAnalyzer` or PCA.
    - Determine the optimal number of factors (Scree plot).
    - Interpret the factors based on loadings.
    - **Output**: Create new "Factor Scores" for each block to use as robust target variables.

## 4. Feature Importance & Predictive Modeling
- **Objective**: Determine which factors (Treatments, Geometry, Foundation) best predict degradation.
- **Method**:
    - Train a **Random Forest Regressor** to predict the "Degradation Factor(s)" or `Total Scr`.
    - Extract **Feature Importance** scores to rank predictors.
    - Use **SHAP (SHapley Additive exPlanations)** values to explain *how* each feature affects degradation (e.g., does `treatment_5` increase or decrease degradation?).

## 5. Hypothesis Testing (Statistical Validation)
- **T-tests / Mann-Whitney U tests**: Compare degradation scores between treated and untreated groups for key treatments.
- **ANOVA**: If there are categorical groups (e.g., `Wall Rank` groups), compare means of other variables.

## 6. Reporting
- Generate visualizations:
    - Correlation Heatmap.
    - Feature Importance Bar Chart.
    - SHAP Summary Plot.
    - Factor Loading Plot.
- Summarize findings for the paper.
