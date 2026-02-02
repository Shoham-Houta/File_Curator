import os
import shutil


def create_directory(dest_path: str) -> dict:
    os.makedirs(dest_path, exist_ok=True)
    return {
        "action_type": "Create",
        "status": "Success",
        "timestamp": "",
        "destination_path": dest_path,
        "message": f"{dest_path} was created.",
    }


def delete_file(dest_path: str) -> dict:
    return {
        "action_type": "Delete",
        "status": "",
        "timestamp": "",
        "source_path": "",
        "destination_path": "",
        "message": "",
    }


def move_file(src_path: str, dest_path: str) -> dict:
    try:
        create_directory(os.path.dirname(dest_path))
        shutil.move(src_path, dest_path)
        return {
            "action_type": "Move",
            "status": "Success",
            "timestamp": "",
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"{src_path} -> {dest_path}",
        }
    except FileNotFoundError:
        return {
            "action_type": "Move",
            "status": "Error",
            "timestamp": "",
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"{src_path} was not found.",
        }
    except PermissionError:
        return {
            "action_type": "Move",
            "status": "Error",
            "timestamp": "",
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"No permission to move {src_path} -> {dest_path}.",
        }
    except Exception as e:
        return {
            "action_type": "Move",
            "status": "Error",
            "timestamp": "",
            "source_path": src_path,
            "destination_path": dest_path,
            "message": f"Something went wrong while moving {src_path} -> {dest_path}.",
        }


def copy_file(src_path: str, dest_path: str) -> dict:
    return {
        "action_type": "Copy",
        "status": "",
        "timestamp": "",
        "source_path": "",
        "destination_path": "",
        "message": "",
    }
