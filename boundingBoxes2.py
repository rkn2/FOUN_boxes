import csv
import ezdxf

# Path to your DWG file
input_dwg = "rect_blocks.dxf"
output_csv = "output_blocks.csv"

# Load the DWG file
doc = ezdxf.readfile(input_dwg)
msp = doc.modelspace()

# Create a dictionary to store block data
block_data = {}

# Loop over each block in the model space
for block_ref in msp.query('INSERT'):
    block_name = block_ref.dxf.name
    block = doc.blocks[block_name]  # Get the block definition
    if block:
        block_ref_location = block_ref.dxf.insert  # Insertion point of the block reference
        block_points = []

        # Loop over each entity in the block definition
        for entity in block:
            if entity.dxftype() == 'LWPOLYLINE':
                polyline = entity  # The LWPOLYLINE entity
                polyline_vertices = [(block_ref_location[0] + vertex[0], block_ref_location[1] + vertex[1])
                                     for vertex in polyline.get_points('xy')]
                block_points.extend(polyline_vertices)

        block_data[block_name] = block_points

# Create a CSV file for writing
with open(output_csv, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Create the header row
    header = ["block name"]
    max_points = max(len(points) for points in block_data.values())
    for i in range(1, max_points + 1):
        header.append(f"point {i}")
    csv_writer.writerow(header)

    # Write data for each block
    for block_name, points in block_data.items():
        row_data = [block_name] + [f"{point[0]}, {point[1]}" for point in points]
        csv_writer.writerow(row_data)
