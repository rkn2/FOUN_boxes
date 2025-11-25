"""
Verification and Supplemental Analysis for FOUN Manuscript Revisions
=====================================================================

This script:
1. Verifies Factor Analysis communalities calculation
2. Runs supplemental Random Forest WITHOUT damage indicators
3. Provides intervention matrix priority score examples
"""

import pandas as pd
import numpy as np
import json
from scipy.stats import pearsonr
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.inspection import permutation_importance
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_preprocess_data(filepath):
    """Load and preprocess data"""
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Original shape: {df.shape}")
    
    non_numeric_cols = ['Wall ID', 'Image Name', 'Notes', 'Date', 'Reviewer', 
                        'Wall Rank', 'Section ID']
    df_clean = df.drop(columns=[c for c in non_numeric_cols if c in df.columns])
    
    imputer = SimpleImputer(strategy='median')
    df_numeric = df_clean.select_dtypes(include=[np.number])
    df_numeric = df_numeric.dropna(axis=1, how='all')
    
    imputed_data = imputer.fit_transform(df_numeric)
    df_imputed = pd.DataFrame(imputed_data, columns=df_numeric.columns)
    
    print(f"Final shape: {df_imputed.shape}")
    return df_imputed

def verify_factor_analysis_communalities(df):
    """
    Verify Factor Analysis communalities calculation
    """
    print("\n" + "="*70)
    print("FACTOR ANALYSIS COMMUNALITY VERIFICATION")
    print("="*70)
    
    fa_vars = ['Sill 1', 'Sill 2', 'Coat 1 Cracking', 'Coat 1 Loss',
               'Lintel Deterioration', 'Coat 2 Cracking', 
               'Structural Cracking', 'Out of Plane']
    
    available_vars = [v for v in fa_vars if v in df.columns]
    df_fa = df[available_vars]
    
    # Run Factor Analysis
    fa = FactorAnalyzer(n_factors=3, rotation='varimax')
    fa.fit(df_fa)
    
    # Get loadings
    loadings = fa.loadings_
    loadings_df = pd.DataFrame(
        loadings,
        index=available_vars,
        columns=['Factor 1', 'Factor 2', 'Factor 3']
    )
    
    print("\nFactor Loadings (all values):")
    print(loadings_df.round(4))
    
    # Calculate communalities manually
    print("\n" + "-"*70)
    print("COMMUNALITY CALCULATION VERIFICATION")
    print("-"*70)
    print(f"{'Variable':<30} {'Manual Calc':<15} {'get_communalities()':<20} {'Match?'}")
    print("-"*70)
    
    communalities_auto = fa.get_communalities()
    
    for i, var in enumerate(available_vars):
        # Manual calculation: sum of squared loadings
        manual_comm = (loadings[i, 0]**2 + loadings[i, 1]**2 + loadings[i, 2]**2)
        auto_comm = communalities_auto[i]
        match = "✓" if abs(manual_comm - auto_comm) < 0.01 else "✗"
        
        print(f"{var:<30} {manual_comm:<15.4f} {auto_comm:<20.4f} {match}")
    
    # Check for Heywood cases (communalities > 1)
    heywood_cases = [(available_vars[i], communalities_auto[i]) 
                     for i in range(len(available_vars)) 
                     if communalities_auto[i] > 1.0]
    
    if heywood_cases:
        print("\n⚠️  WARNING: Heywood Cases Detected (communalities > 1.0):")
        for var, comm in heywood_cases:
            print(f"   {var}: {comm:.4f}")
        print("\n   This indicates:")
        print("   - Possible model misspecification")
        print("   - May need more factors or different rotation")
        print("   - Or numerical precision issues")
    
    return {
        'loadings': loadings_df.to_dict(),
        'communalities': {var: float(comm) for var, comm in zip(available_vars, communalities_auto)},
        'heywood_cases': heywood_cases
    }

def run_supplemental_rf_geometric_only(df):
    """
    Supplemental Analysis: Random Forest using ONLY geometric/non-damage features
    """
    print("\n" + "="*70)
    print("SUPPLEMENTAL RANDOM FOREST: GEOMETRIC FACTORS ONLY")
    print("="*70)
    
    # Define damage indicators to EXCLUDE
    damage_indicators = [
        'Cap Deterioration', 'Out of Plane', 'Structural Cracking',
        'Cracking Junction', 'Sill 1', 'Sill 2',
        'Coat 1 Cracking', 'Coat 1 Loss', 'Coat 2 Cracking', 'Coat 2 Loss',
        'Lintel Deterioration', 'Surface Loss Top', 'Surface Loss Mid', 'Surface Loss Low',
        'Foundation Displacement 1', 'Foundation Displacement 2',
        'Foundation Mortar 1', 'Foundation Mortar 2', 'Foundation Stone Det'
    ]
    
    # Geometric and contextual features
    geometric_features = [
        'Height', 'Foundation Height', 'Treatment', 'Bracing', 'Bracing Score',
        'Animal Activity', 'Fireplace', 'Point Cloud Mean', 'Point Cloud Deviation'
    ]
    
    # Select available geometric features
    available_geom = [f for f in geometric_features if f in df.columns]
    
    if 'Total Scr' not in df.columns:
        print("ERROR: Total Scr not found")
        return None
    
    X_geom = df[available_geom]
    y = df['Total Scr']
    
    print(f"\nPredicting Total Scr using {len(available_geom)} geometric/contextual features:")
    for feat in available_geom:
        print(f"  - {feat}")
    
    # Train RF with same hyperparameters
    rf_geom = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=None,
        min_samples_split=2,
        oob_score=True
    )
    rf_geom.fit(X_geom, y)
    
    # Performance metrics
    print("\n" + "-"*70)
    print("MODEL PERFORMANCE (Geometric Features Only)")
    print("-"*70)
    
    oob_score = rf_geom.oob_score_
    print(f"Out-of-Bag R²: {oob_score:.4f}")
    
    cv_scores = cross_val_score(rf_geom, X_geom, y, cv=5, scoring='r2')
    cv_predictions = cross_val_predict(rf_geom, X_geom, y, cv=5)
    
    r2_cv = np.mean(cv_scores)
    r2_cv_std = np.std(cv_scores)
    rmse_cv = np.sqrt(mean_squared_error(y, cv_predictions))
    mae_cv = mean_absolute_error(y, cv_predictions)
    
    print(f"5-Fold CV R²: {r2_cv:.4f} (±{r2_cv_std:.4f})")
    print(f"CV RMSE: {rmse_cv:.4f}")
    print(f"CV MAE: {mae_cv:.4f}")
    
    # Feature importances
    importances_mdi = rf_geom.feature_importances_
    
    # Permutation importance
    print("\nCalculating permutation importance...")
    perm_importance = permutation_importance(
        rf_geom, X_geom, y,
        n_repeats=30,
        random_state=42,
        n_jobs=-1
    )
    
    importances_perm = perm_importance.importances_mean
    importances_perm_std = perm_importance.importances_std
    
    # Sort by MDI
    indices = np.argsort(importances_mdi)[::-1]
    
    print("\n" + "-"*70)
    print("FEATURE IMPORTANCES (Geometric Features)")
    print("-"*70)
    print(f"{'Rank':<5} {'Feature':<30} {'MDI':<10} {'Perm±SE'}")
    print("-"*70)
    
    for i, idx in enumerate(indices, 1):
        feat = available_geom[idx]
        mdi = importances_mdi[idx]
        perm = importances_perm[idx]
        perm_se = importances_perm_std[idx]
        print(f"{i:<5} {feat:<30} {mdi:.4f}    {perm:.4f}±{perm_se:.4f}")
    
    # Create figure
    plt.figure(figsize=(10, 6))
    colors = sns.color_palette("viridis", len(available_geom))
    y_pos = range(len(available_geom))
    
    plt.barh(y_pos, importances_mdi[indices], color=colors)
    plt.yticks(y_pos, [available_geom[i] for i in indices])
    plt.gca().invert_yaxis()
    
    plt.title('Feature Importance: Geometric/Contextual Factors Only\n(Excluding All Damage Indicators)', pad=15)
    plt.xlabel('Feature Importance (Mean Decrease in Impurity)')
    plt.ylabel('Feature')
    
    for i, (idx, val) in enumerate(zip(indices, importances_mdi[indices])):
        plt.text(val + 0.005, i, f'{val:.3f}', va='center')
    
    plt.tight_layout()
    plt.savefig('journalPaper/Images/feature_importance_geometric_only.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\n✓ Saved figure: journalPaper/Images/feature_importance_geometric_only.png")
    
    return {
        'n_features': len(available_geom),
        'features': available_geom,
        'oob_r2': float(oob_score),
        'cv_r2_mean': float(r2_cv),
        'cv_r2_std': float(r2_cv_std),
        'cv_rmse': float(rmse_cv),
        'cv_mae': float(mae_cv),
        'importances_mdi': importances_mdi.tolist(),
        'importances_perm_mean': importances_perm.tolist(),
        'importances_perm_std': importances_perm_std.tolist()
    }

def calculate_intervention_priority_example(fa_stats, rf_stats):
    """
    Work through intervention matrix priority score calculation example
    """
    print("\n" + "="*70)
    print("INTERVENTION MATRIX PRIORITY SCORE CALCULATION EXAMPLE")
    print("="*70)
    
    # Factor Analysis variance contributions
    f1_var = 26.1  # Factor 1
    f2_var = 24.9  # Factor 2
    f3_var = 14.0  # Factor 3
    max_var = f1_var
    
    print("\nFactor Analysis Variance Explained:")
    print(f"  Factor 1 (Sill Deterioration): {f1_var}%")
    print(f"  Factor 2 (Surface/Lintel): {f2_var}%")
    print(f"  Factor 3 (Structural Instability): {f3_var}%")
    
    print("\n" + "-"*70)
    print("EXAMPLE: Structural Instability (Factor 3)")
    print("-"*70)
    
    # Method 1: Based on variance explained
    priority_variance = 10 * (f3_var / max_var)
    print(f"\nMethod 1 - Variance-based priority:")
    print(f"  10 × ({f3_var}% / {max_var}%) = {priority_variance:.2f}")
    
    # Method 2: Based on maximum loading
    coat2_loading = 0.5938  # From FA output
    max_loading = 1.0017  # Coat 1 Cracking on Factor 1
    priority_loading = 10 * (coat2_loading / max_loading)
    print(f"\nMethod 2 - Loading-based priority:")
    print(f"  10 × ({coat2_loading:.4f} / {max_loading:.4f}) = {priority_loading:.2f}")
    
    # Method 3: Combined (typical approach)
    # Normalize variance contribution and loading
    variance_norm = f3_var / max_var
    loading_norm = coat2_loading / max_loading
    combined_priority = 10 * ((variance_norm + loading_norm) / 2)
    
    print(f"\nMethod 3 - Combined priority:")
    print(f"  Variance normalized: {variance_norm:.4f}")
    print(f"  Loading normalized: {loading_norm:.4f}")
    print(f"  Average: {(variance_norm + loading_norm)/2:.4f}")
    print(f"  10 × average = {combined_priority:.2f}")
    print(f"  Rounded to integer: {round(combined_priority)}")
    
    print("\n" + "-"*70)
    print("CELL SCORE CALCULATION")
    print("-"*70)
    
    priority_score = round(combined_priority)
    mitigation_score = 6
    cell_score = priority_score * mitigation_score
    
    print(f"\nStructural Instability × Mitigation:")
    print(f"  NSC Priority: {priority_score}")
    print(f"  Mitigation Score: {mitigation_score} (Secretary of Interior Standards)")
    print(f"  Cell Score: {priority_score} × {mitigation_score} = {cell_score}")
    print(f"\nInterpretation: This intervention addresses a moderately high-priority")
    print(f"  condition using a preservation-appropriate approach.")

if __name__ == "__main__":
    data_path = 'synthetic_adobe_data.csv'
    
    print("\n" + "="*70)
    print("FOUN MANUSCRIPT VERIFICATION & SUPPLEMENTAL ANALYSES")
    print("="*70)
    
    # Load data
    df = load_and_preprocess_data(data_path)
    
    # 1. Verify Factor Analysis communalities
    fa_results = verify_factor_analysis_communalities(df)
    
    # 2. Run supplemental RF with geometric features only
    rf_geom_results = run_supplemental_rf_geometric_only(df)
    
    # 3. Calculate intervention priority example
    calculate_intervention_priority_example(fa_results, rf_geom_results)
    
    # Save results
    results = {
        'factor_analysis_verification': fa_results,
        'supplemental_rf_geometric_only': rf_geom_results
    }
    
    output_file = 'journalPaper/verification_and_supplemental.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*70)
    print(f"✓ Results saved to: {output_file}")
    print("="*70)
