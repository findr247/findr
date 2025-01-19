#!/bin/bash

# Install pip if not installed
if ! command -v pip &> /dev/null
then
    echo "pip not found. Installing pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3
fi

# Install Python dependencies
echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

python3 -m spacy download en_core_web_sm
# Notify completion
echo "Build process completed."
