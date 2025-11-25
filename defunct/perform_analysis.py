import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from factor_analyzer import FactorAnalyzer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from scipy.stats import ttest_ind

# 1. Load Data
file_path = '/Users/rebeccanapolitano/antigravityProjects/FOUN/FOUN_boxes/2023_12_8_targeted_eval.csv'
df = pd.read_csv(file_path)

# 2. Preprocessing
# Drop non-numeric/coordinate columns
cols_to_drop = ['Unnamed: 0'] + [f'point {i}' for i in range(1, 10)]
df_clean = df.drop(columns=cols_to_drop, errors='ignore')

# Handle missing values (-1 often indicates missing in this dataset context, based on previous observations)
# We will replace -1 with NaN for specific columns where it makes sense (e.g., foundation attributes)
foundation_cols = ['elev 1 foundation disp', 'ele 1 foundation mortar condition', 
                   'ele 2 foundation displ', 'ele 2 foundation mortar condition', 
                   'Foundation Stone Deterioration']
for col in foundation_cols:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].replace(-1, np.nan)

# Impute NaN with median for numerical columns
imputer = SimpleImputer(strategy='median')
df_imputed = pd.DataFrame(imputer.fit_transform(df_clean), columns=df_clean.columns)

# 3. Correlation Analysis
# Focus on correlations with 'Total Scr' and 'Wall Rank'
target_vars = ['Total Scr', 'Wall Rank']
correlations = df_imputed.corr()

print("--- Top Correlations with Total Scr ---")
print(correlations['Total Scr'].sort_values(ascending=False).head(10))
print(correlations['Total Scr'].sort_values(ascending=False).tail(5))

# Generate Heatmap for a subset of interesting variables
# Select degradation metrics and some treatments
heatmap_cols = ['Total Scr', 'Wall Rank', 'Sill 1', 'Coat 1 Loss', 'Structural Cracking', 
                'Cracking Wall Junction', 'Out of Plane', 'Foundation Stone Deterioration',
                'treatment_5', 'treatment_1', 'Bracing', 'Height']
heatmap_cols = [c for c in heatmap_cols if c in df_imputed.columns]

plt.figure(figsize=(12, 10))
sns.heatmap(df_imputed[heatmap_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap: Key Degradation Metrics & Features')
plt.tight_layout()
plt.savefig('correlation_heatmap_new.png')
plt.close()

# 4. Factor Analysis
# Select degradation variables for FA
degradation_vars = ['Sill 1', 'Coat 1 Cracking', 'Coat 1 Loss', 'SILL 2', 'Coat2 Cracking', 
                    'Coat2 Loss', 'Cap Deterioration', 'Structural Cracking', 
                    'Cracking Wall Junction', 'Out of Plane', 'Lintel Deteriration', 
                    'Foundation Stone Deterioration']
# Filter to existing columns
degradation_vars = [c for c in degradation_vars if c in df_imputed.columns]

# Check adequacy (Bartlett/KMO is good practice but we'll skip for brevity and assume suitability)
fa = FactorAnalyzer(n_factors=3, rotation='varimax')
fa.fit(df_imputed[degradation_vars])

loadings = pd.DataFrame(fa.loadings_, index=degradation_vars, columns=['Factor 1', 'Factor 2', 'Factor 3'])
print("\n--- Factor Analysis Loadings ---")
print(loadings)

# Get factor scores
factor_scores = fa.transform(df_imputed[degradation_vars])
df_imputed['Factor_1_Score'] = factor_scores[:, 0]
df_imputed['Factor_2_Score'] = factor_scores[:, 1]
df_imputed['Factor_3_Score'] = factor_scores[:, 2]

# 5. Feature Importance (Random Forest)
# Predict 'Total Scr' using Treatments, Geometry, and Bracing
# Exclude the degradation metrics themselves (as they make up the score)
predictors = [c for c in df_imputed.columns if 'treatment' in c or '1960_treat' in c]
predictors += ['Height', 'foundation height', 'Bracing', 'fireplace']
predictors = [c for c in predictors if c in df_imputed.columns]

X = df_imputed[predictors]
y = df_imputed['Total Scr']

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)

feature_importances = pd.DataFrame({'Feature': predictors, 'Importance': rf.feature_importances_})
feature_importances = feature_importances.sort_values(by='Importance', ascending=False)

print("\n--- Random Forest Feature Importance (Top 10) ---")
print(feature_importances.head(10))

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importances.head(10))
plt.title('Feature Importance for Predicting Total Degradation Score')
plt.tight_layout()
plt.savefig('feature_importance_new.png')
plt.close()

# 6. Hypothesis Testing
# Compare Total Scr for top treatments
# Example: treatment_5 vs No treatment_5
top_treatments = feature_importances.head(3)['Feature'].tolist()
print("\n--- Hypothesis Testing (T-test) ---")
for treat in top_treatments:
    # Check if binary
    if df_imputed[treat].nunique() == 2:
        group1 = df_imputed[df_imputed[treat] == 1]['Total Scr']
        group0 = df_imputed[df_imputed[treat] == 0]['Total Scr']
        t_stat, p_val = ttest_ind(group1, group0, equal_var=False)
        print(f"Treatment: {treat}")
        print(f"  Mean Score (Treated): {group1.mean():.2f}")
        print(f"  Mean Score (Untreated): {group0.mean():.2f}")
        print(f"  T-statistic: {t_stat:.4f}, P-value: {p_val:.4f}")
        if p_val < 0.05:
            print("  Result: Significant Difference")
        else:
            print("  Result: No Significant Difference")
        print("-" * 30)
