from typing import List
from pydantic.v1 import BaseModel, Field


class SQLCommand(BaseModel):
    validation_command: str = Field(
        ..., description="The extracted SQL command used to find anomalous records"
    )
    validation_type: str = Field(
        ..., description="The type of validation associated to this command"
    )

    def __repr__(self):
        return f"""-- {self.validation_type}
{self.validation_command}
"""

class SQLCommands(BaseModel):
    validation_commands: List[SQLCommand] = Field(
        ..., description="The extracted SQL commands"
    )
