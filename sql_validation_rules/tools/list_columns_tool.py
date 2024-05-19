from typing import Optional, List, Any
from json import dumps

from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from sql_validation_rules.config.log_factory import logger


class ListIndicesSQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for getting columns of a table."""

    name = "sql_db_list_columns"
    description = """Input is a single table name, output is a JSON string with the names and types of the columns.

    Example Input: "table_name"
    """

    def _run(
        self,
        table_name: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get the indices for all tables."""
        if table_name is None:
            logger.warn(f"Table {table_name} is empty.")
            return []
        table_name = table_name.strip()
        try:
            logger.info(f"Listing columns for {table_name}.")
            columns: List[Any] = self.db._inspector.get_columns(table_name)
            simplified_columns = [
                {"name": c["name"], "type": str(c["type"])} for c in columns
            ]
            return dumps(simplified_columns)
        except Exception as e:
            logger.exception(f"Could not fetch columns for {table_name}")
            return f"Error: {e}"

    async def _arun(
        self,
        table_names: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("ListTablesSqlDbTool does not support async")
