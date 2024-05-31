from typing import Optional, List, Any
import json

from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.engine import reflection
from sql_validation_rules.tools.tools_model import TableColumn


class TableColumnInfoDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for extracting information about a single field."""

    name = "sql_column_info"
    description = """Input is a table name and column name, output is information about the field, like e.g. the field type.
"""
    args_schema = TableColumn

    def _run(
        self,
        table: str,
        field: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute query to get information about a column in a table."""

        try:
            engine: Engine = self.db._engine
            inspector = reflection.Inspector.from_engine(engine)
            all_cols = inspector.get_columns(table)
            for col in all_cols:
                if col["name"] == field.lower():
                    col["is_foreign_key"] = is_foreign_key(table, field.lower(), engine)
                    return str(col)
            return "<Empty>"
        except Exception as e:
            return f"Error: {e}"

    async def _arun(
        self,
        table: str = "",
        field: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("ListTablesSqlDbTool does not support async")
    

def is_foreign_key(table_name: str, field_name: str, engine: Engine):
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    column = table.c.get(field_name)
    if column is not None:
        return any(column.foreign_keys)
    return False


