"""
Generate Publication-Quality Figures for Adobe Degradation Analysis
===================================================================

Educational Purpose:
-------------------
This script demonstrates how to create publication-ready visualizations
from heritage structure assessment data. Graduate students will learn:
1. Data preprocessing techniques for field survey data
2. Correlation analysis visualization
3. Machine learning feature importance interpretation

Author: Rebecca Napolitano, Penn State University
Course: AE 597 - Diagnostics and Monitoring
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer

# ============================================================================
# PUBLICATION STYLE SETTINGS
# ============================================================================
# Set style for publication quality figures following journal standards
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.figsize': (10, 6),
    'figure.dpi': 300  # High resolution for publication
})

def load_and_preprocess_data(filepath):
    """
    Load and preprocess adobe degradation data.
    
    Educational Notes:
    ------------------
    - Field survey data often contains missing values (equipment failure, 
      inaccessible sections)
    - We use median imputation (robust to outliers) rather than mean
    - Columns with ALL missing data are dropped (measurement not applicable)
    
    Parameters:
    -----------
    filepath : str
        Path to CSV file with degradation data
        
    Returns:
    --------
    pd.DataFrame
        Cleaned and imputed dataset ready for analysis
    """
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Original shape: {df.shape}")
    
    # Columns to drop (identifiers, notes, etc. - not for statistical analysis)
    non_numeric_cols = ['Wall ID', 'Image Name', 'Notes', 'Date', 'Reviewer', 
                        'Wall Rank', 'Section ID']
    df_clean = df.drop(columns=[c for c in non_numeric_cols if c in df.columns])
    
    # Handle missing values
    # TEACHING POINT: Why median over mean?
    # - Median is robust to outliers (e.g., one extremely degraded wall)
    # - Mean can be skewed by measurement errors
    imputer = SimpleImputer(strategy='median')
    df_numeric = df_clean.select_dtypes(include=[np.number])
    
    # Drop columns that are all NaN before imputation to avoid issues
    # TEACHING POINT: This happens when a damage type doesn't apply to any walls
    # (e.g., lintel deterioration in walls without openings)
    original_cols = df_numeric.shape[1]
    df_numeric = df_numeric.dropna(axis=1, how='all')
    dropped_cols = original_cols - df_numeric.shape[1]
    if dropped_cols > 0:
        print(f"Dropped {dropped_cols} columns with all missing values")
    
    imputed_data = imputer.fit_transform(df_numeric)
    df_imputed = pd.DataFrame(imputed_data, columns=df_numeric.columns)
    
    print(f"Final shape after preprocessing: {df_imputed.shape}")
    print(f"Missing values remaining: {df_imputed.isnull().sum().sum()}")
    
    return df_imputed

def generate_correlation_heatmap(df, output_path):
    """
    Generate correlation matrix heatmap.
    
    Educational Notes:
    ------------------
    - Correlation (r) ranges from -1 to +1
    - r > 0.5: Strong positive correlation (variables increase together)
    - r < -0.5: Strong negative correlation (one ↑, other ↓)
    - r ≈ 0: No linear relationship
    
    In preservation context:
    - High correlations suggest coupled failure mechanisms
    - Example: If "Out of Plane" ↔ "Structural Cracking" have r=0.7,
      they likely share a common cause (e.g., foundation settlement)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed data
    output_path : str
        Where to save the figure
    """
    # Select key columns for a cleaner heatmap
    # TEACHING POINT: Don't include ALL 70+ columns - focus on actionable metrics
    key_cols = ['Total Scr', 'Cap Deterioration', 'Out of Plane', 'Height', 
                'Structural Cracking', 'Bracing', 'Sill 1', 'Sill 2', 
                'Coat 1 Cracking', 'Lintel Deterioration', 'Foundation Height']
    
    # Ensure columns exist (some may have been dropped)
    available_cols = [c for c in key_cols if c in df.columns]
    corr_matrix = df[available_cols].corr()
    
    # Create figure
    plt.figure(figsize=(12, 10))
    
    # Mask for upper triangle (avoid redundancy - matrix is symmetric)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Create heatmap
    # TEACHING POINT: 'coolwarm' colormap - red=positive correlation, blue=negative
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', 
                vmax=1, vmin=-1, center=0, square=True, linewidths=.5, 
                cbar_kws={"shrink": .5, "label": "Pearson Correlation (r)"})
    
    plt.title('Correlation Matrix of Key Degradation Metrics', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved correlation heatmap to {output_path}")

def generate_feature_importance(df, output_path):
    """
    Generate Random Forest feature importance plot.
    
    Educational Notes:
    ------------------
    Feature Importance Metric: Mean Decrease in Impurity (Gini Importance)
    - Measures how much each feature contributes to reducing prediction error
    - Higher value = more important for predicting Total Degradation
    - Useful for identifying PRIMARY DRIVERS of damage (not just correlations)
    
    Why Random Forest?
    - Handles nonlinear relationships (e.g., damage accelerates exponentially)
    - Robust to multicollinearity (many heritage metrics are correlated)
    - Provides importance scores without assuming linear models
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed data with 'Total Scr' as target variable
    output_path : str
        Where to save the figure
    """
    # Separate features (X) and target (y)
    # TEACHING POINT: Never include the target in the feature set (data leakage!)
    X = df.drop(columns=['Total Scr'])
    y = df['Total Scr']
    
    print(f"Training Random Forest with {X.shape[1]} features...")
    
    # Train Random Forest
    # n_estimators=100: Use 100 decision trees (more = stable but slower)
    # random_state=42: Reproducible results for teaching/debugging
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    # Extract importances
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]  # Sort descending
    
    # Top 10 features (for readability)
    top_n = 10
    top_indices = indices[:top_n]
    
    # Create bar plot
    plt.figure(figsize=(12, 6))
    colors = sns.color_palette("viridis", top_n)
    plt.barh(range(top_n), importances[top_indices], color=colors)
    plt.yticks(range(top_n), X.columns[top_indices])
    plt.gca().invert_yaxis()  # Highest importance at top
    
    plt.title('Top 10 Predictors of Adobe Wall Degradation (Random Forest)', pad=20)
    plt.xlabel('Feature Importance (Mean Decrease in Impurity)')
    plt.ylabel('Feature')
    
    # Add importance values as text annotations
    for i, (idx, val) in enumerate(zip(top_indices, importances[top_indices])):
        plt.text(val + 0.005, i, f'{val:.3f}', va='center')
    
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved feature importance plot to {output_path}")
    
    # Print numerical results for reporting
    print("\nTop 10 Most Important Features:")
    print("="*50)
    for i, idx in enumerate(top_indices, 1):
        print(f"{i:2d}. {X.columns[idx]:30s} {importances[idx]:.4f}")

if __name__ == "__main__":
    # ========================================================================
    # MAIN EXECUTION
    # ========================================================================
    
    # Use SYNTHETIC DATA (not real FOUN data - privacy protection)
    # To use real data: replace with '2023_12_8_targeted_eval.csv'
    data_path = 'synthetic_adobe_data.csv'
    
    print("\n" + "="*70)
    print("ADOBE DEGRADATION ANALYSIS - Figure Generation")
    print("="*70 + "\n")
    
    # Step 1: Load and preprocess
    df = load_and_preprocess_data(data_path)
    
    # Step 2: Generate correlation heatmap
    print("\n" + "-"*70)
    print("Generating Correlation Heatmap...")
    print("-"*70)
    generate_correlation_heatmap(df, 'texfigures/correlation_heatmap.png')
    
    # Step 3: Generate feature importance
    print("\n" + "-"*70)
    print("Generating Feature Importance Plot...")
    print("-"*70)
    generate_feature_importance(df, 'texfigures/feature_importance.png')
    
    print("\n" + "="*70)
    print("✓ All figures generated successfully!")
    print("="*70)
    print("\nNext steps:")
    print("1. View figures in 'texfigures/' directory")
    print("2. Include in LaTeX document: \\includegraphics{texfigures/correlation_heatmap.png}")
    print("3. Interpret results in context of preservation planning\n")

