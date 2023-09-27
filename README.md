# Making the cad file
Open AutoCAD: Launch AutoCAD software on your computer.

Start a New Drawing: Create a new drawing or open an existing one where you want to add wall sections.

Setting Up Layers: Ensure you have appropriate layers set up for your wall sections. You can create new layers for walls or use existing ones if applicable.

Draw Closed Polylines:

a. Click on the "Polyline" tool in the "Home" or "Draw" tab, depending on your AutoCAD version.

b. Start drawing the wall section by clicking on the starting point. Continue clicking at each corner or change in direction until you've outlined the entire wall section. Ensure that the polyline forms a closed shape, meaning the last point connects to the first one.

c. Press "Enter" to finish the polyline.

d. Repeat this process for each wall section, ensuring that each one is drawn as a separate, closed polyline.

Create Blocks:

a. Select the closed polyline that represents a wall section.

b. Type "BLOCK" in the command line and press "Enter."

c. AutoCAD will prompt you to specify a base point for the block. Choose a point that makes sense for your wall section, usually one of the corners or an easily recognizable reference point.

d. AutoCAD will then ask you to specify a block name. Assign a unique and descriptive name to the block representing that wall section. For example, you could use names like "Wall_5701," "Wall_02," etc.

e. Save the block definition.

Repeat: Repeat steps 4 and 5 for each wall section in your drawing, giving each block a unique name.

Delete anything else in your model and only keep the blocks and polylines. 

Save your file as .dxf. 

# Extracting the names and boxes to csv
run boundingBoxes2.py in the same place as your .dxf.

# create feature vector file
copy the output_blocks.csv and add feature columns to it. save that as output_blocks_cont.csv
make sure that the first row is filled in, has a decimal if it needs to be continuous, and has a whole number if its categorical


# Extracting the names, points, and creating images from feature vectors
run readCSV8.py in the same place as "output_blocks_cont.csv"
you hard coded the number of feature columns so if you add another feature update that variable at the top ofthe code i readCSV.
FYI: num features does not include wall name or any of the geometry points