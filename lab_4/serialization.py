import json


def write_json(path: str, data: dict)-> None:
    """_summary_

    Args:
        path (str): _description_
        data (dict): _description_
    """
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception as error:
        print(error)


def read_json(path: str)-> dict:
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data
    except Exception as error:
        print(error)