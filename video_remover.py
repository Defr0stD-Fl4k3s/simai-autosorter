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

# BG MP4 file name
mp4_name = "pv.mp4"

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

    #Unzip all .zip files found in 'ZIP Imports' folder
    for zip_file in os.listdir(zip_import_dir):
        print("\nFound zipfile '%s'. Unzipping file..." % str(zip_file))
        zip_file_dir = os.path.join(zip_import_dir, zip_file)
        zip_name = os.path.splitext(zip_file)[0]

        try:
            new_extraction_dir = os.path.join(clean_output_dir,zip_name)
            os.mkdir(new_extraction_dir)
        except:
            print("Error! Could not create new directory.")
        else:
            print("Successfully created new directory '%s'" % zip_name)

            with zipfile.ZipFile(zip_file_dir, "r") as extract_zip:
                # Extract all files from zip file
                try:
                    extract_zip.extractall(path=new_extraction_dir)
                except:
                    print("Unable to extract zip file!")
                else:
                    print("Extraction complete.")

    # Locate all unzipped directories
    for game_ver in os.listdir(clean_output_dir):
        game_ver_dir = os.path.join(clean_output_dir, game_ver)
        game_ver_dir2 = os.path.join(game_ver_dir, game_ver)
        print("\nFound game version folder '%s'." % game_ver)

        # Locate all song directories
        for song_folder in list(Path(game_ver_dir2).glob("*")):
            song_folder_name = str(song_folder).split("\\")[2]
            print("   Found song folder '%s'." % song_folder_name)

            video_file_dir = os.path.join(song_folder, mp4_name)
            if os.path.exists(video_file_dir):
                print("      Hit! Found video file in folder. Attempting deletion...")

                try:
                    os.remove(video_file_dir)
                except:
                    print("      Error! Unable to delete video file.")
                else:
                    print("      Successfully deleted video file!")

            else:
                print("      No video file found.")

        try:
            dir_to_be_zipped = os.path.join(clean_output_dir, game_ver)
            shutil.make_archive(dir_to_be_zipped, "zip", dir_to_be_zipped)
        except:
            print("         Failed to make archive '%s'!" % game_ver)
        else:
            print("         Successfully created archive '%s'." % game_ver)

            try:
                path = Path.cwd() / str(dir_to_be_zipped + ".zip")
                path.rename(path.with_suffix('.adx'))
            except:
                print("         Error! Unable to convert from ZIP to ADX format.")
            else:
                print("         Successfully converted from ZIP to ADX format.")

            # Remove original folder
            try:
                shutil.rmtree(game_ver_dir)
            except:
                print("         Unable to delete original folder '%s'!" % game_ver)
            else:
                print("         Successfully deleted original folder '%s'." % game_ver)