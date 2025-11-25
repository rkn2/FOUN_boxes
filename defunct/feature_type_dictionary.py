import pandas as pd

#discrete
# Create a DataFrame from the CSV file
df = pd.read_csv('your_disc_feats.csv', sep='\t')

# Convert the DataFrame to the desired dictionary format
disc_feat = {}
for index, row in df.iterrows():
    feature_name = row['discrete']
    values = {}
    for i in range(1, len(row), 3):
        value = int(row[i])
        color = row[i + 1]
        legend = row[i + 2]
        values[str(value)] = {
            "color": color,
            "legend": legend
        }
    disc_feat[feature_name] = values

# Read the CSV file (replace 'your_file.csv' with the actual path to your CSV file)
df = pd.read_csv('your_cont_file.csv', sep=',', header=None, names=['label', 'colorscale'])

# Initialize an empty dictionary for the continuous features
continuous_feat = {"continuous": {}}

# Loop through the rows of the DataFrame to populate the dictionary
for _, row in df.iterrows():
    feature_name = row['label']
    colorscale = row['colorscale']
    continuous_feat["continuous"][feature_name] = colorscale

#binary
# Read the CSV file (replace 'your_file.csv' with the actual path to your CSV file)
df = pd.read_csv('your_bin_file.csv', sep='\t', header=None, index_col=0)

# Initialize an empty dictionary for the binary features
binary_feat = {"binary": {}}

# Loop through the rows of the DataFrame to populate the dictionary
for index, row in df.iterrows():
    feature_name = index
    values = {}
    for i in range(len(row)):
        values[str(i)] = row[i]
    binary_feat["binary"][feature_name] = values

# Combine all dictionaries into a nested dictionary
nested_dict = {
    "discrete": disc_feat["discrete"],
    "continuous": continuous_feat["continuous"],
    "binary": binary_feat["binary"]
}

# Print the resulting nested dictionary
print(nested_dict)
