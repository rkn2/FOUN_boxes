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
    Generate Random Forest feature importance plot with comprehensive metrics.
    
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
        
    Returns:
    --------
    dict : Dictionary containing all model metrics
    """
    from sklearn.model_selection import cross_val_score, cross_val_predict
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.inspection import permutation_importance
    
    # Separate features (X) and target (y)
    # TEACHING POINT: Never include the target in the feature set (data leakage!)
    X = df.drop(columns=['Total Scr'])
    y = df['Total Scr']
    
    print(f"Training Random Forest with {X.shape[1]} features on n={len(df)} samples...")
    print(f"Feature-to-sample ratio: 1:{len(df)/X.shape[1]:.2f}")
    
    # Train Random Forest with hyperparameters as specified in paper
    # n_estimators=100: Use 100 decision trees (more = stable but slower)
    # random_state=42: Reproducible results for teaching/debugging
    rf = RandomForestRegressor(
        n_estimators=100, 
        random_state=42,
        max_depth=None,  # Unrestricted depth
        min_samples_split=2,
        oob_score=True  # Enable out-of-bag scoring
    )
    rf.fit(X, y)
    
    # Calculate performance metrics
    print("\n" + "="*60)
    print("MODEL PERFORMANCE METRICS")
    print("="*60)
    
    # Out-of-bag error
    oob_score = rf.oob_score_
    print(f"Out-of-Bag R² Score: {oob_score:.4f}")
    
    # 5-fold cross-validation
    cv_scores = cross_val_score(rf, X, y, cv=5, scoring='r2')
    cv_predictions = cross_val_predict(rf, X, y, cv=5)
    
    r2_cv = np.mean(cv_scores)
    r2_cv_std = np.std(cv_scores)
    rmse_cv = np.sqrt(mean_squared_error(y, cv_predictions))
    mae_cv = mean_absolute_error(y, cv_predictions)
    
    print(f"5-Fold Cross-Validation R²: {r2_cv:.4f} (±{r2_cv_std:.4f})")
    print(f"Cross-Validation RMSE: {rmse_cv:.4f}")
    print(f"Cross-Validation MAE: {mae_cv:.4f}")
    
    # Training performance (for comparison - may indicate overfitting if much better than CV)
    y_pred_train = rf.predict(X)
    r2_train = r2_score(y, y_pred_train)
    rmse_train = np.sqrt(mean_squared_error(y, y_pred_train))
    mae_train = mean_absolute_error(y, y_pred_train)
    
    print(f"\nTraining Set Performance (reference):")
    print(f"  R²: {r2_train:.4f}")
    print(f"  RMSE: {rmse_train:.4f}")
    print(f"  MAE: {mae_train:.4f}")
    
    if r2_train - r2_cv > 0.15:
        print("  ⚠ Warning: Large train-CV gap suggests potential overfitting")
    
    # Extract mean decrease in impurity importances
    importances_mdi = rf.feature_importances_
    
    # Calculate permutation importance with standard errors
    print("\nCalculating permutation importance (this may take a moment)...")
    perm_importance = permutation_importance(
        rf, X, y, 
        n_repeats=30,  # 30 permutations for stable estimates
        random_state=42,
        n_jobs=-1  # Use all CPUs
    )
    
    importances_perm = perm_importance.importances_mean
    importances_perm_std = perm_importance.importances_std
    
    # Sort by mean decrease in impurity for plotting
    indices = np.argsort(importances_mdi)[::-1]  # Sort descending
    
    # Top 10 features (for readability)
    top_n = 10
    top_indices = indices[:top_n]
    
    # Create bar plot
    plt.figure(figsize=(12, 6))
    colors = sns.color_palette("viridis", top_n)
    plt.barh(range(top_n), importances_mdi[top_indices], color=colors)
    plt.yticks(range(top_n), X.columns[top_indices])
    plt.gca().invert_yaxis()  # Highest importance at top
    
    plt.title('Top 10 Predictors of Adobe Wall Degradation (Random Forest)', pad=20)
    plt.xlabel('Feature Importance (Mean Decrease in Impurity)')
    plt.ylabel('Feature')
    
    # Add importance values as text annotations
    for i, (idx, val) in enumerate(zip(top_indices, importances_mdi[top_indices])):
        plt.text(val + 0.005, i, f'{val:.3f}', va='center')
    
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"\n✓ Saved feature importance plot to {output_path}")
    
    # Print detailed results for reporting
    print("\n" + "="*60)
    print("TOP 10 MOST IMPORTANT FEATURES")
    print("="*60)
    print(f"{'Rank':<5} {'Feature':<30} {'MDI':<10} {'Perm±SE'}")
    print("-"*60)
    for i, idx in enumerate(top_indices, 1):
        feature_name = X.columns[idx]
        mdi_val = importances_mdi[idx]
        perm_val = importances_perm[idx]
        perm_se = importances_perm_std[idx]
        print(f"{i:<5} {feature_name:<30} {mdi_val:.4f}    {perm_val:.4f}±{perm_se:.4f}")
    
    # Compile metrics dictionary
    metrics = {
        'n_samples': len(df),
        'n_features': X.shape[1],
        'oob_r2': oob_score,
        'cv_r2_mean': r2_cv,
        'cv_r2_std': r2_cv_std,
        'cv_rmse': rmse_cv,
        'cv_mae': mae_cv,
        'train_r2': r2_train,
        'feature_names': X.columns.tolist(),
        'importances_mdi': importances_mdi.tolist(),
        'importances_perm_mean': importances_perm.tolist(),
        'importances_perm_std': importances_perm_std.tolist(),
        'top_features': [X.columns[idx] for idx in top_indices],
        'top_importances_mdi': [importances_mdi[idx] for idx in top_indices],
        'top_importances_perm': [importances_perm[idx] for idx in top_indices],
        'top_importances_perm_std': [importances_perm_std[idx] for idx in top_indices]
    }
    
    return metrics

if __name__ == "__main__":
    # ========================================================================
    # MAIN EXECUTION
    # ========================================================================
    import json
    
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
    generate_correlation_heatmap(df, 'journalPaper/Images/correlation_heatmap.png')
    
    # Step 3: Generate feature importance and capture metrics
    print("\n" + "-"*70)
    print("Generating Feature Importance Plot...")
    print("-"*70)
    metrics = generate_feature_importance(df, 'journalPaper/Images/feature_importance.png')
    
    # Save metrics to JSON for LaTeX integration
    metrics_file = 'journalPaper/model_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\n✓ Saved model metrics to {metrics_file}")
    
    print("\n" + "="*70)
    print("✓ All figures and metrics generated successfully!")
    print("="*70)
    print("\nGenerated outputs:")
    print("1. Correlation heatmap: journalPaper/Images/correlation_heatmap.png")
    print("2. Feature importance plot: journalPaper/Images/feature_importance.png")
    print("3. Model metrics (JSON): journalPaper/model_metrics.json")
    print("\nMetrics Summary:")
    print(f"  - Cross-Validation R²: {metrics['cv_r2_mean']:.4f} (±{metrics['cv_r2_std']:.4f})")
    print(f"  - CV RMSE: {metrics['cv_rmse']:.4f}")
    print(f"  - CV MAE: {metrics['cv_mae']:.4f}")
    print(f"  - OOB R²: {metrics['oob_r2']:.4f}")
    print(f"\nTop 3 Features:")
    for i in range(min(3, len(metrics['top_features']))):
        print(f"  {i+1}. {metrics['top_features'][i]}: {metrics['top_importances_mdi'][i]:.4f}")
    print("\nNext steps:")
    print("1. Review figures in 'journalPaper/Images/' directory")
    print("2. Metrics will be auto-inserted into LaTeX document")
    print("3. Interpret results in context of preservation planning\n")
