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
                        significant_relationships.append((col1, col2, corr, p_value))

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
    df_significant.to_csv(date + 'significant_relationships_dropped.csv', index=False)

if __name__ == "__main__":
    main()
