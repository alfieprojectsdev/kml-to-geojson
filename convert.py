import os
import geopandas as gpd
import pandas as pd
import fiona

# --- CONFIGURATION ---
INPUT_FOLDER = 'input_kml'
OUTPUT_FOLDER = 'output_geojson'
# ---------------------

def enable_kml_driver():
    """
    Ensure KML drivers are enabled in Fiona.
    """
    fiona.drvsupport.supported_drivers['KML'] = 'rw'
    fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

def convert_kml_to_geojson(input_path, output_path):
    try:
        # 1. Get all layers in the KML file
        # KMLs often have nested folders that act as separate layers
        layers = fiona.listlayers(input_path)
        
        all_gdfs = []

        # 2. Loop through every layer to find the data
        for layer_name in layers:
            try:
                # Read the specific layer
                gdf = gpd.read_file(input_path, driver='KML', layer=layer_name)
                
                # If the layer has data, add it to our list
                if not gdf.empty:
                    print(f"   Found {len(gdf)} features in layer: '{layer_name}'")
                    all_gdfs.append(gdf)
            except Exception as e:
                # Some layers might be empty or metadata-only, just skip them
                continue

        # 3. Combine all layers into one GeoJSON
        if all_gdfs:
            # Concatenate all dataframes found
            combined_gdf = pd.concat(all_gdfs, ignore_index=True)

            # Convert to WGS84 (GeoJSON standard)
            if combined_gdf.crs is not None:
                combined_gdf = combined_gdf.to_crs("EPSG:4326")
            
            # Save
            combined_gdf.to_file(output_path, driver='GeoJSON')
            print(f"✅ Success: {os.path.basename(input_path)} -> {len(combined_gdf)} features saved.")
        else:
            print(f"⚠️  Warning: {os.path.basename(input_path)} contains no geometry features in any layer.")

    except Exception as e:
        print(f"❌ Error converting {os.path.basename(input_path)}: {e}")

def main():
    enable_kml_driver()

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Input directory '{INPUT_FOLDER}' not found.")
        return

    print(f"Scanning '{INPUT_FOLDER}' for KML/KMZ files...\n")

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.kml', '.kmz'))]
    
    if not files:
        print("No KML files found.")
        return

    for filename in files:
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_filename = os.path.splitext(filename)[0] + '.geojson'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        convert_kml_to_geojson(input_path, output_path)

if __name__ == "__main__":
    main()