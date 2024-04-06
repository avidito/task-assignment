from pydantic import Field
from pydantic_settings import BaseSettings

import os
SOURCE_DIR = os.path.join(os.path.dirname(__file__), "source")
TARGET_DIR = os.path.join(os.path.dirname(__file__), "target")


class Config(BaseSettings):
    SOURCE_DIR: str = Field(default=SOURCE_DIR)
    TARGET_DIR: str = Field(default=TARGET_DIR)