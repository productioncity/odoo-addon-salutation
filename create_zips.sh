#!/usr/bin/env bash

# Define the directories to be zipped
directories=("salutation" "salutation_marketing")

# Exclude patterns
exclude_patterns=(
    "*/__pycache__/*"
    "*.pyc"
    "*.pyo"
    "*.DS_Store"
    "*.log"
    "*.tmp"
)

# Loop through each directory and create a zip file
for dir in "${directories[@]}"; do
    # Remove any existing zip file
    rm -f "${dir}.zip"

    # Build the exclusion arguments for the zip command
    exclusion_args=()
    for pattern in "${exclude_patterns[@]}"; do
        exclusion_args+=(-x "${pattern}")
    done

    # Create the zip file, excluding unnecessary files and directories
    zip -r "${dir}.zip" "${dir}" "${exclusion_args[@]}"

    echo "Created ${dir}.zip"
done

# Print completion message
echo "Zip files created successfully."
