import csv
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
import csv
import pandas as pd
import numpy as np

def extract_data_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        raw_df = pd.read_csv(csv_file_path)
    columns_with_point = [col for col in raw_df.columns if 'point' in col.lower()]
    # Get columns that are not columns with 'point' in their names
    columns_without_point = [col for col in raw_df.columns if col not in columns_with_point]
    # Include the first column from 'raw_df'
    selected_columns = ['Unnamed: 0'] + columns_with_point
    # Create a new DataFrame with the selected columns
    points_df = raw_df[selected_columns]

    # Create a new DataFrame with columns that are not columns with 'point'
    feature_df = raw_df[['Unnamed: 0'] + columns_without_point]

    return points_df, feature_df

# Example usage: dataFrame = extract_data_from_csv(csv_file_path)

def calculate_image_dimensions_defunct(points_df, padding=400):
    max_x = max(p[0] for points, _ in data for p in points)
    max_y = max(p[1] for points, _ in data for p in points)
    min_x = min(p[0] for points, _ in data for p in points)
    min_y = min(p[1] for points, _ in data for p in points)

    image_width = int(max_x - min_x + padding)
    image_height = int(max_y - min_y + padding)

    return image_width, image_height

# Example usage: image_width, image_height = calculate_image_dimensions(data)
def calculate_image_size(points_df):
    # Initialize minimum and maximum coordinates with large values
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    # Loop through the DataFrame and find the minimum and maximum coordinates
    for index, row in points_df.iterrows():
        coordinates = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in row[1:] if pd.notna(coord)]
        for x, y in coordinates:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

    # Calculate image width and height based on the range of coordinates
    image_width = int(max_x - min_x) + 50
    image_height = int(max_y - min_y) + 50

    return image_width, image_height


def extract_feature_columns(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Get the header row

        # Extract feature columns starting from the 10th column (1-based index)
        feature_columns = header[10:]

    return feature_columns

# Example usage: feature_columns = extract_feature_columns(csv_file_path)


def create_nested_dict(disc_file_path, cont_file_path, bin_file_path):
    # Read and process the discrete data
    df_disc = pd.read_csv(disc_file_path, sep=',')
    disc_feat = {}
    for index, row in df_disc.iterrows():
        feature_name = row['discrete']
        values = {}
        for i in range(1, len(row), 3):
            value_str = row[i]
            if pd.notna(value_str):
                value = int(value_str)
                color = row[i + 1]
                legend = row[i + 2]
                values[str(value)] = {
                    "color": color,
                    "legend": legend
                }
        disc_feat[feature_name] = values

    # Read and process the continuous data
    df_cont = pd.read_csv(cont_file_path, sep=',', header=0, names=['label', 'colorscale'])
    continuous_feat = {}
    # Iterate through the rows and populate the dictionary
    for _, row in df_cont.iterrows():
        feature_name = row['label']
        colorscale = row['colorscale']
        continuous_feat[feature_name] = colorscale

    # Read and process the binary data
    df_bin = pd.read_csv(bin_file_path, sep='\t', header=0, index_col=0)
    binary_dict = {}
    # Iterate through the rows and populate the dictionary
    for index, row in df_bin.iterrows():
        feature_name = index
        values = {}
        for i in range(len(row)):
            value = int(row.index[i])
            color = row[i]
            values[value] = color
        binary_dict[feature_name] = values

    # Combine all dictionaries into a nested dictionary
    nested_dict = {
        "discrete": disc_feat,
        "continuous": continuous_feat,
        "binary": binary_dict
    }

    return nested_dict
# Example usage:
# disc_file_path = 'disc_file.csv'  # Replace with the actual path to your discrete CSV file
# cont_file_path = 'cont_file.csv'    # Replace with the actual path to your continuous CSV file
# bin_file_path = 'bin_file.csv'      # Replace with the actual path to your binary CSV file
# nested_dict = create_nested_dict(disc_file_path, cont_file_path, bin_file_path)

def parse_coordinates(row):
    points = row.split(', ')
    coordinates = [(float(points[i]), float(points[i + 1])) for i in range(0, len(points), 2)]
    return coordinates

def draw_discrete_shapes(points_df, feature_df, nested_dict, feature_of_interest, output_image_path):
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)
    colors = []
    labels = []
    # Create a blank matplotlib figure and axis
    fig, ax = plt.subplots()
    # Loop through the DataFrame and draw polygons
    for index, row in points_df.iterrows():
        coordinates = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in row[1:] if pd.notna(coord)]
        if coordinates:
            # Get the feature value for this shape
            shape_name = row['Unnamed: 0']
            # Get the feature value for this shape and feature_of_interest
            feature_value = feature_df.query("`Unnamed: 0` == @shape_name")[feature_of_interest].values[0]
            # Now, that i have my feature value i want to lookin my dictioarny to see what color i should be using
            color = nested_dict['discrete'][feature_of_interest][str(int(feature_value))]['color']
            if color not in colors:
                label = nested_dict['discrete'][feature_of_interest][str(int(feature_value))]['legend']
                colors.append(color)
                labels.append(label)

            draw.polygon(coordinates, outline='black', fill=color)
            # Calculate the center of the rectangle
            center_x = sum(p[0] for p in coordinates) // len(coordinates)
            center_y = sum(p[1] for p in coordinates) // len(coordinates)
            # Draw the name as text in the center
            draw.text((center_x, center_y), shape_name, fill='black')

    # Calculate the height of the legend image based on the number of labels
    legend_height = len(labels) * 30  # Adjust as needed for spacing
    # Create a legend image using matplotlib
    legend_image = Image.new('RGB', (200, legend_height), 'white')
    legend_draw = ImageDraw.Draw(legend_image)
    font = ImageFont.load_default()
    legend_y = 10
    for color, label in zip(colors, labels):
        legend_draw.rectangle([10, legend_y, 30, legend_y + 20], fill=color, outline='black')
        legend_draw.text((40, legend_y), label, fill='black', font=font)
        legend_y += 30
    # Overlay the legend image on top of the main image
    image.paste(legend_image, (10, 30))
    # Add a title at the top of the image based on the feature_of_interest
    title_text = f"Feature of Interest: {feature_of_interest}"
    title_position = (0, 0)  # Adjust the Y-coordinate (10) as needed
    # Calculate the width and height of the white rectangle for the title background
    title_bg_width = 300  # Add some padding
    title_bg_height = 30  # Add some padding
    # Draw a white rectangle as a background for the title
    draw.rectangle([title_position, (title_position[0] + title_bg_width, title_position[1] + title_bg_height)],
                   fill='white')
    title_position = (10, 10)
    draw.text(title_position, title_text, fill='black')

    # Save the combined image to the specified output path
    image.save(output_image_path)
    print(f"Image with legend and title saved to {output_image_path}")
    image.show()

# Example usage:
date = '2023_12_5_'
csv_file_path = date+'targeted_eval.csv'
points_df, feature_df= extract_data_from_csv(csv_file_path)
image_width, image_height = calculate_image_size(points_df)
feature_columns = extract_feature_columns(csv_file_path)
feature_of_interest = 'Sill 1'
output_image_path = 'output2.png'

disc_file_path = 'disc_file.csv'  # Replace with the actual path to your discrete CSV file
cont_file_path = 'cont_file.csv'    # Replace with the actual path to your continuous CSV file
bin_file_path = 'bin_file.csv'      # Replace with the actual path to your binary CSV file
nested_dict = create_nested_dict(disc_file_path, cont_file_path, bin_file_path)

if feature_of_interest in nested_dict['discrete']:
    print(f"{feature_of_interest} is a discrete feature.")
    draw_discrete_shapes(points_df, feature_df, nested_dict, feature_of_interest, output_image_path)
elif feature_of_interest in nested_dict['continuous']:
    print(f"{feature_of_interest} is a continuous feature.")
elif feature_of_interest in nested_dict['binary']:
    print(f"{feature_of_interest} is a binary feature.")
else:
    print(f"{feature_of_interest} is not found in any of the dictionaries.")

# ^^ works














# __ older stuff __

# Choose a font for labeling
font = ImageFont.load_default()  # You can choose an appropriate font

# Create images for each feature column
for feature_index, feature_name in enumerate(header[-featCols:], start=len(data[0][0]) + 1): #HER

    if feature_index in discrete_features:
        # Draw shapes for discrete values using extracted points and features
        count=0
        for points, feature in data:
            fill_color = color_mapping.get(feature[feature_index - len(data[0][0]) - 1], 'white')  # Get color based on feature value
            adjusted_points = [(int(p[0] - min_x + 50), int(p[1] - min_y + 50)) for p in points]  # Adjust points based on image dimensions
            draw.polygon(adjusted_points, outline='black', fill=fill_color)

            # Calculate the center of the rectangle
            center_x = sum(p[0] for p in adjusted_points) // len(adjusted_points)
            center_y = sum(p[1] for p in adjusted_points) // len(adjusted_points)

            # Draw the name as text in the center
            text_x = center_x - (len(feature) * 2)  # Adjust text position based on text length
            text_y = center_y - 10  # Adjust text position vertically
            draw.text((text_x, text_y), names[count], font=font, fill='black')
            count = count + 1

        # Create a legend for discrete values
        for i, label in enumerate(['0', '1', '2', '3', '4', '5']):
            legend_x = image_width - 150
            legend_y = 50 + i * 50
            draw.rectangle([legend_x, legend_y, legend_x + 30, legend_y + 30], outline='black',
                           fill=color_mapping.get(int(label), 'black'))
            draw.text((legend_x + 40, legend_y), label, font=font, fill='black')
    elif feature_index in continuous_features:
        # Create a grayscale colorbar for continuous values
        min_value = min(float(feature[feature_index - len(data[0][0]) - 1]) for _, feature in data if isinstance(feature[feature_index - len(data[0][0]) - 1], (int, float)))
        max_value = max(float(feature[feature_index - len(data[0][0]) - 1]) for _, feature in data if isinstance(feature[feature_index - len(data[0][0]) - 1], (int, float)))
        color_range = max_value - min_value
        count = 0
        for points, feature in data:
            # Check if the value is not an empty string and can be converted to a float
            value_to_convert = feature[feature_index - len(data[0][0]) - 1]
            if value_to_convert != '' and value_to_convert != '-':
                value_as_float = float(value_to_convert)
            else:
                value_as_float = 0.0  # Or any other default value you prefer

            normalized_value = (value_as_float - min_value) / color_range

            grayscale_value = int(255 * normalized_value)
            fill_color = (grayscale_value, grayscale_value, grayscale_value)
            adjusted_points = [(int(p[0] - min_x + 50), int(p[1] - min_y + 50)) for p in points]  # Adjust points based on image dimensions
            draw.polygon(adjusted_points, outline='black', fill=fill_color)

            # Calculate the center of the rectangle
            center_x = sum(p[0] for p in adjusted_points) // len(adjusted_points)
            center_y = sum(p[1] for p in adjusted_points) // len(adjusted_points)

            # Draw the name as text in the center
            text_x = center_x - (len(feature) * 2)  # Adjust text position based on text length
            text_y = center_y - 10  # Adjust text position vertically
            draw.text((text_x, text_y), names[count], font=font, fill='red')
            count = count + 1

            # Create a grayscale colorbar for continuous values
            colorbar_x = image_width - 200
            colorbar_y = 100
            colorbar_width = 25
            colorbar_height = 400

            # Create a smooth gradient colorbar using matplotlib
            fig, ax = plt.subplots(figsize=(1, 6))
            cmap = plt.get_cmap('gray')
            norm = plt.Normalize(min_value, max_value)
            cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax)
            cb.ax.set_title(feature_name, fontsize=12)
            cb.ax.tick_params(labelsize=10)

            # Set a solid background color for the colorbar
            cb.outline.set_edgecolor('black')  # Border color
            cb.outline.set_linewidth(1)  # Border width
            cb.ax.xaxis.set_tick_params(color='black', width=1)  # Tick color and width
            cb.ax.yaxis.set_tick_params(color='black', width=1)  # Tick color and width
            # Customize colorbar labels with min_value and max_value
            cb.set_ticks([min_value, max_value])
            cb.set_ticklabels([str(min_value), str(max_value)])

            # Save the colorbar as an image
            colorbar_image_path = f'colorbar_{feature_name}.png'
            plt.savefig(colorbar_image_path, bbox_inches='tight', pad_inches=0, transparent=False, dpi=300)
            plt.close()

            # Load and paste the colorbar onto the main image
            colorbar_image = Image.open(colorbar_image_path)
            colorbar_image = colorbar_image.resize((80, 400))
            image.paste(colorbar_image, (colorbar_x, colorbar_y))

    # Save the generated image
    image.save(output_image_path)
