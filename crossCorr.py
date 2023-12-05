# pip install pandas-profiling
# pip install pandas
# pip install stats
# pip install matplotlib

import scipy.stats as stats  # Import the scipy.stats library
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas_profiling import ProfileReport

date = '2023_12_5_'
file_path = date+'targeted_eval.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

columns_to_drop = list(range(0, 10))  # This creates a list of column indices from 1 to 9

# Use the .drop() method to remove the specified columns
df = df.drop(columns=df.columns[columns_to_drop])

# Use dropna() to remove rows with missing values
# df_cleaned = df.dropna() # takes away too many

columns_to_drop = ['Coat WGT SCR', 'Coat 4 WGT SCR', 'Wall NRM SCR ', 'Wall WGT SCR', 'Total Scr', 'Wall Rank']
#columns_to_drop = []

# Use the .drop() method to remove the specified columns
#df = df.drop(columns=columns_to_drop)

# Check if each column exists before dropping it
for column in columns_to_drop:
    if column in df.columns:
        df = df.drop(columns=column)

# do reporting if desired
#prof = ProfileReport(df)
#prof.to_file(output_file='output_raw.html')

correlation_matrix = df.corr() #pearson correlation

# Define a significance level (e.g., 0.05, which is common)
alpha = 0.05

from scipy.stats import pearsonr
import numpy as np

# Calculate p-values for Pearson correlation
p_values = np.zeros((len(df.columns), len(df.columns)))

# Define your significance level (alpha)
alpha = 0.05

# Create a list to store the significant relationships
significant_relationships = []

# Iterate through each pair of columns
for i, col1 in enumerate(df.columns):
    for j, col2 in enumerate(df.columns):
        if i < j:  # Consider only the upper triangular part
            # Check for NaNs or Infs in the columns
            if df[col1].isnull().any() or df[col2].isnull().any() or np.isinf(df[col1]).any() or np.isinf(df[col2]).any():
                p_values[i, j] = np.nan  # Set p-value to NaN for this pair
            else:
                corr, p_value = pearsonr(df[col1], df[col2])
                p_values[i, j] = p_value
                if p_value < alpha:
                    significant_relationships.append((col1, col2, corr, p_value))

# Sort the significant relationships by the magnitude of correlation
significant_relationships.sort(key=lambda x: abs(x[2]), reverse=True)

# Create a DataFrame from the significant relationships
df_significant = pd.DataFrame(significant_relationships, columns=["Variable 1", "Variable 2", "Correlation", "p-value"])

# Save the DataFrame to a CSV file
df_significant.to_csv(date+'significant_relationships_dropped.csv', index=False)

# Print the significant relationships in order of magnitude
#for relationship in significant_relationships:
#    col1, col2, corr, p_value = relationship
#    print(f"{col1} - {col2}: Correlation = {corr:.2f}, p-value = {p_value:.4f}")

# Create a mask for statistically significant correlations
mask = p_values >= alpha

# Create a heatmap with correlation coefficients
plt.figure(figsize=(20, 16))
sns.set(font_scale=1)
sns.heatmap(correlation_matrix, annot=False, mask=mask, cmap='coolwarm', linewidths=0.5, fmt=".2f")

plt.title('Cross-Correlation Heatmap with Correlation Coefficients')
plt.savefig(date+'heatmap_dropped.png')  # Save the figure to a file
