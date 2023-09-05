import csv
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt

# Define the path to the CSV file containing data
csv_file_path = '2023_9_5_output_blocks_cont.csv'

# Read the CSV file and extract the data
data = []
names = []  # Create an empty list to store the names
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Get the header row
    for row in csv_reader:
        name = row[0]
        names.append(name)  # Store the names in the same order as the data
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

# Separate discrete and continuous feature columns
discrete_features = [feature_index for feature_index, feature in enumerate(data[0][1], start=len(data[0][0]) + 1) if
                     isinstance(feature, int)]
continuous_features = [feature_index for feature_index, feature in enumerate(data[0][1], start=len(data[0][0]) + 1) if
                       isinstance(feature, float)]



# Create a color mapping for discrete values
color_mapping = {
    0: 'green',
    1: 'yellow',
    2: '#FFD700',  # Yellow-Orange
    3: 'orange',   # Full orange
    4: '#FF6347',  # Light red
    5: 'red'       # Dark red
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
        count=0
        for points, feature in data:
            fill_color = color_mapping.get(feature[feature_index - len(data[0][0]) - 1], 'black')  # Get color based on feature value
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
        min_value = min(feature[feature_index - len(data[0][0]) - 1] for _, feature in data)
        max_value = max(feature[feature_index - len(data[0][0]) - 1] for _, feature in data)
        color_range = max_value - min_value
        count = 0
        for points, feature in data:
            normalized_value = (feature[feature_index - len(data[0][0]) - 1] - min_value) / color_range
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
            norm = plt.Normalize(0, 1)
            cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax)
            cb.ax.set_title(feature_name, fontsize=12)
            cb.ax.tick_params(labelsize=10)

            # Set a solid background color for the colorbar
            cb.outline.set_edgecolor('black')  # Border color
            cb.outline.set_linewidth(1)  # Border width
            cb.ax.xaxis.set_tick_params(color='black', width=1)  # Tick color and width
            cb.ax.yaxis.set_tick_params(color='black', width=1)  # Tick color and width

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
