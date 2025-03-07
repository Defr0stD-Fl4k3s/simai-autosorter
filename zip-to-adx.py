import os
import warnings
import zipfile
from pathlib import Path

# Make directories if not existing
os.makedirs("ZIP Imports", exist_ok=True)
os.makedirs("ADX Files", exist_ok=True)

# Directory variables
zip_import_dir = "./ZIP Imports"
adx_output_dir = "./ADX Files"

# Check if 'ZIP Imports' folder is empty
if not os.listdir(zip_import_dir):
    warnings.warn("No imported ZIPs found!")
    exit(1001)

# Unzip all .zip files found in 'ZIP Imports' folder
for zip_file in os.listdir(zip_import_dir):
    # print(zip_file)
    zip_file_dir = os.path.join(zip_import_dir, zip_file)
    with zipfile.ZipFile(zip_file_dir, "r") as extract_zip:
        extract_zip.extractall(path=adx_output_dir)