import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def read_and_clean_data(file_path, drop_columns=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    if drop_columns is not None:
        # Drop specified columns by index
        df = df.drop(columns=df.columns[drop_columns])

    # Remove rows with missing values
    df = df.dropna()

    return df

def calculate_correlations(df, alpha=0.05):
    # Create a dictionary to map existing variable names to new names
    variable_name_mapping = {
        "treatment_1": "Remove to blow top of foundation",
        "treatment_2": "Pushing adobe wall into plumb using (trench box, hydraulic jacks, and wood panel)",
        "treatment_3": "Rebuilding",
        "treatment_4": "Apply a fresh Rhoplex amended shelter coat annually",
        "treatment_5": "Plastering",
        "treatment_6": "Replace amended capping",
        "treatment_7": "In all rooms, correct differential fill, especially in corners",
        "treatment_8": "Repoint foundation stones with lime or earthen mortar (whichever material was used originally)",
        "treatment_9": "Collapse was cleaned up but remains open at present",
        "treatment_10": "Infill the wide crack with new amended bricks and tie or key into the wall ends on either side of the opening every third course (use of headers and stretchers) (two full bricks end-to-end and overlapping in the middle)",
        "treatment_11": "Stitching of new bricks on the interior side of the crack",
        "treatment_12": "Filled dry packed mud mortar",
        "treatment_13": "Brick cobbling",
        "treatment_14": "Stitched crack should be monitored",
        "treatment_15": "Rebuilt section be trimmed with a saw to make it even with the rest of the wall and then replastered",
        "treatment_16": "Cracks were filled with amended mortar with brick cobbling",
        "treatment_17": "Tied in to the existing walls, though not consistently at every third course",
        "treatment_18": "Cap should be monitored",
        "treatment_19": "Base coat for mud cap",
        "treatment_20": "Lintel being removed",
        "1960_treat_1": "Capping",
        "1960_treat_2": "Sprayed with DOW corning 772 diluted in water at a ratio of 1 to 9",
        "1960_treat_3": "Add Horizontal Support",
        "1960_treat_4": "Add Vertical Support",
        "1960_treat_5": "Rebuilt",
        "1960_treat_6": "Stabilizing fireplace and chimney by replacing missing bricks",
        "1960_treat_7": "Rebuilt hearth",
        "1960_treat_8": "Crack grouted with soil-cement mortar",
        "1960_treat_9": "Rebuilt missing foundation",
        "1960_treat_10": "Rebuilt flue",
        "1960_treat_11": "Concrete sill",
        "1960_treat_12": "Add support in window",
        "1960_treat_13": "Rebuilt window",
        "1960_treat_14": "Rebuilt up of the lintel and bolted to original one",
        "1960_treat_15": "Steel bolt with washer at both ends in window",
        "1960_treat_16": "Wall jack into plumb",
        "1960_treat_17": "Replace lintel",
        "1960_treat_18": "Reinforced by another layer of mortar",
        "1960_treat_19": "Bolts",
        "1960_treat_20": "Steel fence placed above the lintel",
        "1960_treat_21": "Rebuilt door jump",
    }
    # Calculate Pearson correlations and p-values
    correlation_matrix = df.corr()
    p_values = np.zeros((len(df.columns), len(df.columns)))

    significant_relationships = []

    for i, col1 in enumerate(df.columns):
        for j, col2 in enumerate(df.columns):
            if i < j:
                if df[col1].isnull().any() or df[col2].isnull().any() or np.isinf(df[col1]).any() or np.isinf(df[col2]).any():
                    p_values[i, j] = np.nan
                else:
                    corr, p_value = pearsonr(df[col1], df[col2])
                    p_values[i, j] = p_value
                    if p_value < alpha:
                        significant_relationships.append((variable_name_mapping.get(col1, col1), variable_name_mapping.get(col2, col2), corr, p_value))

    significant_relationships.sort(key=lambda x: abs(x[2]), reverse=True)

    df_significant = pd.DataFrame(significant_relationships, columns=["Variable 1", "Variable 2", "Correlation", "p-value"])

    return correlation_matrix, p_values, df_significant


def plot_correlation_heatmap(correlation_matrix, p_values, alpha=0.05):
    mask = p_values >= alpha

    plt.figure(figsize=(20, 16))
    sns.set(font_scale=1)
    sns.heatmap(correlation_matrix, annot=False, mask=mask, cmap='coolwarm', linewidths=0.5, fmt=".2f")
    plt.title('Cross-Correlation Heatmap with Correlation Coefficients')
    plt.show()

def main():
    date = '2023_12_8_'
    file_path = date + 'targeted_eval.csv'

    # Define columns to drop by index
    columns_to_drop = list(range(0, 10))

    # Read and clean the data
    df = read_and_clean_data(file_path, drop_columns=columns_to_drop)

    # Calculate correlations and p-values
    correlation_matrix, p_values, df_significant = calculate_correlations(df)

    # Plot the correlation heatmap
    plot_correlation_heatmap(correlation_matrix, p_values)

    # Save significant relationships to a CSV file
    df_significant.to_csv(date + 'significant_relationships.csv', index=False)

if __name__ == "__main__":
    main()
