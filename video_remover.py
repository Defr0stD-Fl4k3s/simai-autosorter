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

    # Unzip all .zip files found in 'ZIP Imports' folder
    for zip_file in os.listdir(zip_import_dir):
        print("\nFound zipfile '%s'. Unzipping file..." % str(zip_file))
        zip_file_dir = os.path.join(zip_import_dir, zip_file)

        with zipfile.ZipFile(zip_file_dir, "r") as extract_zip:
            # Extract all files from zip file
            try:
                extract_zip.extractall(path=clean_output_dir)
            except:
                print("Unable to extract zip file!")
            else:
                print("Extraction complete.")

    # Locate all unzipped directories
    for game_ver in os.listdir(clean_output_dir):
        game_ver_dir = os.path.join(clean_output_dir, game_ver)
        print("\nFound game version folder '%s'." % game_ver)

        # Locate all song directories
        for song_folder in list(Path(game_ver_dir).glob("*_*")):
            song_folder_name = str(song_folder).split("\\")[2]
            print("   Found song folder '%s'." % song_folder_name)

