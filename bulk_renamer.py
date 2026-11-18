import os      # work with files, folders and paths
import shutil  # copy files (used for the backup)
from datetime import datetime  # used to name the backup folder

# The default folder sits next to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FOLDER = os.path.join(SCRIPT_DIR, "sample_files")