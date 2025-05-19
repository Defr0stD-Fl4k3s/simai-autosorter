import os
import shutil
import warnings
import zipfile
from pathlib import Path

# Map data variable
song_map_name = "maidata.txt"

# Genre folder name list
genre_folder_names = [
    r"01 - POPSアニメ",
    r"02 - niconicoボーカロイド",
    r"03 - 東方Project",
    r"04 - ゲームバラエティ",
    r"05 - maimai",
    r"06 - オンゲキCHUNITHM",
    r"07 - 宴会場(utage)"
]

# Key-Value table for ADX file names
adx_file_names = {
    "maimai": "SD-01 maimai",
    "maimai PLUS": "SD-02 maimai PLUS",
    "maimai GreeN": "SD-03 GreeN",
    "maimai GreeN PLUS": "SD-04 GreeN PLUS",
    "maimai ORANGE": "SD-05 ORANGE",
    "maimai ORANGE PLUS": "SD-06 ORANGE PLUS",
    "maimai PiNK": "SD-07 PiNK",
    "maimai PiNK PLUS": "SD-08 PiNK PLUS",
    "maimai MURASAKi": "SD-09 MURASAKi",
    "maimai MURASAKi PLUS": "SD-10 MURASAKi PLUS",
    "maimai MiLK": "SD-11 MiLK",
    "maimai MiLK PLUS": "SD-12 MiLK PLUS",
    "maimai FiNALE": "SD-13 FiNALE",
    "maimai DX": "DX-01 DX ",
    "maimai DX PLUS": "DX-02 DX PLUS ",
    "maimai DX Splash": "DX-03 DX Splash",
    "maimai DX Splash PLUS": "DX-04 DX Splash PLUS",
    "maimai DX UNiVERSE": "DX-05 DX UNiVERSE",
    "maimai DX UNiVERSE PLUS": "DX-06 DX UNiVERSE PLUS",
    "maimai DX FESTiVAL": "DX-07 DX FESTiVAL",
    "maimai DX FESTiVAL PLUS": "DX-08 DX FESTiVAL PLUS",
    "maimai DX BUDDiES": "DX-09 DX BUDDiES",
    "maimai DX BUDDiES PLUS": "DX-10 DX BUDDiES PLUS",
    "maimai DX PRiSM": "DX-11 DX PRiSM",
    "maimai DX PRiSM PLUS": "DX-12 DX PRiSM PLUS"
}

# Make directories if not existing
os.makedirs("ZIP Imports", exist_ok=True)
os.makedirs("ADX Files", exist_ok=True)

# Directory variables
zip_import_dir = ".\\ZIP Imports"
adx_output_dir = ".\\ADX Files"

# Check if 'ZIP Imports' folder is empty
if not os.listdir(zip_import_dir):
    warnings.warn("No imported ZIPs found!")
    exit(1001)

# Clear all contents in 'ADX Files' directory
if os.path.exists(adx_output_dir):
    try:
        if os.listdir(adx_output_dir):
            print("\nFiles found in 'ADX Files'. Deleting files...")
            try:
                for file in os.listdir(adx_output_dir):
                    file_dir = os.path.join(adx_output_dir, file)
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
            print("No files found in 'ADX Files' folder.")
    except:
        print("Something went wrong! Unable to clear folder.")
    else:
        print("Successfully cleared 'ADX Files'.")

    # Unzip all .zip files found in 'ZIP Imports' folder
    for zip_file in os.listdir(zip_import_dir):
        print("\nFound zipfile '%s'. Unzipping file..." % str(zip_file))
        zip_file_dir = os.path.join(zip_import_dir, zip_file)

        with zipfile.ZipFile(zip_file_dir, "r") as extract_zip:
            # Extract all files from zip file
            try:
                extract_zip.extractall(path=adx_output_dir)
            except:
                print("Unable to extract zip file!")
            else:
                print("Extraction complete.")

    # Locate all unzipped directories
    for game_ver in os.listdir(adx_output_dir):
        print("\nFound game version folder '%s'." % game_ver)
        game_ver_dir = os.path.join(adx_output_dir, game_ver)

        # Fill folder with genre folders
        for genre_name in genre_folder_names:
            new_genre_folder_dir = os.path.join(game_ver_dir, genre_name)
            try:
                os.makedirs(new_genre_folder_dir)
            except:
                print("   Error creating folder '%s'!" % genre_name)
            else:
                print("   Successfully created directory '%s'." % genre_name)

        # Locate all song directories
        for song_folder in list(Path(game_ver_dir).glob("*_*")):
            print("   Found song folder '%s'." % str(song_folder).split("\\")[2])
            song_folder_name = str(song_folder).split("\\")[2]
            song_file_dir = os.path.join(song_folder, song_map_name)
            print("      Found song file in %s." % song_file_dir)

            # Read lines in song map file
            try:
                with open(song_file_dir, "r", encoding="utf8") as song_file:
                    lines = song_file.readlines()

                    # Isolate each line as separate text
                    for line in lines:
                        text = line.strip()

                        # Locate genre among the texts
                        if "&genre=" in text:
                            # Extract genre label
                            genre_text = text.split("=")[1]
                            print("      Extracted genre '%s' from file." % genre_text)
            except:
                print("      Unable to read file!")
            else:
                print("      Successfully read file.")

            # Identify new directory where song folder is moved to
            for genre_title in genre_folder_names:
                if genre_text in genre_title:
                    # Create new song folder directory
                    new_song_folder_dir = os.path.join(game_ver_dir, genre_title, song_folder_name)
                    try:
                        # Move folder to new directory
                        shutil.move(song_folder, new_song_folder_dir)
                    except:
                        print("      Unable to move from '%s' to '%s'!" % (song_folder, new_song_folder_dir))
                    else:
                        print("      Successfully moved '%s' to '%s'!" % (song_folder, new_song_folder_dir))

        # Check name against list of allowed
        new_zip_name = ''

        for zip_name in adx_file_names:
            if game_ver in zip_name:
                new_zip_name = adx_file_names.get(game_ver)
                # Create zip file for sorted folder
                try:
                    shutil.make_archive(os.path.join(adx_output_dir, new_zip_name), "zip", os.path.join(adx_output_dir, game_ver))
                except:
                    print("         Failed to make archive '%s'!" % new_zip_name)
                else:
                    print("         Successfully created archive '%s'." % new_zip_name)

                    # Remove original folder
                    try:
                        shutil.rmtree(game_ver_dir)
                    except:
                        print("         Unable to delete original folder '%s'!" % game_ver)
                    else:
                        print("         Successfully deleted original folder '%s'." % game_ver)

        # Change '.zip' extension to '.adx'
        try:
            path = Path.cwd() / Path(adx_output_dir) / str(new_zip_name + ".zip")
            new_file_path = path.with_suffix(".adx")
            path.rename(new_file_path)
        except:
            print("Unable to change file extension for '%s' to '.adx'!" % path)
        else:
            print("Successfully changed file extension.\nSuccessfully created")