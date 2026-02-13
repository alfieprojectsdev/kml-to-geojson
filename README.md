# KML/KMZ to GeoJSON Batch Converter

    A Python utility to batch convert Google Earth KML and KMZ files into GeoJSON format. 

It handles:
- **Multi-layer KMLs:** Iterates through all folders in a KML to find data.
- **Complex KMZs:** Automatically unzips and extracts data if the standard reader fails.
- **Coordinate Systems:** Forces all outputs to standard WGS84 (EPSG:4326).

## Prerequisites

- **Python 3.10+**
- **uv** (An extremely fast Python package manager)

## Installation

1.  **Initialize the project:**
    ```bash
    mkdir kml-to-geojson
    cd kml-to-geojson
    uv init
    ```

2.  **Add dependencies:**
    ```bash
    uv add geopandas fiona pandas
    ```

3.  **Add the script:**
    Copy the `convert.py` script into this directory.

## Usage

1.  **Prepare your files:**
    The script looks for a folder named `input_kml` in the project directory.
    ```bash
    mkdir input_kml
    ```
    Place all your `.kml` and `.kmz` files inside this folder.

2.  **Run the script:**
    ```bash
    uv run convert.py
    ```

3.  **Get results:**
    Converted files will appear in the `output_geojson` folder.

## Troubleshooting

- **Empty GeoJSONs:** The script is designed to scan all layers. If you still get empty files, ensure your KML actually contains geometry (Points, Polygons) and not just NetworkLinks or overlays.
- **Windows Users:** If you encounter errors regarding DLLs or GDAL, `uv` usually handles binary wheels well, but ensure you have the Visual C++ Redistributable installed if needed.
