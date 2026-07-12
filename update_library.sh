#!/bin/bash

echo "🔄 Step 1: Fetching ONLY new or newly edited files from Google Drive..."
# The --update flag tells Rclone to skip local files that are newer than Google Drive
rclone copy gdrive: . --drive-root-folder-id 1V2tfnU3cgZRtqXXpeYSVZbj2piTsb7yU --update --progress

echo "📝 Step 2: Rebuilding the clean collapsible navigation index..."
python3 build_index.py

echo "🏠 Step 3: Scanning and injecting mobile Home buttons..."
python3 inject_home.py

echo "🏁 Update complete!"
