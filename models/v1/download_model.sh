#!/bin/bash

# Array of names
names=('hi' 'as' 'bn' 'brx' 'gu' 'kn' 'ml' 'mni' 'mr' 'or' 'pa' 'raj' 'ta' 'te')
# names = ( 'hi' 'as')

# Base URL
base_url="https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/"

# Loop through each name
for name in "${names[@]}"; do
    # Construct the full URL
    url="${base_url}${name}.zip"
    
    # Download the file
    wget $url
    
    # Unzip the file
    unzip "${name}.zip"
    
    # Remove the zip file
    rm "${name}.zip"
done
