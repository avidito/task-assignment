import os
from typing import List, Optional
from jinja2 import Template

from google.cloud.bigquery import Client as BQClient


class BQHelper:
    __bq: BQClient
    __query_dir: str

    def __init__(self, project_id: str, query_dir: str):
        self.__bq = BQClient(project_id)
        self.__query_dir = query_dir


    def run_query(self, query: str, params: Optional[dict] = None):
        query_file = os.path.join(self.__query_dir, query)
        with open(query_file, "r") as file:
            query_str = file.read()
        
        t_query = self.__templating(query_str, params)
        self.__bq.query_and_wait(t_query)
        return

    
    def __templating(self, query: str, params: dict) -> str:
        t = Template(query)
        t_query = t.render({
            "params": params
        })
        return t_query