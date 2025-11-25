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
        points = []

        # Dynamically extract points from CSV columns
        for col_value in row[1:]:
            if col_value.strip():
                point = tuple(map(float, col_value.split(',')))
                points.append(point)

        # Ensure the polygon is closed by repeating the first vertex as the last
        if len(points) > 2 and points[0] != points[-1]:
            points.append(points[0])

        # Create a Shapely Polygon object
        polygon = Polygon(points)

        # Extract discrete and continuous values
        discrete_value = int(row[len(points) + 1])
        discrete2_value = int(row[len(points) + 2])
        continuous_value = float(row[len(points) + 3])

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
