#!/bin/bash

# Loop through all files matching the pattern ????_modified.png
for file in ????_modified.png; do
    # Check if the file name matches the expected pattern
    if [[ $file =~ ^(.{4})_modified\.png$ ]]; then
        # Extract the prefix before "_modified"
        prefix=${BASH_REMATCH[1]}
        # Rename the file
        mv "$file" "${prefix}.png"
    fi
done

