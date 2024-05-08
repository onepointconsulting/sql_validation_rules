import json

from typing import Optional, List, Any
from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic.v1 import BaseModel, Field


class TableColumn(BaseModel):
    table_name: str = Field(..., description="The name of the table")
    column_name: str = Field(..., description="The name of the table columns")


class NumericStatsSQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for running statistical queries on numeric fields."""

    name = "sql_numeric_statistics"
    description = """Input is a table name and column name, output are the results of statistical queries for min, max and average.

    Example Input: "table_name" "column_name"
    """
    args_schema = TableColumn

    def _run(
        self,
        table_name: str,
        column_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute pre=defined statistical queries."""

        try:
            result: List[List[Any]] = self.db._execute(
                f"select min({column_name}), avg({column_name}), max({column_name}) from {table_name}"
            )
            # TODO: Include other statistical queries.
            for row in result:
                return json.dumps({k:float(v) for k,v in row.items()})
            return "<Empty>"
        except Exception as e:
            return f"Error: {e}"

    async def _arun(
        self,
        table_names: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("ListTablesSqlDbTool does not support async")
