import os      # work with files, folders and paths
import shutil  # copy files (used for the backup)
from datetime import datetime  # used to name the backup folder

# The default folder sits next to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FOLDER = os.path.join(SCRIPT_DIR, "sample_files")

# 5 messy file names used to test the script
SAMPLE_FILE_NAMES = [
    "IMG_4821.JPG",
    "holiday photo.png",
    "notes (final).txt",
    "report v2.pdf",
    "Screenshot 2026-01-05.PNG",
]
 
# Characters that are not allowed in file names
INVALID_CHARS = '/\\:*?"<>|'

 #Create sample files for testing
def create_sample_files(folder):
    """Create the 5 messy sample files so you can test the renamer."""
    try:
        os.makedirs(folder, exist_ok=True)  # create the folder if missing
        for name in SAMPLE_FILE_NAMES:
            with open(os.path.join(folder, name), "w", encoding="utf-8") as file:
                file.write(f"Sample file: {name}\n")
        print(f"Created {len(SAMPLE_FILE_NAMES)} sample files in:\n{folder}")
    except OSError as error:
        print(f"Could not create sample files: {error}")


#List the files we want to rename
def list_files(folder):
    """Return a sorted list of file names (skips folders and hidden files)."""
    files = []
    for name in sorted(os.listdir(folder), key=str.lower):
        path = os.path.join(folder, name)
        # Keep real files only; skip folders and hidden files like .DS_Store
        if os.path.isfile(path) and not name.startswith("."):
            files.append(name)
    return files

def build_new_names(files, prefix, start):
    """Return a list of new names in the same order as 'files'."""
    # Use at least 3 digits (001) or more if there are lots of files
    width = max(3, len(str(start + len(files) - 1)))
    new_names = []
    for number, old_name in enumerate(files, start=start):
        _, extension = os.path.splitext(old_name)  # e.g. ".JPG"
        new_names.append(f"{prefix}{str(number).zfill(width)}{extension.lower()}")
    return new_names



def backup_files(folder, files):
    """Copy all files into a new backup folder. Returns the backup path."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(folder, f"backup_{stamp}")
    os.makedirs(backup_folder)
    for name in files:
        # copy2 copies the file AND keeps its dates
        shutil.copy2(os.path.join(folder, name), os.path.join(backup_folder, name))
    return backup_folder