# File Curator

## Project Description
This is an AI-powered file curator that intelligently organizes files based on their content and context. It will monitor designated folders, analyze new or modified files using machine learning, and apply user-defined rules to automate file organization. The project includes a web dashboard for configuration and monitoring.

## Installation

1. **Create and activate the conda environment:**
```
conda env create -f environment.yml
conda activate file_curator
```
2. **Install the `python-magic` dependency:**
* **On Windows:**
    ```conda install -c conda-forge python-magic-bin```

* **On Linux or MacOS (including Apple Silicon):**
```conda install -c conda-forge python-magic```