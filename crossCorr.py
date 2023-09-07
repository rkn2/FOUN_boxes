# pip install pandas-profiling
# pip install pandas
# pip install stats
# pip install matplotlib

import scipy.stats as stats  # Import the scipy.stats library
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas_profiling import ProfileReport

file_path = '2023_9_5_output_blocks_cont4.csv'
# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

columns_to_drop = list(range(0, 10))  # This creates a list of column indices from 1 to 9

# Use the .drop() method to remove the specified columns
df = df.drop(columns=df.columns[columns_to_drop])

# Use dropna() to remove rows with missing values
# df_cleaned = df.dropna() # takes away too many

columns_to_drop = ['Coat WGT SCR', 'Coat 4 WGT SCR', 'Wall nrm scr', 'Wall wgt scr', 'Total scr', 'Wall rank']

# Use the .drop() method to remove the specified columns
df = df.drop(columns=columns_to_drop)

# do reporting if desired
#prof = ProfileReport(df)
#prof.to_file(output_file='output_raw.html')

correlation_matrix = df.corr()

# Define a significance level (e.g., 0.05, which is common)
alpha = 0.05

# Create an empty list to store the significant correlations
significant_correlations = []

# Loop through the rows and columns of the correlation matrix
for i in range(len(correlation_matrix.columns)):
    for j in range(i + 1, len(correlation_matrix.columns)):
        column1 = df.iloc[:, i]
        column2 = df.iloc[:, j]

        # Check for missing values in the pair of columns
        if not column1.hasnans and not column2.hasnans:
            correlation_coefficient = correlation_matrix.iloc[i, j]
            p_value = stats.pearsonr(column1, column2)[1]  # Calculate the p-value
            if p_value < alpha:
                significant_correlations.append((i, j, correlation_coefficient, p_value))

# Print the significant correlations
for i, j, coefficient, p_value in significant_correlations:
    col1_name = correlation_matrix.columns[i]
    col2_name = correlation_matrix.columns[j]
    print(f"Variables {col1_name} and {col2_name}: Correlation = {coefficient}, p-value = {p_value}")


# to see what values in my cross corr are above 0.25 (based on the output of p testing)
# Define the threshold for correlation
threshold = 0.25

# Loop through the column names in the correlation matrix
column_names = list(correlation_matrix.keys())
for i in range(len(column_names)):
    for j in range(i + 1, len(column_names)):
        column1_name = column_names[i]
        column2_name = column_names[j]
        correlation_coefficient = correlation_matrix[column1_name][j]
        if abs(correlation_coefficient) > threshold:
            print("Variables '{}' and '{}': Correlation = {}".format(column1_name, column2_name, correlation_coefficient))

# ^^ something seems off about this since its not pulling all the right numbers

# Create a heatmap with correlation coefficients
plt.figure(figsize=(20,16))
sns.set(font_scale=1)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5, fmt=".2f")

plt.title('Cross-Correlation Heatmap with Correlation Coefficients')
plt.savefig('heatmap.png')  # Save the figure to a file