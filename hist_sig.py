# Create a histogram of significant features
# with treatment
import matplotlib.pyplot as plt
from collections import Counter

# Combine 'Variable 1' and 'Variable 2' into a single column
variable_names = pd.concat([df_significant['Variable 1'], df_significant['Variable 2']])

# Count the frequency of each variable
variable_counts = variable_names.value_counts()

# Count the frequency of each variable
variable_counts = Counter(variable_names)

# Extract the most common N variables and their counts (adjust N as needed)
top_N = 10  # You can change this to show more or fewer variables
most_common_variables = variable_counts.most_common(top_N)

# Separate variable names and their counts
most_common_names, most_common_counts = zip(*most_common_variables)

# Create a bar chart (histogram) for the top N most frequent variables
plt.figure(figsize=(12, 6))
plt.barh(most_common_names, most_common_counts, color='skyblue')
plt.xlabel('Frequency')
plt.ylabel('Variable Names')
plt.title('Frequency Distribution of Top {} Variables'.format(top_N))
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.show()

#without treatment

import matplotlib.pyplot as plt
from collections import Counter
import textwrap

# Filter the DataFrame to exclude rows where the 'p' column is smaller than E-10
df_filtered = df_significant[df_significant['p-value'] >= 1e-10]

# Combine 'Variable 1' and 'Variable 2' into a single column
variable_names = pd.concat([df_filtered['Variable 1'], df_filtered['Variable 2']])

# Count the frequency of each variable
variable_counts = variable_names.value_counts()

# Filter out variables containing the word "treat"
variable_counts_filtered = variable_counts[~variable_counts.index.str.contains('treat', case=False)]

# Extract the most common N variables and their counts (adjust N as needed)
top_N = 10  # You can change this to show more or fewer variables
most_common_variables = variable_counts_filtered.head(top_N)

# Separate variable names and their counts
most_common_names = most_common_variables.index
most_common_counts = most_common_variables.values

# Create a bar chart (histogram) for the top N most frequent variables
plt.figure(figsize=(12, 6))
plt.barh(most_common_names, most_common_counts, color='skyblue')
plt.xlabel('Frequency')
plt.ylabel('Variable Names')
plt.title('Frequency Distribution of Top {} Variables (Excluding "treatment" and p < 1e-10)'.format(top_N))

# Adjust y-axis tick labels to wrap text
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.yticks(range(len(most_common_names)), [textwrap.fill(name, 20) for name in most_common_names])  # Adjust the 20 for desired line length
plt.tight_layout()  # Ensure proper spacing
plt.show()
