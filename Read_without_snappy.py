import os
import zipfile
import rasterio
import numpy as np
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from rasterio.plot import show

# Set your Copernicus Open Access Hub credentials
username = 'muhannadsarsat'
password = 'Ms!42302658'

# Define the area of interest and time range
aoi_geojson = {
    "type": "Polygon",
    "coordinates": [
        [
            [41.10979923608616, 31.780155925771567],
            [40.74338163414552, 31.4951937267774],
            [41.387927296953904, 31.552032949840836],
            [41.260977210263775, 31.68762594713526],
            [41.10979923608616, 31.780155925771567]
        ]
    ]
}
start_date = '20230101'
end_date = '20230326'

# Connect to the API
api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')

# Search for images
footprint = geojson_to_wkt(aoi_geojson)
products = api.query(footprint,
                     date=(start_date, end_date),
                     platformname='Sentinel-1',
                     producttype='GRD',
                     orbitdirection='DESCENDING',
                     polarisationmode='VV')


# Download images
try:
    downloaded_files = api.download_all(products)
except Exception as e:
    print(f"Error while downloading files: {e}")

# Get the successful downloads and image paths
successful_downloads = downloaded_files[0]
image_paths = [f['path'] for f in successful_downloads.values() if 'path' in f]

# Change detection
def normalize(img):
    return (img - np.min(img)) / (np.max(img) - np.min(img))

def change_detection(image1, image2):
    image1_norm = normalize(image1)
    image2_norm = normalize(image2)

    diff = np.abs(image1_norm - image2_norm)
    return diff

#  the extract_geotiffs function here
def extract_geotiffs(zip_file_path):
    geotiff_files = []
    with zipfile.ZipFile(zip_file_path, 'r') as zf:
        zf.extractall()
        for root, dirs, files in os.walk(os.path.splitext(zip_file_path)[0] + '.SAFE'):
            print(f"Checking directory: {root}")
            for file in files:
                print(f"Checking file: {file}")
                if file.endswith('.tiff') and file.startswith('s1a'):
                    geotiff_path = os.path.join(root, file)
                    geotiff_files.append(geotiff_path)
                    print(f"Found {geotiff_path}")
    print(f"Found {len(geotiff_files)} GeoTIFF files in {zip_file_path}")
    return geotiff_files

# Process the downloaded images
image_paths = [f['path'] for f in successful_downloads.values() if 'path' in f]

# Extract GeoTIFF files from the downloaded ZIP archives
geotiff_paths = []
for image_path in image_paths:
    geotiff_paths.extend(extract_geotiffs(image_path))

try:
    # Read the first image
    with rasterio.open(geotiff_paths[0]) as src:
        band1 = src.read(1)
except Exception as e:
    print(f"Error while opening the first image: {e}")
    raise

try:
    # Read the second image
    with rasterio.open(geotiff_paths[1]) as src:
        band2 = src.read(1)
except Exception as e:
    print(f"Error while opening the second image: {e}")
    raise

# Perform change detection
change_map = change_detection(band1, band2)

# Save the change map to a GeoTIFF file
output_file = 'change_map.tif'
with rasterio.open(geotiff_paths[0]) as src:
    profile = src.profile
    profile.update(dtype=rasterio.float32)

    with rasterio.open(output_file, 'w', **profile) as dst:
        dst.write(change_map.astype(rasterio.float32), 1)

print(f"Change map saved to {output_file}")

