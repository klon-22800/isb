import json

from typing import Optional


def load(file_path: str) -> Optional[dict[str, str]]:
    """
        The function reads json file and return dict

    Args:
        file_path (str): path to json file

    Returns:
        Optional[dict]: dict contains sequences
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return None