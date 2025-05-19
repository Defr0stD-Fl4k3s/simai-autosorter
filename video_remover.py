import os
import shutil
import warnings
import zipfile
from pathlib import Path

# Make directories if not existing
os.makedirs("ZIP Imports", exist_ok=True)
os.makedirs("Video_Free", exist_ok=True)

# Directory variables
zip_import_dir = ".\\ZIP Imports"
clean_output_dir = ".\\Video_Free"

# Check if 'ZIP Imports' folder is empty
if not os.listdir(zip_import_dir):
    warnings.warn("No imported ZIPs found!")
    exit(1001)

# Clear all contents in 'Video-Free Files' directory
if os.path.exists(clean_output_dir):
    try:
        if os.listdir(clean_output_dir):
            print("\nFiles found in 'Video-Free Files' folder. Deleting files...")
            try:
                for file in os.listdir(clean_output_dir):
                    file_dir = os.path.join(clean_output_dir, file)
                    if os.path.isdir(file_dir):
                        shutil.rmtree(file_dir)
                    elif os.path.isfile(file_dir):
                        os.remove(file_dir)
                    elif zipfile.is_zipfile(file_dir):
                        os.remove(file_dir)
            except:
                print("Something went wrong! File '%s' wasn't removed successfully." % file)
            else:
                print("File '%s' was removed successfully." % file)
        else:
            print("No files found in the 'Video-Free Files' folder.")
    except:
        print("Something went wrong! Unable to clear folder.")
    else:
        print("Successfully cleared contents of 'Video-Free Files' folder.")