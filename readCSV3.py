import csv
from PIL import Image, ImageDraw, ImageFont

# Define the path to the CSV file containing data
csv_file_path = '2023_9_5_output_blocks_cont.csv'

# Read the CSV file and extract the data
data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Get the header row
    for row in csv_reader:
        name = row[0]
        # Extract and convert points from CSV to tuples
        points = []
        for point_str in row[1:-3]:
            if point_str.strip() == '':
                continue  # Skip empty points
            point = tuple(map(float, point_str.split(',')))
            points.append(point)
        # Handle discrete and continuous values, converting to appropriate types
        features = [float(feature) if '.' in feature else int(feature) for feature in row[-3:]]  # Extract features
        data.append((points, features))

# Calculate image dimensions based on the extracted points
max_x = max(p[0] for points, _ in data for p in points)
max_y = max(p[1] for points, _ in data for p in points)
min_x = min(p[0] for points, _ in data for p in points)
min_y = min(p[1] for points, _ in data for p in points)
image_width = int(max_x - min_x + 400)  # Add some padding for labels
image_height = int(max_y - min_y + 400)  # Add some padding for labels

# Create a color mapping for discrete values
color_mapping = {
    0: 'green',
    1: 'yellow',
    2: 'red'
}

# Choose a font for labeling
font = ImageFont.load_default()  # You can choose an appropriate font

# Create images for each feature column
for feature_index, feature_name in enumerate(header[-3:], start=len(data[0][0]) + 1):
    output_image_path = f'output_image_{feature_name}.png'
    image = Image.new('RGB', (image_width, image_height), 'white')  # Create an image based on calculated dimensions
    draw = ImageDraw.Draw(image)  # Create a drawing object for the image

    # Calculate the title position based on image dimensions
    title_x = image_width // 3
    title_y = 20

    # Add the feature name to the image
    draw.text((title_x, title_y), feature_name, font=font, fill='black')

    if feature_index in discrete_features:
        # Draw shapes for discrete values using extracted points and features
        for points, feature in data:
            fill_color = color_mapping.get(feature[feature_index - len(data[0][0]) - 1], 'black')  # Get color based on feature value
            adjusted_points = [(int(p[0] - min_x + 50), int(p[1] - min_y + 50)) for p in points]  # Adjust points based on image dimensions
            draw.polygon(adjusted_points, outline='black', fill=fill_color)

        # Create a legend for discrete values
        for i, label in enumerate(['0', '1', '2']):
            legend_x = image_width - 150
            legend_y = 50 + i * 50
            draw.rectangle([legend_x, legend_y, legend_x + 30, legend_y + 30], outline='black',
                           fill=color_mapping.get(int(label), 'black'))
            draw.text((legend_x + 40, legend_y), label, font=font, fill='black')
    elif feature_index in continuous_features:
        # Create a grayscale colorbar for continuous values
        min_value = min(feature[feature_index - len(data[0][0]) - 1] for _, feature in data)
        max_value = max(feature[feature_index - len(data[0][0]) - 1] for _, feature in data)
        color_range = max_value - min_value

        for points, feature in data:
            normalized_value = (feature[feature_index - len(data[0][0]) - 1] - min_value) / color_range
            grayscale_value = int(255 * normalized_value)
            fill_color = (grayscale_value, grayscale_value, grayscale_value)
            adjusted_points = [(int(p[0] - min_x + 50), int(p[1] - min_y + 50)) for p in points]  # Adjust points based on image dimensions
            draw.polygon(adjusted_points, outline='black', fill=fill_color)

        # Create a grayscale legend for continuous values
        for i, label in enumerate(['Low', 'High']):
            legend_x = image_width - 150
            legend_y = 50 + i * 50
            grayscale_value = 255 if i == 0 else 0
            draw.rectangle([legend_x, legend_y, legend_x + 30, legend_y + 30], outline='black',
                           fill=(grayscale_value, grayscale_value, grayscale_value))
            draw.text((legend_x + 40, legend_y), label, font=font, fill='black')

    # Save the generated image
    image.save(output_image_path)
