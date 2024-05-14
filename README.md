# PowerShell File Handling Script

## Overview
This PowerShell script is designed to automate the download of large files from IBM Cloud Object Storage and to split them into manageable chunks. It addresses the challenges associated with managing large datasets, making the process more efficient and reliable.

## Purpose
The script serves to:
- **Download** large files directly to a local machine from a specified URL.
- **Split** the downloaded files into predefined chunk sizes for easier data management.

## Requirements
- **PowerShell 5.1+**: Ensure compatibility with modern PowerShell features.
- **Network Access**: Required for downloading files.
- **Adequate Storage**: Sufficient disk space on the local system is necessary for storing both the entire file and its chunks.
- **Permissions**: Appropriate read/write permissions are needed for operations on the filesystem.

## Features
- **Efficient File Downloading**: Uses `Invoke-WebRequest` for robust file transfers.
- **Dynamic File Splitting**: Automatically splits the downloaded file into segments, saving each as a separate file.
- **Error Management**: Basic error handling is implemented to address potential issues during download or file manipulation.

## Configuration
Modify the following script parameters as needed:
- **`$url`**: The URL of the file to download.
- **`$outputFilePath`**: Local path where the downloaded file will be stored.
- **`$chunkSize`**: Size of each file segment after splitting.

## Workflow
1. **Initialize Variables**: Configure the script with the URL, output path, and chunk size.
2. **Download File**: Execute the file download to the specified local path.
3. **Split File**: Post-download, the file is split into chunks as configured.
4. **Clean-Up and Verification**: Perform any necessary clean-up operations and verify the integrity of the file and its chunks.

## Usage
Ensure all configurations are set correctly before running the script. Execute the script within a PowerShell environment that has the necessary permissions.

