# Sentinel-1-SAR-for-change-detection
This code demonstrates how to download, preprocess, and perform change detection on Sentinel-1 images using Python. The script performs the following steps:

    Define the user's Copernicus Open Access Hub credentials.
    Define the area of interest (AOI) using a GeoJSON-formatted polygon and set the date range for the image search.
    Connect to the Copernicus Open Access Hub API.
    Search for Sentinel-1 images that match the AOI, date range, and other specified criteria (e.g., product type, orbit direction, and polarization mode).
    Download the images that match the search criteria.
    Define a change detection function that normalizes the input images and computes the absolute difference between them.
    Extract GeoTIFF files from the downloaded images.
    Preprocess the Sentinel-1 images using radiometric calibration and speckle filtering (using the SNAP Python library).
    Perform change detection on the preprocessed images.
    Save the resulting change map as a GeoTIFF file.

The code has been organized into functions to perform specific tasks, such as normalizing images, performing change detection, extracting GeoTIFF files, and preprocessing SAR images. The script relies on several external libraries, including rasterio, sentinelsat, and snappy, to handle various processing tasks.
