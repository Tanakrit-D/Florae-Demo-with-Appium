#!/bin/bash

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

source_dir="reporting/allure-results"
source_dir_single="reporting/allure-single-page"
dest_dir="reporting/historical/$timestamp/allure-results"
dest_dir_single="reporting/historical/$timestamp/allure-single-page"

# Check if the source directory exists
if [ ! -d "$source_dir" ]; then
    echo "Error: Source directory $source_dir does not exist."
    exit 1
fi

# Check if the source directory is empty
if [ -z "$(ls -A "$source_dir")" ]; then
    echo "The source directory $source_dir is empty. No files to move."
fi

# Check if the single source directory is empty
if [ -z "$(ls -A "$source_dir_single")" ]; then
    echo "The single source directory $source_dir is empty. No files to move."
fi

# Create the destination directory
mkdir -p "$dest_dir"
mkdir -p "$dest_dir_single"

# Move the contents of the source directory to the destination
mv "$source_dir"/* "$dest_dir"
mv "$source_dir_single"/* "$dest_dir_single"

# Print a message indicating the operation is complete
echo "Contents moved from $source_dir to $dest_dir"
echo "Contents moved from $source_dir_single to $dest_dir_single"