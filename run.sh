#!/bin/bash

# Check if the executable exists
if [ ! -f "dist/app" ]; then
    echo "Building application..."
    pip install -r requirements.txt
    pyinstaller --add-data "templates:templates" --onefile app.py
fi

# Run the executable
./dist/app &
sleep 2
open http://localhost:5000