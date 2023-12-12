import csv
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import Normalize
from typing import Tuple

class DataProcessor:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.raw_df = None
        self.points_df = None
        self.feature_df = None
        self.image_width = None
        self.image_height = None
        self.feature_columns = None
        self.nested_dict = None

    def extract_data_from_csv(self):
        with open(self.csv_file_path, 'r') as csv_file:
            self.raw_df = pd.read_csv(self.csv_file_path)

        columns_with_point = [col for col in self.raw_df.columns if 'point' in col.lower()]
        columns_without_point = [col for col in self.raw_df.columns if col not in columns_with_point]
        selected_columns = ['Unnamed: 0'] + columns_with_point
        self.points_df = self.raw_df[selected_columns]
        self.feature_df = self.raw_df[['Unnamed: 0'] + columns_without_point]

    def calculate_image_size(self):
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for index, row in self.points_df.iterrows():
            coordinates = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in row[1:] if pd.notna(coord)]
            for x, y in coordinates:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

        self.image_width = int(max_x - min_x) + 50
        self.image_height = int(max_y - min_y) + 50
        self.min_y = min_y
        self.min_x = min_x

    # def extract_feature_columns(self):
    #     with open(self.csv_file_path, 'r') as csv_file:
    #         csv_reader = csv.reader(csv_file)
    #         header = next(csv_reader)
    #         self.feature_columns = header[10:]

    def create_nested_dict(self, disc_file_path, cont_file_path):
        # Process the discrete data
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

        # Process the continuous data
        df_cont = pd.read_csv(cont_file_path, sep=',', header=0, names=['label', 'colorscale'])
        continuous_feat = {}
        for _, row in df_cont.iterrows():
            feature_name = row['label']
            colorscale = row['colorscale']
            continuous_feat[feature_name] = colorscale

        # Combine all dictionaries into a nested dictionary
        self.nested_dict = {
            "discrete": disc_feat,
            "continuous": continuous_feat
        }

class ShapeDrawer:
    def __init__(self, feature_of_interest, processor):
        self.processor = processor
        self.feature_of_interest = feature_of_interest
        self.image = Image.new('RGB', (processor.image_width, processor.image_height), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def draw_discrete_shapes(self):
        colors = []
        labels = []

        for index, row in self.processor.points_df.iterrows():
            coordinates = [(float(coord.split(',')[0])-self.processor.min_x, float(coord.split(',')[1])-self.processor.min_y) for coord in row[1:] if pd.notna(coord)]
            if coordinates:
                shape_name = row['Unnamed: 0']
                feature_value = self.processor.feature_df.query("`Unnamed: 0` == @shape_name")[self.feature_of_interest].values[0]
                color = self.processor.nested_dict['discrete'][self.feature_of_interest][str(int(feature_value))]['color']
                if color not in colors:
                    label = self.processor.nested_dict['discrete'][self.feature_of_interest][str(int(feature_value))]['legend']
                    colors.append(color)
                    labels.append(label)

                self.draw.polygon(coordinates, outline='black', fill=color)
                center_x = sum(p[0] for p in coordinates) // len(coordinates)
                center_y = sum(p[1] for p in coordinates) // len(coordinates)
                self.draw.text((center_x, center_y), shape_name, fill='black')

        legend_height = len(labels) * 30
        legend_image = Image.new('RGB', (200, legend_height), 'white')
        legend_draw = ImageDraw.Draw(legend_image)
        font = ImageFont.load_default()
        legend_y = 10

        for color, label in zip(colors, labels):
            legend_draw.rectangle([10, legend_y, 30, legend_y + 20], fill=color, outline='black')
            legend_draw.text((40, legend_y), label, fill='black', font=font)
            legend_y += 30

        self.image.paste(legend_image, (10, 30))
        title_text = f"Feature of Interest: {self.feature_of_interest}"
        title_position = (0, 0)
        title_bg_width = 300
        title_bg_height = 30
        self.draw.rectangle([title_position, (title_position[0] + title_bg_width, title_position[1] + title_bg_height)],
                            fill='white')
        title_position = (10, 10)
        self.draw.text(title_position, title_text, fill='black')

    def draw_continuous_shapes(self):
        for index, row in self.processor.points_df.iterrows():
            coordinates = [(float(coord.split(',')[0])-self.processor.min_x, float(coord.split(',')[1])-self.processor.min_y) for coord in row[1:] if pd.notna(coord)]
            if coordinates:
                shape_name = row['Unnamed: 0']
                feature_value = self.processor.feature_df.query("`Unnamed: 0` == @shape_name")[self.feature_of_interest].values[0]
                colorscale = self.processor.nested_dict['continuous'][self.feature_of_interest].capitalize()
                min_value = min(self.processor.feature_df[self.feature_of_interest])
                max_value = max(self.processor.feature_df[self.feature_of_interest])
                normalized_value = (feature_value - min_value) / (max_value - min_value)
                grayscale_value = int(255 * normalized_value)
                color = (grayscale_value, grayscale_value, grayscale_value)

                self.draw.polygon(coordinates, outline='black', fill=color)
                center_x = sum(p[0] for p in coordinates) // len(coordinates)
                center_y = sum(p[1] for p in coordinates) // len(coordinates)
                self.draw.text((center_x, center_y), shape_name, fill='black')

        colorbar_x = 0
        colorbar_y = 0
        colorbar_width = 2
        colorbar_height = 4

        fig, ax = plt.subplots(figsize=(1, 6))
        cmap = plt.get_cmap(colorscale)
        norm = Normalize(vmin=min_value, vmax=max_value)
        cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax)
        cb.ax.set_title(self.feature_of_interest, fontsize=12)
        cb.ax.tick_params(labelsize=10)
        cb.outline.set_edgecolor('black')
        cb.outline.set_linewidth(1)
        cb.ax.xaxis.set_tick_params(color='black', width=1)
        cb.ax.yaxis.set_tick_params(color='black', width=1)

        colorbar_image_path = 'colorbar.png'
        fig.savefig(colorbar_image_path, bbox_inches='tight', transparent=True, dpi=150)

        colorbar_image = Image.open(colorbar_image_path)
        self.image.paste(colorbar_image, (colorbar_x, colorbar_y))

    def save_image(self, output_image_path):
        self.image.save(output_image_path)
        print(f"Image with legend and title saved to {output_image_path}")
        self.image.show()

def main():
    date = '2023_12_8_'
    csv_file_path = date + 'targeted_eval.csv'
    disc_file_path = 'disc_file.csv'  # Replace with the actual path to your discrete CSV file
    cont_file_path = 'cont_file.csv'  # Replace with the actual path to your continuous CSV file
    feature_of_interests = ['Sill 1', 'Coat WGT SCR']  # Change to the desired feature list
    processor = DataProcessor(csv_file_path)
    processor.extract_data_from_csv()
    processor.calculate_image_size()
    #processor.extract_feature_columns()
    processor.create_nested_dict(disc_file_path, cont_file_path)

    for feature_of_interest in feature_of_interests:
        if feature_of_interest in processor.nested_dict['discrete']:
            print(f"{feature_of_interest} is a discrete feature.")
            drawer = ShapeDrawer(feature_of_interest, processor)
            drawer.draw_discrete_shapes()
            drawer.save_image(f"{feature_of_interest}.png")
        elif feature_of_interest in processor.nested_dict['continuous']:
            print(f"{feature_of_interest} is a continuous feature.")
            drawer = ShapeDrawer(feature_of_interest, processor)
            drawer.draw_continuous_shapes()
            drawer.save_image(f"{feature_of_interest}.png")
        else:
            print(f"{feature_of_interest} is not found in any of the dictionaries.")


if __name__ == "__main__":
    main()
