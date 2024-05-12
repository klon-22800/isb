import json


def write_json(path: str, data: dict) -> None:
    """function write data to .json file

    Args:
        path (str): path to file
        data (dict): data for writing
    """
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception as error:
        print(error)


def read_json(path: str) -> dict:
    """function read .json file and return data from them

    Args:
        path (str): path to file

    Returns:
        dict: data from file
    """
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data
    except Exception as error:
        print(error)
