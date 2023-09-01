# Import necessary libraries
import csv
from PIL import Image, ImageDraw, ImageFont  # Make sure to install PIL using "pip install Pillow"

# Define the path to the CSV file containing data
csv_file_path = 'output_blocks_cont.csv'

# Read the CSV file and extract the data
data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Get the header row
    for row in csv_reader:
        name = row[0]
        # Extract and convert points from CSV to tuples
        points = [tuple(map(float, point.split(','))) for point in row[1:5]]
        # Handle discrete and continuous values, converting to appropriate types
        features = [float(feature) if '.' in feature else int(feature) for feature in row[5:]]
        data.append((points, features))

# Separate discrete and continuous feature columns
discrete_features = [feature_index for feature_index, feature in enumerate(data[0][1], start=4) if
                     isinstance(feature, int)]
continuous_features = [feature_index for feature_index, feature in enumerate(data[0][1], start=4) if
                       isinstance(feature, float)]

# Define a color mapping for discrete values
color_mapping = {
    0: 'green',
    1: 'yellow',
    2: 'red'
}

# Choose a font for labeling
font = ImageFont.load_default()  # You can choose an appropriate font

# Create images for each feature column
for feature_index, feature_name in enumerate(header[5:], start=4):
    output_image_path = f'output_image_{feature_name}.png'
    image = Image.new('RGB', (1000, 800), 'white')  # Create a white image with specified dimensions
    draw = ImageDraw.Draw(image)  # Create a drawing object for the image

    # Add the feature name to the image
    draw.text((400, 20), feature_name, font=font, fill='black')

    if feature_index in discrete_features:
        # Draw shapes for discrete values using extracted points and features
        for points, feature in data:
            fill_color = color_mapping.get(feature[feature_index - 4], 'black')  # Get color based on feature value
            draw.polygon(points, outline='black', fill=fill_color)

        # Create a legend for discrete values
        for i, label in enumerate(['0', '1', '2']):
            legend_x = 850
            legend_y = 50 + i * 50
            draw.rectangle([legend_x, legend_y, legend_x + 30, legend_y + 30], outline='black',
                           fill=color_mapping.get(int(label), 'black'))
            draw.text((legend_x + 40, legend_y), label, font=font, fill='black')
    elif feature_index in continuous_features:
        # Create a grayscale colorbar for continuous values
        min_value = min(feature[feature_index - 4] for _, feature in data)
        max_value = max(feature[feature_index - 4] for _, feature in data)
        color_range = max_value - min_value

        for points, feature in data:
            normalized_value = (feature[feature_index - 4] - min_value) / color_range
            grayscale_value = int(255 * normalized_value)
            fill_color = (grayscale_value, grayscale_value, grayscale_value)
            draw.polygon(points, outline='black', fill=fill_color)

        # Create a grayscale legend for continuous values
        for i, label in enumerate(['Low', 'High']):
            legend_x = 850
            legend_y = 50 + i * 50
            grayscale_value = 255 if i == 0 else 0
            draw.rectangle([legend_x, legend_y, legend_x + 30, legend_y + 30], outline='black',
                           fill=(grayscale_value, grayscale_value, grayscale_value))
            draw.text((legend_x + 40, legend_y), label, font=font, fill='black')

    # Save the generated image
    image.save(output_image_path)
