from typing import List
from pydantic.v1 import BaseModel, Field


class SQLCommands(BaseModel):
    validation_commands: List[str] = Field(
        ..., description="The extracted SQL commands"
    )
