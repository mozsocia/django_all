#!/bin/bash

# Define the word to be replaced and the replacement
old_word="brand"
new_word="product_slider"

# Loop through all files in the current directory
for file in *; do
    # Check if the file name contains the word to be replaced
    if [[ "$file" == *"$old_word"* ]]; then
        # Replace the word in the file name
        new_file="${file//$old_word/$new_word}"
        # Rename the file
        mv "$file" "$new_file"
        echo "Renamed $file to $new_file"
    fi
done
