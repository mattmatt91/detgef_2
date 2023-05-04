import json
import os
from datetime import datetime


def read_json(path: str):
    f = open(path)
    data = json.load(f)
    f.close()
    return data


def create_folder(path:str):
    path_folder =os.path.join(path, datetime.now().strftime("%m_%d_%Y-%H_%M_%S"))
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
        return path_folder
    else:
        raise ValueError("not able to create file")

