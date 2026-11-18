# BulkFileRenaming
Simple Automation Script

Automates a repetitive task: renaming many files in a folder at once.
 
What it does:
    
A Python automation script that renames many files in a folder at once. Automates a repetitive task: renaming many files in a folder at once.

What It Does
    - Takes every file in a folder (sorted A-Z)
    - Renames them with a prefix and a number, e.g. vacation_001.jpg
    - Keeps each file's original extension (in lowercase)
    - Shows a PREVIEW first and asks for confirmation
    - Can make a BACKUP copy of the files before renaming

Before

holiday photo.png
IMG_4821.JPG
notes (final).txt
report v2.pdf
Screenshot 2026-01-05.PNG

After (prefix vacation_)

vacation_001.png
vacation_002.jpg
vacation_003.txt
vacation_004.pdf
vacation_005.png

Features
Preview of every change before anything is renamed
Confirmation (y/n) before renaming
Optional backup copy of all files first (using shutil)
Keeps file extensions and converts them to lowercase (.JPG becomes .jpg)
Custom prefix and starting number
Skips sub-folders and hidden files (such as .DS_Store)
Two-pass renaming, so new names never overwrite files that haven't been renamed yet
Built-in option to create 5 sample files for testing
Input validation and error handling

Requirements
Python 3.8 or newer
No extra libraries. It uses only built-in modules: os, shutil, datetime
How to Run
Download or clone this repository.
Open a terminal in the project folder.
Run:

Mac / Linux

python3 bulk_renamer.py

Windows

python bulk_renamer.py
How to Use
===== BULK FILE RENAMER =====
Current folder: .../sample_files
1. Create 5 sample files (for testing)
2. Change folder
3. Rename files in this folder
4. Exit
Option 1 creates 5 messy sample files in a sample_files folder, so you can try the script safely.
Option 2 lets you choose any other folder (type the path, or drag the folder into the terminal window).
Option 3 asks for a prefix and a starting number, shows a preview, then renames the files after you confirm.
Option 4 exits.
How to Test (5 Sample Records)
Run the script and choose 1 to create the 5 sample files.
Choose 3, enter the prefix vacation_, and press Enter to start from 1.
Check the preview, type y to rename, and y to make a backup.
Open the sample_files folder. You should see vacation_001 to vacation_005 and a backup_... folder with the originals.

Error Handling
Problem	How it is handled
Folder does not exist	Shows a message and asks again
Empty prefix	Asks again
Prefix contains illegal characters (/ \ : * ? " < > |)	Asks again
Starting number is not a whole number	Asks again
Answer is not y or n	Asks again
Folder has no files	Shows a message and returns to the menu
File cannot be renamed or backed up	Shows a clear error message instead of crashing

Python Concepts Used
The os module: listing, joining, and renaming files
The shutil module: copying files for the backup
Functions
Loops and menus
try / except error handling
f-strings and string methods
