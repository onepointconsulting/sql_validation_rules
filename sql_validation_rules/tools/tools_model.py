from pydantic.v1 import BaseModel, Field


class TableColumn(BaseModel):
    table: str = Field(..., description="The name of the table")
    field: str = Field(..., description="The name of the table columns")
