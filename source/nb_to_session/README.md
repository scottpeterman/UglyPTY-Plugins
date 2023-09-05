
# Netbox to UglyPTY YAML Exporter

## Overview

This PyQt6-based application is designed to export Netbox site and device data to generate a YAML file compatible with UglyPTY's session file format. This enables you to quickly get a populated list of sites and devices for SSH management.

## Requirements

- Python 3.9 or higher (for UglyPTY)
- PyQt6
- pynetbox

You can install PyQt6 and pynetbox using pip:

```bash
pip install PyQt6 pynetbox
```

## How to Use

1. Run the PyQt6 application.
2. A window will appear containing two text input fields and a "Download" button.
   - First text field: Enter your Netbox API Token.
   - Second text field: Enter your Netbox URL.
3. Click the "Download" button to begin the process.
4. A progress bar will indicate the status of the operation.

## How It Works

### GUI Layout

The application uses PyQt6 to create a simple graphical interface that includes:

- Two `QLineEdit` widgets for taking Netbox API Token and Netbox URL as input.
- One `QPushButton` to trigger the export/download process.
- A `QProgressBar` to indicate the progress.

### Data Processing

Here's a brief rundown of how the data is processed:

1. The Netbox API is accessed using the `pynetbox` library.
2. All the sites available in the Netbox instance are fetched.
3. For each site, devices are fetched and their attributes are collected.
4. The attributes are mapped to UglyPTY's session file format.
5. The progress bar is updated based on the number of sites processed.

### YAML File Generation

- A list of dictionaries, each representing a site and its devices, is generated.
- The list is then written to an output YAML file using Python's `yaml` library.

## Author

Scott Peterman

---

