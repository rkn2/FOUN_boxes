import csv
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
import csv
import pandas as pd
import numpy as np
from matplotlib.colors import Normalize

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

def create_nested_dict(disc_file_path, cont_file_path):
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

    # Combine all dictionaries into a nested dictionary
    nested_dict = {
        "discrete": disc_feat,
        "continuous": continuous_feat
    }

    return nested_dict

def parse_coordinates(row):
    points = row.split(', ')
    coordinates = [(float(points[i]), float(points[i + 1])) for i in range(0, len(points), 2)]
    return coordinates

def draw_discrete_shapes(points_df, feature_df, nested_dict, feature_of_interest):
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
    output_image_path = str(feature_of_interest) + '.png'
    image.save(output_image_path)
    print(f"Image with legend and title saved to {output_image_path}")
    image.show()

def draw_continuous_shapes(points_df, feature_df, nested_dict, feature_of_interest):
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)

    # Create a blank matplotlib figure and axis
    fig, ax = plt.subplots()

    # Loop through the DataFrame and draw polygons
    for index, row in points_df.iterrows():
        coordinates = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in row[1:] if pd.notna(coord)]

        # Now, that I have my feature value, I want to look in my dictionary to see what color I should be using
        colorscale = nested_dict['continuous'][feature_of_interest].capitalize()

        # What is the min feature value
        min_value = min(feature_df[feature_of_interest])
        # What is the max feature value
        max_value = max(feature_df[feature_of_interest])

        if coordinates:
            # Get the feature value for this shape
            shape_name = row['Unnamed: 0']
            # Get the feature value for this shape and feature_of_interest
            feature_value = feature_df.query("`Unnamed: 0` == @shape_name")[feature_of_interest].values[0]
            #print(feature_value)

            normalized_value = (feature_value - min_value) / (max_value - min_value)
            grayscale_value = int(255 * normalized_value)
            color = (grayscale_value, grayscale_value, grayscale_value)

            draw.polygon(coordinates, outline='black', fill=color)
            # Calculate the center of the rectangle
            center_x = sum(p[0] for p in coordinates) // len(coordinates)
            center_y = sum(p[1] for p in coordinates) // len(coordinates)
            # Draw the name as text in the center
            draw.text((center_x, center_y), shape_name, fill='black')


    # Create a colorbar for continuous values
    colorbar_x = 0
    colorbar_y = 0

    # Create a smooth gradient colorbar using matplotlib
    fig, ax = plt.subplots(figsize=(1, 6))
    cmap = plt.get_cmap(colorscale)
    norm = Normalize(vmin=min_value, vmax=max_value)
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax)
    cb.ax.set_title(feature_of_interest, fontsize=12)
    cb.ax.tick_params(labelsize=10)

    # Set a solid background color for the colorbar
    cb.outline.set_edgecolor('black')  # Border color
    cb.outline.set_linewidth(1)  # Border width
    cb.ax.xaxis.set_tick_params(color='black', width=1)  # Tick color and width
    cb.ax.yaxis.set_tick_params(color='black', width=1)  # Tick color and width

    # Save the colorbar as a separate image
    colorbar_image_path = 'colorbar.png'
    fig.savefig(colorbar_image_path, bbox_inches='tight', transparent=True, dpi=100)

    # Load the colorbar image and paste it onto the main image
    colorbar_image = Image.open(colorbar_image_path)
    image.paste(colorbar_image, (colorbar_x, colorbar_y))
    output_image_path = str(feature_of_interest) + '.png'
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
#feature_of_interest = 'Sill 1' # discrete
#feature_of_interest = 'Coat WGT SCR' # continuous
feature_of_interest = '1960_treat_2' # binary


disc_file_path = 'disc_file.csv'  # Replace with the actual path to your discrete CSV file
cont_file_path = 'cont_file.csv'    # Replace with the actual path to your continuous CSV file
nested_dict = create_nested_dict(disc_file_path, cont_file_path)

if feature_of_interest in nested_dict['discrete']:
    print(f"{feature_of_interest} is a discrete feature.")
    draw_discrete_shapes(points_df, feature_df, nested_dict, feature_of_interest)
elif feature_of_interest in nested_dict['continuous']:
    print(f"{feature_of_interest} is a continuous feature.")
    draw_continuous_shapes(points_df, feature_df, nested_dict, feature_of_interest)
else:
    print(f"{feature_of_interest} is not found in any of the dictionaries.")

