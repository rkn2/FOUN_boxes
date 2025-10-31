# Architectural Data Processing and Visualization Toolkit

=======================================================

This project provides a suite of tools for processing, analyzing, and visualizing architectural data, primarily from CAD files. It includes two main workflows: one for converting `.dxf` files into visual representations based on feature data, and another for performing statistical analysis on the extracted data.

## Workflows

---------

There are two primary workflows in this project:

1\.  **CAD to Image Visualization**: This workflow takes a `.dxf` CAD file, extracts geometric data, associates it with feature data, and generates images that visualize these features.

2\.  **Data Analysis**: This workflow uses Python scripts and a Jupyter Notebook to perform statistical analysis, such as cross-correlation, principal component analysis (PCA), and feature importance, on the architectural data.

##File Descriptions

-----------------

-   `README.md`: This documentation.

-   `boundingBoxes2.py`: A Python script that reads a `.dxf` file and extracts bounding box information for blocks and polylines, saving it to a `.csv` file.

-   `map_maker.py`: A Python script that generates images from the feature vector file (`output_blocks_cont.csv`), color-coding shapes based on discrete or continuous features.

-   `crossCorr.py`: A Python script for performing cross-correlation analysis on the feature data.

-   `hist_sig.py`: A Python script to create histograms of significant features identified by the `crossCorr.py` script.

-   `plot_blocks.py`: A utility script for plotting the shapes from the `output_blocks_cont.csv` file for a quick visual check.

-   `feature_type_dictionary.py`: A script to generate a nested dictionary of feature types from CSV files.

-   `code_for_Mina_FOUN.ipynb`: A Jupyter Notebook for more in-depth data analysis, including correlation matrices, PCA, and feature importance.

## Setup and Installation

----------------------

To use these scripts, you need to have Python installed, along with several libraries. You can install the required libraries using `pip`:

```

pip install -r requirements.txt

```

The `requirements.txt` file should contain:

```

dash

factor_analyzer

ezdxf

shapely

matplotlib

pandas

seaborn

scipy

Pillow

```

## Workflow 1: From CAD to Image Visualization

-------------------------------------------

This workflow converts a `.dxf` file into images that visualize specific features.

### Step 1: Create the CAD File (`.dxf`)

1\.  **Open AutoCAD** and start a new drawing.

2\.  **Set Up Layers** for your wall sections.

3\.  **Draw Closed Polylines** for each wall section using the "Polyline" tool. Ensure each polyline is a closed shape.

4\.  **Create Blocks** from each closed polyline. Use the `BLOCK` command, specify a base point, and give each block a unique, descriptive name (e.g., "Wall_5701").

5\.  **Clean the Model** by deleting everything except the blocks and polylines.

6\.  **Save** the file in `.dxf` format.

### Step 2: Extract Bounding Boxes to CSV

Run the `boundingBoxes2.py` script in the same directory as your `.dxf` file. This script will read the `.dxf` file and create a CSV file named `output_blocks.csv` containing the block names and their bounding box coordinates.

```

python boundingBoxes2.py

```

### Step 3: Create Feature Vector File

1\.  Open the `output_blocks.csv` file.

2\.  Add new columns for the features you want to visualize.

3\.  Save this new file as `output_blocks_cont.csv`.

4\.  Make sure the first row contains the feature names. Use a decimal for continuous features and a whole number for categorical features.

### Step 4: Generate Images from Feature Vectors

Run the `map_maker.py` script in the same directory as `output_blocks_cont.csv`. This script will generate images for each feature, color-coding the shapes based on their feature values.

```

python map_maker.py

```

## Workflow 2: Data Analysis

-------------------------

This workflow is for performing statistical analysis on your feature data.

### Step 1: Cross-Correlation Analysis

The `crossCorr.py` script is used to calculate and visualize the cross-correlation between different features.

1\.  Ensure your data is in a `.csv` file (e.g., `2023_12_8_targeted_eval.csv`).

2\.  Modify the `file_path` variable in `crossCorr.py` to point to your data file.

3\.  Run the script:

```

python crossCorr.py

```

This will:

-   Generate a heatmap of the correlation matrix and display it.

-   Save a CSV file named `*_significant_relationships.csv` listing the feature pairs with statistically significant correlations.

### Step 2: Histogram of Significant Features

The `hist_sig.py` script can be used to visualize the frequency of features that appear in significant correlations. It provides options to view the data with or without treatment-related features.

### Step 3: In-Depth Analysis with Jupyter Notebook

The `code_for_Mina_FOUN.ipynb` notebook provides a more interactive way to analyze your data. It includes:

-   **Correlation Matrix Heatmap**: A visual representation of the relationships between features.

-   **Principal Component Analysis (PCA)**: A technique to reduce the dimensionality of your data and identify the most important components.

-   **Feature Importance**: Using a Random Forest Regressor to determine which features are most predictive of the "Wall Rank".

To use the notebook:

1\.  Open it in a Jupyter environment.

2\.  Ensure your data is in an `.xlsx` file named `OUT-update.xlsx`.

3\.  Run the cells in the notebook to perform the analysis.

## Utility Scripts

---------------

-   **`plot_blocks.py`**: A simple script to visualize the polygons from the `output_blocks_cont.csv` file. This is useful for a quick check to ensure your geometric data has been extracted correctly.

-   **`feature_type_dictionary.py`**: This script helps create a nested dictionary of your feature types (discrete, continuous, binary) from separate CSV files. This can be useful for organizing and managing your feature data programmatically.
