
from typing import Optional, List, Any
from json import dumps

from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun
)

class GenerateTableStatsSQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for executing statistical queries for all columns of a table."""

    name = "sql_db_table_statistics"
    description = """Input is a table name, output is a json string with the statistics for each columns of the table.

    Example Input: "table_name"
    """
    def _run(
        self,
        table_name: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute statistical queries."""
        try:
            columns: List[Any] = self.db._inspector.get_columns(table_name)
            stats= dict()
            for c in columns:
               column_name: str =c["name"]
               stats_query: str = f"select '{column_name}' as column_name, count({column_name}) as count_not_null, count(*) - count({column_name}) as count_of_nulls, count(distinct {column_name})  as count_distinct_values, min({column_name})::string as min_value, max({column_name})::string as max_value  , mode({column_name})::string as most_frequent_value, min(len({column_name}))::string as min_length_of_values, avg(len({column_name}))::string as average_length_of_values, max(len({column_name}))::string as max_length_of_values from {table_name}"
               stats[column_name] = self.db._execute(stats_query)[0]
            return dumps(stats)
            #for row in stats:
                #print(row.items())
                #return dumps({k:float(v) for k,v in row.items()})
        except Exception as e:
            return f"Error: {e}"
            
    async def _arun(
        self,
        table_names: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("GenerateTableStatsSQLDatabaseTool does not support async")