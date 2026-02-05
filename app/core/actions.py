import os
import shutil
import datetime


TIMESTAMP_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def create_directory(dest_path: str) -> dict:
    """Ensures a directory exists at the given path, creating it if necessary.

    This function is idempotent. If the directory already exists, it does nothing
    but still returns a success status.

    Args:
        dest_path (str): The absolute path of the directory to create.

    Returns:
        dict: A log dictionary detailing the action's outcome.
    """
    # Efficiency: O(N) where N is the number of new directories to create. O(1) if it exists.
    if os.path.exists(dest_path):
        message = f"Directory: {dest_path} already exists."
    else:
        os.makedirs(dest_path, exist_ok=True)
        message = f"Directory: {dest_path} was created."
    return {
        "action_type": "Create",
        "status": "Success",
        "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
        "destination_path": dest_path,
        "message": message,
    }


def delete_file(dest_path: str) -> dict:
    """Deletes a file from the specified path.

    Args:
        dest_path (str): The absolute path to the file to be deleted.

    Returns:
        dict: A log dictionary detailing the action's outcome.
    """
    # Efficiency: O(1) in most cases, as it's a direct syscall to the filesystem.
    try:
        os.remove(dest_path)
        return {
            "action_type": "Delete",
            "status": "Success",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "destination_path": dest_path,
            "message": f"{dest_path} was deleted.",
        }
    except FileNotFoundError:
        return {
            "action_type": "Delete",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "destination_path": dest_path,
            "message": f"{dest_path} was not found.",
        }
    except PermissionError:
        return {
            "action_type": "Delete",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "destination_path": dest_path,
            "message": f"No permission to delete {dest_path}.",
        }
    except IsADirectoryError:
        return {
            "action_type": "Delete",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "destination_path": dest_path,
            "message": f"{dest_path} is a directory.",
        }
    except Exception:
        return {
            "action_type": "Delete",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "destination_path": dest_path,
            "message": f"Something went wrong while deleting {dest_path}.",
        }


def move_file(src_path: str, dest_path: str, override: bool = False) -> dict:
    """Moves a file from a source path to a destination path.

    Handles overwriting the destination file if `override` is True. It first
    attempts a fast atomic `os.rename`, but falls back to a copy-and-delete
    operation if the destination is on a different filesystem.

    Args:
        src_path (str): The path of the file to move.
        dest_path (str): The path where the file will be moved.
        override (bool, optional): If True, overwrites the destination file if it
            exists. Defaults to False.

    Returns:
        dict: A log dictionary detailing the action's outcome.
    """
    # Efficiency (Time): Best case O(1) for same-filesystem rename.
    # Worst case O(S) where S is the file size, for cross-filesystem move.
    # Efficiency (Space): Best O(1), Worst O(S) during the copy operation.
    create_directory(os.path.dirname(dest_path))

    if not override and os.path.exists(dest_path):
        return {
            "action_type": "Move",
            "status": "Fail",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"File already exists and override is set to False.",
        }
    try:
        if override and os.path.isfile(dest_path):
            os.remove(dest_path)

        shutil.move(src_path, dest_path)
        return {
            "action_type": "Move",
            "status": "Success",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"Moved: {src_path} -> {dest_path}",
        }
    except FileNotFoundError:
        return {
            "action_type": "Move",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"{src_path} was not found.",
        }
    except PermissionError:
        return {
            "action_type": "Move",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"No permission to move {src_path} -> {dest_path}.",
        }
    except Exception:
        return {
            "action_type": "Move",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"Something went wrong while moving {src_path} -> {dest_path}.",
        }


def copy_file(src_path: str, dest_path: str, override: bool = False) -> dict:
    """Copies a file from a source path to a destination path.

    This function uses `shutil.copy2` to preserve file metadata. It also
    handles overwriting the destination file if `override` is True.

    Args:
        src_path (str): The path of the file to copy.
        dest_path (str): The path where the copy will be created.
        override (bool, optional): If True, overwrites the destination file if it
            exists. Defaults to False.

    Returns:
        dict: A log dictionary detailing the action's outcome.
    """
    # Efficiency: O(S) for both Time and Space, where S is the size of the file.
    create_directory(os.path.dirname(dest_path))
    if not override and os.path.exists(dest_path):
        return {
            "action_type": "Copy",
            "status": "Fail",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"Destination file already exists and override is set to False.",
        }
    try:
        shutil.copy2(src_path, dest_path)
        return {
            "action_type": "Copy",
            "status": "Success",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"Copied: {src_path} -> {dest_path}",
        }
    except FileNotFoundError:
        return {
            "action_type": "Copy",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"File {src_path} was not found.",
        }
    except PermissionError:
        return {
            "action_type": "Copy",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"Permission denied to copy {src_path} -> {dest_path}",
        }
    except IsADirectoryError:
        return {
            "action_type": "Copy",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"{src_path} is a directory. ",
        }
    except Exception:
        return {
            "action_type": "Copy",
            "status": "Error",
            "timestamp": datetime.datetime.strftime(datetime.datetime.now(), TIMESTAMP_FORMAT),
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"Something went wrong while copying {src_path} -> {dest_path}",
        }
