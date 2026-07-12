#!/bin/bash
# Ensure you are on the develop branch working track
git checkout develop

# Pull any raw updates down from Google Drive using the timestamp safety flag
rclone copy gdrive: . --drive-root-folder-id 1V2tfnU3cgZRtqXXpeYSVZbj2piTsb7yU --update --progress

# Run your manual index compilation and button injection scripts
python3 generate_index.py
python3 inject_home.py
