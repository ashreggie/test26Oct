# Bibliometric Data Analyzer

This Python script provides a web-based interface for analyzing bibliometric data from Excel files. It uses Gradio to create a simple UI for file upload and download. The code is adapted from a Jupyter notebook and runs on Windows, Mac, and Linux environments.

## Description

The Bibliometric Data Analyzer processes Excel files containing academic publication data. It performs the following operations:

1. Reads an Excel file with bibliometric data.
2. Processes and cleans the data, including:
   - Handling different column structures based on the presence of "A-Journal Papers".
   - Renaming and reorganizing H-index columns.
   - Cleaning up the PromoYear column.
   - Splitting Scopus IDs if they contain multiple values.
3. Filters out rows with NaN values in the Name column.
4. Saves the processed data to a new Excel file.

## Components

- `analyze_bibliometric(file)`: The main function that processes the uploaded Excel file.
- Gradio interface: Provides a web UI for file upload and download.

## Requirements

- Python 3.x
- Required libraries:
  - gradio
  - numpy
  - pandas
  - openpyxl (for Excel file handling)

## Installation

1. Clone this repository or download the script.
2. Install the required libraries:

```
pip install gradio numpy pandas openpyxl
```

## How to Run

1. Open a terminal or command prompt.
2. Navigate to the directory containing the script.
3. Run the script:

```
python app.py
```

4. Open a web browser and go to the URL provided in the terminal (usually `http://127.0.0.1:7860`).
5. Use the web interface to upload your bibliometric Excel file.
6. The processed file will be available for download once the analysis is complete.

## Notes

- The input Excel file should have the bibliometric data in the second sheet (index 1).
- The script expects specific column names and structures. Ensure your input file matches the expected format.
- The output will be saved as "filtered_bibliometric_analysis.xlsx" in the same directory as the script.
