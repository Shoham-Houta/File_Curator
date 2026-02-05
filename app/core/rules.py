from actions import copy_file, delete_file, move_file, create_directory


class RuleEngine:
    def __init__(self):
        self.rules = self._load_rules()

        self.dispatcher = {
            "Move": move_file,
            "Delete": delete_file,
            "Create directory": create_directory,
            "Copy": copy_file,
        }

    @staticmethod
    def _load_rules():
        return [
            {
                "rule_name": "Move PDF to Documents",
                "conditions": {
                    "MimeType": "application/pdf",
                    "PathContains": "/data/downloads",

                },
                "action": {
                    "type": "Move",
                    "destination_path": "./data/documents",
                    "override": False,
                }
            },

        ]

    def evaluate(self, file_path: str, file_type: str):
        for rule in self.rules:
            if self._check_condition(rule["conditions"],file_path, file_type):
                action_info = rule["action"]
                action_type = action_info["type"]
                action_func = self.dispatcher[action_type]

                if action_type == "Move":
                    log = action_func(src_path=file_path, dest_path=action_info["destination_path"], override=action_info.get("override", False))
                    return log
                elif action_type == "Delete":
                    log = action_func(dest_path=file_path,)
                    return log
                elif action_type == "Copy":
                    log = action_func(src_path=file_path, dest_path=action_info["destination_path"], override=action_info.get("override", False))
                    return log
                elif action_type == "Create directory":
                    log = action_func(dest_path=action_info["destination_path"],)
                    return log
        return None

    @staticmethod
    def _check_condition(conditions: dict, file_path: str, file_type: str):
        for condition_key, expected_val in conditions.items():
            match condition_key:
                case "MimeType":
                    if file_type != expected_val:
                        return False
                case "PathContains":
                    if expected_val not in file_path:
                        return False
        return True
