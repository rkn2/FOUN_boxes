import csv
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt

date = '2023_9_27_'
csv_file_path = date+'targeted_eval.csv'

import csv

def extract_data_from_csv(csv_file_path):
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
            for point_str in row[1:10]:  # Extract columns 1 to 9
                if point_str.strip() == '':
                    continue  # Skip empty points
                point = tuple(map(float, point_str.split(',')))
                points.append(point)
            # Handle discrete and continuous values, converting to appropriate types
            features = []
            for feature in row[10:]:  # Extract columns from 10 to the end
                if not feature:
                    # Replace empty entries with '-'
                    feature = '-'
                elif '.' in feature:
                    feature = float(feature)
                else:
                    feature = int(feature)
                features.append(feature)
            data.append((points, features))

    return names, data

# Example usage:
names, data = extract_data_from_csv(csv_file_path)


def calculate_image_dimensions(data, padding=400):
    max_x = max(p[0] for points, _ in data for p in points)
    max_y = max(p[1] for points, _ in data for p in points)
    min_x = min(p[0] for points, _ in data for p in points)
    min_y = min(p[1] for points, _ in data for p in points)

    image_width = int(max_x - min_x + padding)
    image_height = int(max_y - min_y + padding)

    return image_width, image_height


# Example usage:
image_width, image_height = calculate_image_dimensions(data)
print(f"Image Dimensions: {image_width} x {image_height}")


# based on the feature you are interested in
# look up if it is continuous, discrete, or binary
# based on that, look up the color scheme









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
