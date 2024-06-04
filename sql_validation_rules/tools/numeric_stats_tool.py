import json

from typing import Optional, List, Any
from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from sql_validation_rules.tools.tools_model import TableColumn


class NumericStatsSQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for running statistical queries on numeric fields."""

    name = "sql_numeric_statistics"
    description = """Input is a table name and column name, output are the results of statistical queries for min, max and average.

    Example Input: "table" "field"
    """
    args_schema = TableColumn

    def _run(
        self,
        table: str,
        field: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute pre=defined statistical querie, like e.g. min, max, averages."""

        try:
            # TODO: Include other statistical queries.
            result: List[List[Any]] = self.db._execute(
                f"select min({field}), avg({field}), max({field}), stddev({field}), mode({field}), median({field}) from {table}"
            )
            for row in result:
                return json.dumps({k: float(v) for k, v in row.items()})
            return "<Empty>"
        except Exception as e:
            return f"Error: {e}"

    async def _arun(
        self,
        table_names: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("ListTablesSqlDbTool does not support async")
