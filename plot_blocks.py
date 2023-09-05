import csv
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

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
        # Create a Shapely Polygon object
        polygon = Polygon(points)
        # Extract discrete and continuous values
        discrete_value = int(row[5])
        discrete2_value = int(row[6])
        continuous_value = float(row[7])
        data.append((name, polygon, discrete_value, discrete2_value, continuous_value))

# Create a figure and axis for plotting
fig, ax = plt.subplots()

# Plot each shape
for name, polygon, _, _, _ in data:
    x, y = polygon.exterior.xy
    plt.plot(x, y, label=name)

# Set axis labels and legend
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.legend()

# Show the plot
plt.show()
