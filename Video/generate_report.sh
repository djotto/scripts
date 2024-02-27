#!/bin/bash

# Check if the user has provided a path
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path>"
    exit 1
fi

SEARCH_PATH="$1"

# Start JSON array
echo "["

# Initialize the firstLine flag to true
firstLine=true

# Use find to get a list of files, then read each file line by line
while IFS= read -r file; do
    if [ "$firstLine" = true ]; then
        # No comma needed for the first line
        firstLine=false
    else
        # Add a comma separator for subsequent entries
        echo ","
    fi
    # Get file size
    filesize=$(stat -c%s "$file")
    # Use ffprobe to output information in JSON format, then add the "filesize" key with jq
    ffprobe -v quiet -print_format json -show_format -show_streams "$file" | \
    jq --arg filesize "$filesize" '. + {"filesize": ($filesize | tonumber)}'
done < <(find "$SEARCH_PATH" -type f -iregex ".*\.\(avi\|divx\|mkv\|mov\|mpg\|mp4\|webm\)$")

# Close JSON array
echo "]"
