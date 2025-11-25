# Auto-Populated Model Metrics - FOUN Manuscript

## Summary
Successfully ran `generate_tex_figures.py` and automatically populated the following metrics into `main_new.tex`:

---

## Random Forest Performance Metrics (Section 4.2)

**Auto-Populated Values:**
- **Sample size**: n=67 wall sections, 28 features
- **Cross-Validation R²**: 0.52 (±0.12)
- **Cross Validation RMSE**: 8.21  
- **Cross-Validation MAE**: 6.76
- **Out-of-Bag R²**: 0.60
- **Training R²**: 0.95 (indicates overfitting as expected)

---

## Feature Importance Rankings (Section 5.1.3)

**Top 10 Features with Mean Decrease in Impurity and Permutation Importance:**

| Rank | Feature | MDI | Perm ± SE |
|------|---------|------|-----------|
| 1 | Coat 2 Cracking | 0.2073 | 0.2507 ± 0.0416 |
| 2 | Structural Cracking | 0.1758 | 0.2263 ± 0.0460 |
| 3 | Out of Plane | 0.1145 | 0.1362 ± 0.0204 |
| 4 | Cap Deterioration | 0.0666 | 0.0504 ± 0.0070 |
| 5 | **Height** | **0.0549** | **0.0320 ± 0.0056** |
| 6 | Foundation Displacement 1 | 0.0426 | 0.0292 ± 0.0072 |
| 7 | Point Cloud Mean | 0.0392 | 0.0263 ± 0.0046 |
| 8 | Sill 1 | 0.0362 | 0.0236 ± 0.0055 |
| 9 | Lintel Deterioration | 0.0351 | 0.0251 ± 0.0053 |
| 10 | Coat 1 Cracking | 0.0287 | 0.0187 ± 0.0035 |

**Key Geometric Factors (not in top 10):**
- **Foundation Height** (rank ~13): MDI = 0.0239, Perm = 0.0132 ± 0.0029

**Treatment Variables (very low importance):**
- Treatment: 0.0031
- Bracing: 0.0011
- Bracing Score: 0.0044

---

## Key Interpretations Updated in Manuscript

### What Changed from Original Expectations:
**Original hypothesis**: Geometric factors (Height, Foundation Height) would be dominant predictors. 

**Actual findings**: Visible damage indicators (Coat 2 Cracking, Structural Cracking, Out of Plane) are top predictors; geometric factors show moderate importance.

### Why This Makes Sense:
1. **Circular dependency**: Total Score aggregates multiple damage types, so features representing severe damage naturally predict it strongly
2. **Geometric factors still meaningful**: Their persistent moderate importance *after* accounting for existing damage suggests intrinsic vulnerability
3. **Treatment variables low**: Reflects selection bias (treated walls were already degraded) not ineffectiveness

### Updated Narrative in Paper:
- Results section now accurately reports damage indicators as top 3 predictors
- Structural engineering discussion repositioned to explain *why* geometric factors matter for **preventive** prioritization
- Conclusions emphasize using geometric risk factors to identify walls requiring early intervention *before* severe damage
- Added explicit discussion of circular dependency problem for practical application

---

## Files Generated:
1. **journalPaper/Images/correlation_heatmap.png** - Updated correlation matrix figure
2. **journalPaper/Images/feature_importance.png** - Random Forest feature importance plot matching actual data
3. **journalPaper/model_metrics.json** - Complete metrics file with all values

---

## Remaining Placeholders in LaTeX

The following `\hl{Becca: ...}` items still require your manual input (data we don't have):

### Factor Analysis:
- KMO value and interpretation
- Bartlett's χ² and df
- Variance explained by each factor (%, %, %)
- Promax rotation results (if run)
- Communality values for 8 variables
- Sill 1 vs Sill 2 correlation

### Correlation Analysis:
- Exact number of pairwise comparisons for Bonferroni correction
- P-value for bracing correlation

### Field Data:
- Survey team size, dates, inter-rater reliability scores
- Treatment application dates and counts per type
- Wall dimension statistics (mean height, range, h/t ratios)
- Orientation 2 directional exposure investigation
- Splash-back measurements (if available)
- Compressive strength test data for FOUN adobe
- Annual precipitation and freeze-thaw cycles at FOUN

### Methodology Decisions:
- Sensitivity analysis for intervention matrix weighting
- Factor 3 variance contribution
- NSP repeat survey plans
- NPS pilot validation study interest
- Point cloud raw data availability
- Cost estimate availability from NPS records

---

## Next Steps:
1. Search for remaining `\hl{` markers in the .tex file
2. Run Factor Analysis code (if separate script) to get KMO, Bartlett's, communalities, variance explained
3. Gather field metadata (survey details, wall dimensions, treatment records)
4. Compile the LaTeX to verify all figures render correctly
5. Review the updated narrative to ensure it aligns with your research story

The manuscript now presents **actual** results rather than expected results, with honest interpretation of what the findings mean for preservation practice!
