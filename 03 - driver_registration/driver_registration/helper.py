from typing import List, Type
from pydantic import BaseModel

import os
import csv
import json


class CSVHelper:
    __source_dir: str
    __target_dir: str

    def __init__(self, source_dir: str, target_dir: str):
        self.__source_dir = source_dir
        self.__target_dir = target_dir


    def get_data(self, source_filename: str, Schema: BaseModel) -> List[BaseModel]:
        filepath = os.path.join(self.__source_dir, f"{source_filename}.csv")
        with open(filepath, "r") as file:
            reader = csv.reader(file)

            result = []
            field = list(Schema.model_fields.keys())
            for row in reader:
                result.append(Schema(**{
                    k: v if(v != "NULL") else None
                    for k, v in zip(field, row)
                }))
        return result


class JSONHelper:
    __source_dir: str
    __target_dir: str

    def __init__(self, source_dir: str, target_dir: str):
        self.__source_dir = source_dir
        self.__target_dir = target_dir


    def export_data(self, data: List[BaseModel], target_filename: str):
        filepath = os.path.join(self.__target_dir, f"{target_filename}.json")

        fmt_data = [json.dumps(row.model_dump()) for row in data]
        with open(filepath, "w") as file:
            file.writelines(fmt_data)