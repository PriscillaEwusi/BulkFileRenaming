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

# The actual renaming
# We rename in TWO passes. If we renamed straight to the final names, a new name could clash with a file that hasn't been renamed yet and overwrite it. Temporary names avoid that.

def rename_files(folder, files, new_names):
    """Rename the files. Returns True if everything worked."""
    try:
        # Pass 1: old name -> temporary name
        temp_names = []
        for index, old_name in enumerate(files):
            temp_name = f"__temp_{index}__"
            os.rename(os.path.join(folder, old_name), os.path.join(folder, temp_name))
            temp_names.append(temp_name)
 
        # Pass 2: temporary name -> final new name
        for temp_name, new_name in zip(temp_names, new_names):
            os.rename(os.path.join(folder, temp_name), os.path.join(folder, new_name))
        return True
    except OSError as error:
        print(f"Something went wrong while renaming: {error}")
        print("If you made a backup, your original files are safe in it.")
        return False

# Input helpers (handle invalid input)
def ask_yes_no(question):
    """Keep asking until the user answers y or n."""
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("Please type y or n.")
 
 
def get_prefix():
    """Ask for a prefix such as 'vacation_' and reject illegal characters."""
    while True:
        prefix = input("Enter a prefix for the new names (e.g. vacation_): ").strip()
        if not prefix:
            print("The prefix cannot be empty.")
        elif any(char in INVALID_CHARS for char in prefix):
            print(f"The prefix cannot contain any of these: {INVALID_CHARS}")
        else:
            return prefix
 
 
def get_start_number():
    """Ask which number to start counting from (default 1)."""
    while True:
        text = input("Start numbering from (press Enter for 1): ").strip()
        if text == "":
            return 1
        if text.isdigit() and int(text) >= 0:
            return int(text)
        print("Please enter a whole number like 1 or 10.")
 
 
def get_folder():
    """Ask for a folder path and check that it exists."""
    while True:
        text = input("Enter the full folder path: ").strip()
        # Dragging a folder into Terminal adds quotes or backslashes; clean them
        text = text.strip("'\"").replace("\\ ", " ")
        path = os.path.expanduser(text)  # turns ~ into your home folder
        if os.path.isdir(path):
            return path
        print("That folder does not exist. Please try again.")

# Put it all together for one rename job
def rename_workflow(folder):
    """Preview, confirm, optionally back up, then rename."""
    if not os.path.isdir(folder):
        print("The folder does not exist yet. Create sample files or change folder first.")
        return
 
    files = list_files(folder)
    if not files:
        print("No files found in this folder.")
        return
 
    prefix = get_prefix()
    start = get_start_number()
    new_names = build_new_names(files, prefix, start)
 
    # Show the preview so the user can check before anything changes
    print(f"\nPreview ({len(files)} files):")
    for old_name, new_name in zip(files, new_names):
        print(f"  {old_name:<30} ->  {new_name}")
 
    if not ask_yes_no("\nRename these files?"):
        print("Cancelled. No files were changed.")
        return
 
    if ask_yes_no("Make a backup copy first? (recommended)"):
        try:
            backup_folder = backup_files(folder, files)
            print(f"Backup saved in: {backup_folder}")
        except OSError as error:
            print(f"Backup failed ({error}). Nothing was renamed.")
            return
 
    if rename_files(folder, files, new_names):
        print(f"Done! Renamed {len(files)} files.")

# Main menu loop
def main():
    """Run the menu until the user exits."""
    folder = DEFAULT_FOLDER
    print("Welcome to the DTEN Bulk File Renamer!")
 
    while True:
        print("\n===== BULK FILE RENAMER =====")
        print(f"Current folder: {folder}")
        print("1. Create 5 sample files (for testing)")
        print("2. Change folder")
        print("3. Rename files in this folder")
        print("4. Exit")
 
        choice = input("Choose an option (1-4): ").strip()
 
        if choice == "1":
            create_sample_files(folder)
        elif choice == "2":
            folder = get_folder()
        elif choice == "3":
            rename_workflow(folder)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")
 
 
# Run main() only when this file is run directly
if __name__ == "__main__":
    main()