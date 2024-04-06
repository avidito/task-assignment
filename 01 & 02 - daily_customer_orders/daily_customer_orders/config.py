from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PROJECT_ID: str = Field(default="noel-lyn-dev")
    DATE_COLUMN: str = Field(default="DATE(order_date)")