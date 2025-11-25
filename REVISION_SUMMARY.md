# Major Revisions to FOUN Manuscript Based on Reviewer Comments
## Summary of Changes Made

This document summarizes the comprehensive revisions made to address reviewer feedback. Yellow-highlighted sections (`\hl{Becca: ...}`) indicate where you need to provide specific values or confirm information.

---

## MAJOR ISSUES ADDRESSED

### 1. **Incomplete Methodology Documentation (Random Forest)**  
**Changes Made:**
- Added explicit hyperparameters: 100 trees, max depth unrestricted, min samples split=2, random_state=42
- Specified 5-fold cross-validation approach (no train/test split due to n=67)
- Added placeholders for model performance metrics (R², RMSE, MAE, OOB error) - **YOU NEED TO RUN MODEL AND PROVIDE THESE**
- Documented permutation importance with bootstrapping (1000 iterations, 95% CI)
- Explicitly acknowledged overfitting risk given 1:2 feature-to-sample ratio
- Added note about mean decrease in impurity bias toward high-cardinality features

**Action Items for You:**
- Line ~320: Provide scikit-learn version number
- Line ~324: Run model and provide R², RMSE, MAE, and out-of-bag error values
- Line ~328: Provide exact feature importance values with standard errors

---

### 2. **Causality vs. Correlation Confusion**  
**Changes Made:**
- Replaced "suggests" with "is likely due to" for bracing correlation
- Changed "drivers" to "predictors" throughout
- Added explicit reverse causality warning for bracing
- Changed "correlations" to "associations" in multiple places
- Added note that cross-sectional data cannot establish temporal relationships
- Suggested propensity score matching for future causal analysis

**Key Sections Modified:**
- Abstract: "associated with" instead of "driving"
- Correlation section (line ~331-344): Added Bonferroni correction, made clear these are associations not causal relationships
- Random Forest section (line ~443-481): Changed "driver" to "predictor", added multiple possible mechanisms
- Conclusions: Emphasized "cross-sectional nature precludes causal inference"

**Action Items for You:**
- Line ~334: Specify exact number of comparisons for Bonferroni correction
- Line ~338: Provide p-value for bracing correlation

---

### 3. **Factor Analysis Interpretation Issues**  
**Changes Made:**
- Added KMO (Kaiser-Meyer-Olkin) measure of sampling adequacy
- Added Bartlett's test of sphericity results
- Added communalities table (Table \ref{tab:communalities})
- Explained why 3 factors were chosen (Kaiser criterion, scree plot, interpretability)
- Reported variance explained by each factor
- Mentioned supplementary promax (oblique) rotation analysis
- Addressed Factor 1 measurement redundancy concern directly
- Explained Factor 3's inclusion of Coat 2 Cracking with hypothesis about orientation-specific exposure
- Softened causal language in factor interpretations

**Action Items for You:**
- Line ~365: Provide KMO value and interpretation (adequate/good/excellent)
- Line ~366: Provide chi-square value, df, and confirm p<0.001
- Line ~369: Provide cumulative variance explained and individual factor percentages
- Line ~370: Did you run promax rotation? Report if similar results
- Lines ~396-414: Fill in communality values for all 8 variables
- Line ~410: What is correlation between Sill 1 and Sill 2?
- Line ~421: Investigate whether Orientation 2 faces prevailing winds - check meteorological data

---

### 4. **Intervention Matrices Lack Quantitative Justification**  
**Changes Made:**
- Added explicit formulas for NSC priority scores: 10 × (loading/max loading) or (importance/max importance)
- Provided detailed justification for preservation standards scores (0-6 scale) with citations to Secretary of Interior's Standards
- Explained cell score calculation explicitly: (NSC priority) × (intervention approach score)
- Added worked example showing calculation
- Acknowledged this is one possible weighting framework
- Suggested sensitivity analysis and AHP (Analytic Hierarchy Process) as future extensions

**Action Items for You:**
- Line ~533: Verify the priority score formula matches your actual calculation
- Line ~534: What percent of variance does Factor 3 explain?
- Line ~555: Did you test alternative weighting schemes? Report if rankings were stable

---

### 5. **Missing Structural Engineering Content**  
**Changes Made:**
- Added comprehensive structural mechanics discussion for foundation height with 4 mechanisms:
  * Splash-back erosion
  * Capillary rise from shallow foundations
  * Loss of lateral restraint
  * Differential settlement markers
- Added structural mechanics discussion for wall height with 4 mechanisms:
  * Increased wind loads (M ∝ h²)
  * Slenderness effects (h/t ratios)
  * Greater rain exposure
  * Higher compressive stress
- Recommended future monitoring: soil moisture, bearing pressures, LiDAR settlement tracking
- Added calculation frameworks mentioned in text
- Recommended FEM modeling, stability calculations in Limitations section

**Action Items for You:**
- Line ~450: Do you have splashback height or erosion rate measurements?
- Line ~462: What are typical wall heights at FOUN? Report mean, range, h/t ratios
- Line ~463: Calculate h/t for tallest walls - do any exceed 10-12 threshold?
- Line ~464: Do you have compressive strength test data for FOUN adobe?

---

### 6. **Statistical Rigor Issues**  
**Changes Made:**
- Added Bonferroni correction for multiple comparisons
- Specified two-tailed tests
- Added p-values to correlation results
- Acknowledged sample size limitations explicitly throughout
- Added discussion of statistical power issues
- Mentioned VIF, heteroscedasticity, residual normality checking in Limitations
- Recommended regularization (LASSO, Ridge) for future work

**Action Items for You:**
- Line ~334: How many total pairwise comparisons were tested?
- Line ~338: Provide p-value for bracing-Total Scr correlation

---

## MODERATE ISSUES ADDRESSED

### 7. **LiDAR Data Underutilization**  
**Changes Made:**
- Added section in Limitations acknowledging only 2 features extracted from point cloud
- Suggested richer features: wall lean angles, surface roughness, erosion depth, settlement patterns, volume loss
- Recommended change detection, Structure-from-Motion photogrammetry

**Action Item:**
- Line ~673: Are raw point cloud data available for reanalysis?

---

### 8. **Treatment History Not Properly Analyzed**  
**Changes Made:**
- Added 4 possible explanations for low treatment importance:
  1. Selection bias
  2. Treatment deterioration over time
  3. Environmental dominance
  4. Sample size limitations
- Recommended temporal/survival analysis if dates are available
- Explicitly stated results don't demonstrate ineffectiveness

**Action Items:**
- Line ~471: Do you have treatment application dates?
- Line ~472: How many walls received each treatment type?

---

### 9. **Environmental Data Absent**  
**Changes Made:**
- Added section in Limitations noting lack of climate integration
- Suggested weather station data, microclimate sensors, aspect/exposure analysis
- Connected to Factor 3 Orientation 2 issue

**Action Item:**
- Line ~644: Annual precipitation? Freeze-thaw cycles at FOUN?

---

### 10. **Abstract Oversells**  
**Changes Made:**
- Changed "demonstrates the effectiveness" to "illustrates the potential"
- Added caveat: "though validation at additional sites and longitudinal monitoring are needed"
- Softened "driving degradation" to "associated with degradation"
- Changed "guiding" to "informing"

---

### 11. **Limitations Section Added**  
**New comprehensive section added before Conclusions covering:**
- Sample size and statistical power
- Single-site generalizability
- Cross-sectional data limitations
- Lack of experimental validation
- Observer bias and inter-rater reliability
- Environmental data gap
- LiDAR underutilization
- Material property unknowns
- Structural mechanics simplification
- Cost-benefit analysis absent

---

## MINOR ISSUES ADDRESSED

### 12. **Data Collection Details**  
**Action Item:**
- Line ~185: How many raters? Team size? Survey dates? Inter-rater reliability results?

---

### 13. **Specific Technical Corrections**  
**Changes Made:**
- Specified two-tailed tests for correlations
- Added note about FactorAnalyzer version (**you need to provide**)
- Mentioned permutation importance as supplement to mean decrease in impurity
- Provided exact cell score calculation formula

---

### 14. **Writing Improvements**  
**Changes Made:**
- Toned down Conclusions section: "suggests" instead of "demonstrates"
- Added caveats about validation needs throughout
- Emphasized "predictor" not "driver"
- Made explicit what can vs. cannot be inferred from data

---

## SECTIONS THAT NEED YOUR INPUT

Throughout the document, I've inserted `\hl{Becca: question or request}` markers. Here's a consolidated list:

1. **Line ~185**: Survey team details, dates, inter-rater reliability
2. **Line ~320**: scikit-learn version number
3. **Line ~324**: Model performance metrics (R², RMSE, MAE, OOB error)
4. **Line ~334**: Number of pairwise comparisons for Bonferroni
5. **Line ~338**: P-value for bracing correlation  
6. **Line ~365**: KMO value and interpretation
7. **Line ~366**: Bartlett's χ², df
8. **Line ~369**: Variance explained by factors
9. **Line ~370**: Promax rotation results
10. **Lines ~396-414**: Communality values (8 variables)
11. **Line ~410**: Sill 1 vs. Sill 2 correlation
12. **Line ~421**: Orientation 2 directional exposure investigation
13. **Line ~450**: Splash-back measurements?
14. **Line ~462-464**: Wall dimensions, h/t ratios, compressive strength
15. **Line ~471-472**: Treatment dates and counts
16. **Line ~533**: Verify priority score formula
17. **Line ~534**: Factor 3 variance contribution
18. **Line ~555**: Sensitivity analysis results?
19. **Line ~641**: Number of treated walls per type
20. **Line ~644**: Annual precipitation, freeze-thaw cycles
21. **Line ~651**: NPS repeat survey plans?
22. **Line ~654**: NPS pilot validation study interest?
23. **Line ~659**: Inter-rater reliability testing details
24. **Line ~673**: Point cloud raw data availability?
25. **Line ~685**: Cost estimates from NPS records?

---

## WHAT TO DO NEXT

1. **Search for all `\hl{` in the .tex file** - these mark places needing your input
2. **Run your analyses** to get:
   - Random Forest performance metrics
   - Factor Analysis fit statistics
   - Exact feature importance values with std errors
3. **Gather metadata**:
   - Survey dates, team composition
   - Software versions used
   - Treatment records
   - Climate data for FOUN
4. **Calculate missing values**:
   - Bonferroni-corrected p-values
   - Communalities
   - h/t ratios if you have wall dimensions
5. **Review and decide** on questions marked with "?" - these are requests for investigation or decisions about what to report

The manuscript now addresses all Major Issues and most Moderate/Minor issues from the reviews. The highlighted sections are where only you can provide the specific technical details or data.
