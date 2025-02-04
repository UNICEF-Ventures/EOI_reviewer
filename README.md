# Application Review System

A Flask-based web application for reviewing and evaluating applications with Excel file support.

## Prerequisites

- Python 3.7 or higher
- pip

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

## Project Structure

```
.
├── app.py                  # Main Flask application
├── templates/             
│   └── review.html        # HTML template for the review page
├── uploads/               # Directory for uploaded files (created automatically)
├── requirements.txt       # Python dependencies
└── run.sh                # Shell script to run the application
```

## Configuration

The application uses the following configuration:
- Upload folder: `uploads/` (created automatically). It downloads the reviewed excel file to this folder..

## Running the Application
```info
Before running the application, make sure to set your name as evaluator in the app.py file (line 24).
```
1. Using the shell script:
```bash
chmod +x run.sh  # Make the script executable (Unix-based systems only)
./run.sh
```

2. Or run directly with Python:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Start the application
2. Upload an Excel file containing applications
3. Review applications one by one
4. Add evaluations and comments
5. Navigate between applications using Previous/Next buttons
6. Export reviews when finished

## Requirements.txt

Create a `requirements.txt` file with the following dependencies:
```text
Flask==2.0.1
pandas==1.3.3
openpyxl==3.0.9
```

## Run Script

Create a `run.sh` file with the following content:
```bash
#!/bin/bash
source venv/bin/activate
python app.py
```

## License