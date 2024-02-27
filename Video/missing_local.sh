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

echo "Files that are available on the remote server, but not available on the local server"

# Extract filename fragments and check for file existence
jq -r '.[].format.filename' "$JSON_FILE" | while read -r filename; do
    # Extract the fragment using grep; if no fragment is found, skip the filename
    fragment=$(echo "$filename" | grep -oE '\.S[0-9]{2,4}E[0-9]{1,2}\.')
    if [ -z "$fragment" ]; then
        continue
    fi

    # Use find with -iregex to search for files matching the fragment and video file extensions in the CWD or below
    regex=".*${fragment}.*\.\(mkv\|mpg\|divx\|mp4\|avi\|mov\|webm\)$"
    match=$(find . -type f -iregex "$regex" -print -quit)

    if [ -z "$match" ]; then
        # No matching files found, print the message with the remote filename
        echo $filename
    fi
done

