#!/usr/bin/env bash

# Define the directories to be zipped
directories=("salutation" "salutation_marketing")

# Loop through each directory and create a zip file
for dir in "${directories[@]}"; do
    # Remove any existing zip file
    rm -f "${dir}.zip"

    # Create the zip file, excluding unnecessary files and directories
    zip -r "${dir}.zip" "${dir}" -x "${dir}/__pycache__/*" "${dir}/*.pyc" "${dir}/*.pyo" "${dir}/*.DS_Store"

    echo "Created ${dir}.zip"
done

# Print completion message
echo "Zip files created successfully."
