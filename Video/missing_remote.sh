#!/bin/bash

# Check if a file path was provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_json_file>"
    exit 1
fi

# The path to the JSON file provided as the first argument
JSON_FILE="$1"

# Check if the JSON file exists
if [ ! -f "$JSON_FILE" ]; then
    echo "JSON file not found: $JSON_FILE"
    exit 1
fi

echo "Files that are available on the local server, but not available on the remote server"

# Extract all filenames from the JSON file into an array
mapfile -t json_filenames < <(jq -r '.[].format.filename' "$JSON_FILE" | sed 's/.*\/\([^\/]*\)$/\1/')

# Use find to get all local video files
while IFS= read -r file; do
    found=false
    local_filename=$(basename "$file")
    # Check if the local file's name is in the array of JSON filenames
    for json_filename in "${json_filenames[@]}"; do
        if [[ "$local_filename" == "$json_filename" ]]; then
            found=true
            break
        fi
    done
    # If the file was not found in the JSON, print it
    if [ "$found" = false ]; then
        echo "$file"
    fi
done < <(find . -type f -iregex ".*\.\(mkv\|mpg\|divx\|mp4\|avi\|mov\|webm\)$")

