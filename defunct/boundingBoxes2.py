# Import necessary libraries
import csv
import ezdxf  # Make sure to install the ezdxf library using "pip install ezdxf"

# Each wall section needs to be a closed polyline in its own, named block

# Define the path to your DWG file
#input_dwg = "WALL BLOCK1_v2.dxf" #original that works
input_dwg = "12.10.2023- flipped.dxf"
output_csv = "2023_12_11_output_blocks.csv"

# Load the DWG file
doc = ezdxf.readfile(input_dwg)  # Read the DWG file using ezdxf
msp = doc.modelspace()  # Get the modelspace of the DWG file

# Create a dictionary to store block data
block_data = {}

# Loop over each block in the model space
for block_ref in msp.query('INSERT'):
    block_name = block_ref.dxf.name  # Get the name of the block reference
    block = doc.blocks[block_name]  # Get the block definition based on the name

    if block:
        block_ref_location = block_ref.dxf.insert  # Get the insertion point of the block reference
        block_points = []

        # Loop over each entity in the block definition
        for entity in block:
            if entity.dxftype() == 'LWPOLYLINE':  # Check if the entity is a closed polyline
                polyline = entity  # Store the LWPOLYLINE entity
                # Calculate the absolute coordinates of each vertex in the polyline
                polyline_vertices = [(block_ref_location[0] + vertex[0], block_ref_location[1] + vertex[1])
                                     for vertex in polyline.get_points('xy')]
                block_points.extend(polyline_vertices)  # Extend the list of block points

        block_data[block_name] = block_points  # Store the block's data in the dictionary

# Create a CSV file for writing
with open(output_csv, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Create the header row for the CSV file
    header = ["block name"]
    max_points = max(len(points) for points in block_data.values())  # Find the maximum number of points among all blocks
    for i in range(1, max_points + 1):
        header.append(f"point {i}")
    csv_writer.writerow(header)  # Write the header row to the CSV file

    # Write data for each block to the CSV file
    for block_name, points in block_data.items():
        row_data = [block_name] + [f"{point[0]}, {point[1]}" for point in points]
        csv_writer.writerow(row_data)  # Write the data for the current block to the CSV file
