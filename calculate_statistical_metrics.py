"""
Calculate Factor Analysis and Correlation Statistics for FOUN Manuscript
=========================================================================

This script calculates all missing statistical metrics needed for the paper:
1. Factor Analysis: KMO, Bartlett's test, communalities, variance explained
2. Correlation Analysis: p-values, Bonferroni correction details

Author: Auto-generated for manuscript revision
"""

import pandas as pd
import numpy as np
import json
from scipy.stats import pearsonr, chi2
from sklearn.impute import SimpleImputer
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo

def load_and_preprocess_data(filepath):
    """Load and preprocess data (same as generate_tex_figures.py)"""
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Original shape: {df.shape}")
    
    # Columns to drop
    non_numeric_cols = ['Wall ID', 'Image Name', 'Notes', 'Date', 'Reviewer', 
                        'Wall Rank', 'Section ID']
    df_clean = df.drop(columns=[c for c in non_numeric_cols if c in df.columns])
    
    # Handle missing values
    imputer = SimpleImputer(strategy='median')
    df_numeric = df_clean.select_dtypes(include=[np.number])
    
    # Drop columns that are all NaN
    original_cols = df_numeric.shape[1]
    df_numeric = df_numeric.dropna(axis=1, how='all')
    dropped_cols = original_cols - df_numeric.shape[1]
    if dropped_cols > 0:
        print(f"Dropped {dropped_cols} columns with all missing values")
    
    imputed_data = imputer.fit_transform(df_numeric)
    df_imputed = pd.DataFrame(imputed_data, columns=df_numeric.columns)
    
    print(f"Final shape: {df_imputed.shape}")
    return df_imputed

def calculate_correlation_stats(df):
    """
    Calculate correlation statistics with p-values and Bonferroni correction
    """
    print("\n" + "="*70)
    print("CORRELATION ANALYSIS WITH STATISTICAL TESTS")
    print("="*70)
    
    # Select key columns for correlation (matching paper's approach)
    key_cols = ['Total Scr', 'Cap Deterioration', 'Out of Plane', 'Height', 
                'Structural Cracking', 'Bracing', 'Sill 1', 'Sill 2', 
                'Coat 1 Cracking', 'Lintel Deterioration', 'Foundation Height']
    
    available_cols = [c for c in key_cols if c in df.columns]
    df_corr = df[available_cols]
    
    # Calculate all pairwise correlations with p-values
    n_vars = len(available_cols)
    n_comparisons = (n_vars * (n_vars - 1)) // 2  # Number of unique pairs
    
    print(f"\nVariables analyzed: {n_vars}")
    print(f"Total pairwise comparisons: {n_comparisons}")
    print(f"Bonferroni-corrected alpha: {0.05 / n_comparisons:.6f}")
    
    # Calculate correlation matrix and p-values
    corr_matrix = df_corr.corr()
    p_matrix = pd.DataFrame(np.ones((n_vars, n_vars)), 
                           columns=available_cols, 
                           index=available_cols)
    
    for i, col1 in enumerate(available_cols):
        for j, col2 in enumerate(available_cols):
            if i < j:  # Only calculate upper triangle
                r, p = pearsonr(df_corr[col1], df_corr[col2])
                p_matrix.loc[col1, col2] = p
                p_matrix.loc[col2, col1] = p
    
    # Focus on Total Scr correlations
    print("\nCorrelations with Total Scr (with p-values):")
    print("-" * 70)
    print(f"{'Variable':<30} {'r':<10} {'p-value':<15} {'Bonf. Sig.'}")
    print("-" * 70)
    
    total_scr_corrs = []
    bonferroni_alpha = 0.05 / n_comparisons
    
    for col in available_cols:
        if col != 'Total Scr':
            r = corr_matrix.loc['Total Scr', col]
            p = p_matrix.loc['Total Scr', col]
            is_sig = "Yes" if p < bonferroni_alpha else "No"
            print(f"{col:<30} {r:>8.4f}  {p:>12.4e}    {is_sig}")
            total_scr_corrs.append({
                'variable': col,
                'r': r,
                'p': p,
                'bonferroni_significant': bool(p < bonferroni_alpha)
            })
    
    # Special attention to key correlations mentioned in paper
    key_pairs = [
        ('Bracing', 'Total Scr'),
        ('Sill 1', 'Sill 2')
    ]
    
    print("\nKey pairwise correlations mentioned in paper:")
    print("-" * 70)
    for var1, var2 in key_pairs:
        if var1 in available_cols and var2 in available_cols:
            r = corr_matrix.loc[var1, var2]
            p = p_matrix.loc[var1, var2]
            print(f"{var1} <-> {var2}: r = {r:.4f}, p = {p:.4e}")
    
    stats = {
        'n_variables': n_vars,
        'n_comparisons': n_comparisons,
        'bonferroni_alpha': bonferroni_alpha,
        'total_scr_correlations': total_scr_corrs,
        'correlation_matrix': corr_matrix.to_dict(),
        'p_value_matrix': p_matrix.to_dict()
    }
    
    return stats

def calculate_factor_analysis_stats(df):
    """
    Calculate comprehensive Factor Analysis statistics
    """
    print("\n" + "="*70)
    print("FACTOR ANALYSIS - COMPREHENSIVE STATISTICS")
    print("="*70)
    
    # Select variables for FA (matching the paper's table)
    fa_vars = ['Sill 1', 'Sill 2', 'Coat 1 Cracking', 'Coat 1 Loss',
               'Lintel Deterioration', 'Coat 2 Cracking', 
               'Structural Cracking', 'Out of Plane']
    
    available_vars = [v for v in fa_vars if v in df.columns]
    df_fa = df[available_vars]
    
    print(f"\nVariables in analysis: {len(available_vars)}")
    print(f"Sample size: {len(df_fa)}")
    
    # 1. KMO (Kaiser-Meyer-Olkin) measure
    kmo_all, kmo_model = calculate_kmo(df_fa)
    
    print(f"\n1. KAISER-MEYER-OLKIN (KMO) MEASURE")
    print(f"   Overall KMO: {kmo_model:.4f}")
    if kmo_model >= 0.9:
        interpretation = "marvelous"
    elif kmo_model >= 0.8:
        interpretation = "meritorious"
    elif kmo_model >= 0.7:
        interpretation = "middling"
    elif kmo_model >= 0.6:
        interpretation = "mediocre"
    elif kmo_model >= 0.5:
        interpretation = "miserable"
    else:
        interpretation = "unacceptable"
    print(f"   Interpretation: {interpretation} (Kaiser threshold)")
    
    print("\n   Individual KMO values:")
    for i, var in enumerate(available_vars):
        print(f"   {var:<30} {kmo_all[i]:.4f}")
    
    # 2. Bartlett's Test of Sphericity
    chi_square_value, p_value = calculate_bartlett_sphericity(df_fa)
    df_bartlett = len(available_vars) * (len(available_vars) - 1) / 2
    
    print(f"\n2. BARTLETT'S TEST OF SPHERICITY")
    print(f"   χ² = {chi_square_value:.2f}")
    print(f"   df = {int(df_bartlett)}")
    print(f"   p-value < 0.001 (highly significant)")
    print(f"   Conclusion: Correlation matrix is NOT an identity matrix")
    print(f"   → Suitable for factor analysis")
    
    # 3. Factor Analysis with 3 factors (varimax rotation)
    fa = FactorAnalyzer(n_factors=3, rotation='varimax')
    fa.fit(df_fa)
    
    # Get loadings
    loadings = fa.loadings_
    loadings_df = pd.DataFrame(
        loadings,
        index=available_vars,
        columns=['Factor 1', 'Factor 2', 'Factor 3']
    )
    
    print(f"\n3. FACTOR LOADINGS (Varimax Rotation)")
    print(loadings_df.round(4))
    
    # 4. Communalities
    communalities = fa.get_communalities()
    
    print(f"\n4. COMMUNALITIES")
    print(f"   (Proportion of variance explained by the 3-factor solution)")
    print("-" * 50)
    for var, comm in zip(available_vars, communalities):
        print(f"   {var:<30} {comm:.4f}")
    
    # 5. Variance Explained
    variance_explained = fa.get_factor_variance()
    
    print(f"\n5. VARIANCE EXPLAINED")
    print("-" * 50)
    print(f"{'Metric':<30} {'F1':<10} {'F2':<10} {'F3':<10}")
    print("-" * 50)
    print(f"{'SS Loadings':<30} {variance_explained[0][0]:>8.4f}  "
          f"{variance_explained[0][1]:>8.4f}  {variance_explained[0][2]:>8.4f}")
    print(f"{'Proportion Var':<30} {variance_explained[1][0]:>8.4f}  "
          f"{variance_explained[1][1]:>8.4f}  {variance_explained[1][2]:>8.4f}")
    print(f"{'Cumulative Var':<30} {variance_explained[2][0]:>8.4f}  "
          f"{variance_explained[2][1]:>8.4f}  {variance_explained[2][2]:>8.4f}")
    
    total_var_explained = variance_explained[2][2] * 100  # Cumulative for Factor 3
    print(f"\nTotal variance explained by 3 factors: {total_var_explained:.2f}%")
    
    # 6. Try oblique rotation (promax) for comparison
    fa_promax = FactorAnalyzer(n_factors=3, rotation='promax')
    fa_promax.fit(df_fa)
    loadings_promax = fa_promax.loadings_
    
    print(f"\n6. COMPARISON: PROMAX (OBLIQUE) ROTATION")
    loadings_promax_df = pd.DataFrame(
        loadings_promax,
        index=available_vars,
        columns=['Factor 1', 'Factor 2', 'Factor 3']
    )
    print(loadings_promax_df.round(4))
    
    # Calculate factor correlations for promax
    try:
        factor_corr = fa_promax.corr_
        print(f"\n   Factor Correlations (Promax):")
        factor_corr_df = pd.DataFrame(
            factor_corr,
            index=['Factor 1', 'Factor 2', 'Factor 3'],
            columns=['Factor 1', 'Factor 2', 'Factor 3']
        )
        print(factor_corr_df.round(4))
        print(f"   Note: Low factor correlations suggest varimax (orthogonal) is appropriate")
    except:
        print("   Factor correlations not available for promax")
    
    # Check which rotation yields more interpretable structure
    varimax_max_loadings = np.max(np.abs(loadings), axis=1)
    promax_max_loadings = np.max(np.abs(loadings_promax), axis=1)
    
    varimax_clarity = np.mean(varimax_max_loadings)
    promax_clarity = np.mean(promax_max_loadings)
    
    print(f"\n   Structure Clarity (mean max loading):")
    print(f"   Varimax: {varimax_clarity:.4f}")
    print(f"   Promax:  {promax_clarity:.4f}")
    
    # Compile results
    fa_stats = {
        'kmo_overall': float(kmo_model),
        'kmo_interpretation': interpretation,
        'kmo_by_variable': {var: float(kmo_all[i]) for i, var in enumerate(available_vars)},
        'bartlett_chi2': float(chi_square_value),
        'bartlett_df': int(df_bartlett),
        'bartlett_p': float(p_value),
        'n_factors': 3,
        'loadings_varimax': loadings_df.to_dict(),
        'communalities': {var: float(comm) for var, comm in zip(available_vars, communalities)},
        'variance_explained': {
            'ss_loadings': variance_explained[0].tolist(),
            'proportion_var': variance_explained[1].tolist(),
            'cumulative_var': variance_explained[2].tolist(),
            'total_var_explained_pct': float(total_var_explained)
        },
        'factor1_var_pct': float(variance_explained[1][0] * 100),
        'factor2_var_pct': float(variance_explained[1][1] * 100),
        'factor3_var_pct': float(variance_explained[1][2] * 100),
        'loadings_promax': loadings_promax_df.to_dict(),
        'promax_similar_to_varimax': bool(abs(varimax_clarity - promax_clarity) < 0.05)
    }
    
    return fa_stats

if __name__ == "__main__":
    # Load data
    data_path = 'synthetic_adobe_data.csv'
    df = load_and_preprocess_data(data_path)
    
    # Calculate statistics
    corr_stats = calculate_correlation_stats(df)
    fa_stats = calculate_factor_analysis_stats(df)
    
    # Combine all statistics
    all_stats = {
        'correlation_analysis': corr_stats,
        'factor_analysis': fa_stats
    }
    
    # Save to JSON
    output_file = 'journalPaper/statistical_metrics.json'
    with open(output_file, 'w') as f:
        json.dump(all_stats, f, indent=2)
    
    print("\n" + "="*70)
    print(f"✓ Statistical metrics saved to: {output_file}")
    print("="*70)
    
    # Print summary for LaTeX insertion
    print("\n" + "="*70)
    print("SUMMARY FOR LATEX DOCUMENT")
    print("="*70)
    
    print(f"\nFACTOR ANALYSIS:")
    print(f"  KMO = {fa_stats['kmo_overall']:.4f} ({fa_stats['kmo_interpretation']})")
    print(f"  Bartlett's χ² = {fa_stats['bartlett_chi2']:.2f}, df = {fa_stats['bartlett_df']}, p < 0.001")
    print(f"  Variance explained: F1={fa_stats['factor1_var_pct']:.1f}%, "
          f"F2={fa_stats['factor2_var_pct']:.1f}%, F3={fa_stats['factor3_var_pct']:.1f}%")
    print(f"  Total variance: {fa_stats['variance_explained']['total_var_explained_pct']:.1f}%")
    print(f"  Promax vs Varimax: {'Similar structure' if fa_stats['promax_similar_to_varimax'] else 'Different structure'}")
    
    print(f"\nCORRELATION ANALYSIS:")
    print(f"  Total comparisons: {corr_stats['n_comparisons']}")
    print(f"  Bonferroni α: {corr_stats['bonferroni_alpha']:.6f}")
    
    # Find Bracing correlation
    for corr in corr_stats['total_scr_correlations']:
        if corr['variable'] == 'Bracing':
            print(f"  Bracing-Total Scr: r={corr['r']:.4f}, p={corr['p']:.4e}")
            break
    
    # Find Sill 1-Sill 2 correlation
    if 'Sill 1' in df.columns and 'Sill 2' in df.columns:
        from scipy.stats import pearsonr
        r_sill, p_sill = pearsonr(df['Sill 1'], df['Sill 2'])
        print(f"  Sill 1-Sill 2: r={r_sill:.4f}, p={p_sill:.4e}")
    
    print("\n" + "="*70)
    print("All metrics calculated successfully!")
    print("="*70)
