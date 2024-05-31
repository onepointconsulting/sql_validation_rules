import re
from typing import Any, Dict, Optional, Sequence, Type, Union

from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from sqlalchemy.engine import Result
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)

LIMIT_EXPRESSION = " limit 1000;"


class _QuerySQLDataBaseToolInput(BaseModel):
    query: str = Field(..., description="A detailed and correct SQL query.")


class ValidatorQuerySQLDataBaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for querying a SQL database."""

    name: str = "sql_db_query"
    description: str = """
    Execute a SQL query against the database and get back the result..
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    args_schema: Type[BaseModel] = _QuerySQLDataBaseToolInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[str, Sequence[Dict[str, Any]], Result]:
        """Execute the query, return the results or an error message."""
        # Make sure that the tool is limited to a specific amount of rows, otherwise we might get in trouble.
        query = append_limit(query)
        return self.db.run_no_throw(query)


def append_limit(query: str) -> str:
    if " limit " not in query.lower():
        query = query.strip()
        query = re.sub(r";$", "", query)
        query += LIMIT_EXPRESSION
    return query


if __name__ == "__main__":
    query = "SELECT c_birth_month FROM customer WHERE c_birth_month IS NOT NULL;"
    query = append_limit(query)
    assert LIMIT_EXPRESSION in query, query
    print(query)

    query = "SELECT c_birth_month FROM customer WHERE c_birth_month IS NOT NULL LIMIT 100;"
    query = append_limit(query)
    assert "LIMIT 100" in query, query
    print(query)