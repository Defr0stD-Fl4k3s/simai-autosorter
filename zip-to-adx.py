import os
import warnings
from pathlib import Path

# Make directories if not existing
os.makedirs("ZIP Imports", exist_ok=True)
os.makedirs("ADX Files", exist_ok=True)

zip_import_dir = "./ZIP Imports"
adx_output_dir = "./ADX Files"

if not os.listdir(zip_import_dir):
    warnings.warn("No imported ZIPs found!")
    exit(1001)