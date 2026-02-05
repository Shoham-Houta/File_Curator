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

## Core Components

The file curator's logic is built around three main components that work together to automatically process files.

### 1. The Watcher (`watcher.py`)
This component uses the `watchdog` library to monitor a list of specified directories (e.g., `./data/downloads`, `./data/watch_folder`). When a file is created or modified, it triggers an event. To handle files that are still being written, it uses a debouncing mechanism to wait for a moment of inactivity before processing the file.

### 2. The Rule Engine (`rules.py`)
When the watcher identifies a stable file change, it passes the file's path and MIME type to the **Rule Engine**. The engine's job is to evaluate the file against a list of rules.

A rule consists of **conditions** and an **action**:
- **Conditions**: A dictionary defining the criteria a file must meet. For example: `{"MimeType": "application/pdf"}`.
- **Action**: A dictionary defining what to do if the conditions are met. For example: `{"type": "Move", "destination_path": "./data/documents"}`.

The engine iterates through the rules and, for the first rule that matches all its conditions, it executes the corresponding action.

#### Important Design Note: Preventing Loops
A critical aspect of the rule design is preventing infinite loops. For instance, a rule that moves PDF files to the `documents` folder will trigger a new file creation event in that folder. To prevent the engine from re-processing the same file, the rule must be specific enough to only act on files in the source location.

**Example of a safe rule:**
```json
{
    "rule_name": "Move PDF from Downloads to Documents",
    "conditions": {
        "MimeType": "application/pdf",
        "PathContains": "/data/downloads/"
    },
    "action": {
        "type": "Move",
        "destination_path": "./data/documents"
    }
}
```
The `"PathContains": "/data/downloads/"` condition ensures this rule only applies to files currently in the `downloads` directory, breaking the potential processing loop.

*(Note: Currently, rules are hardcoded in `rules.py`. They will be moved to a `config.yaml` file in a future update for easier user configuration.)*

### 3. The Actions (`actions.py`)
The actions are the "hands" of the application. They are a collection of simple Python functions that perform the actual file system operations (e.g., `move_file`, `delete_file`, `copy_file`). The Rule Engine calls these functions based on the `type` specified in a rule's action. Each action function is responsible for executing the file operation and returning a structured log dictionary indicating the status (`Success` or `Error`) and details of the operation.