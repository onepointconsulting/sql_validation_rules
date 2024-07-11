import json
import decimal

from typing import Optional, List, Any
from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from sql_validation_rules.tools.tools_model import TableColumn


class ColumnStatsSQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for calculating statistics for a column."""

    name = "sql_column_statistics"
    description = """Input is a table name and column name, output are the statistics for a column - count, count nulls, count distinct, min, max, average, mode.

    Example Input: "table" "field"
    """
    args_schema = TableColumn

    def _run(
        self,
        table: str,
        field: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute predefined statistical querie, like e.g. min, max, averages, mode, count nulls, count not nulls, distinct etc."""

        try:
            query = f"select count({field}) as count_not_null, count(*) - count({field}) as count_of_nulls, count(distinct {field})  as count_distinct_values, min({field}) as min_value, max({field}) as max_value  , mode({field}) as most_frequent_value, min(len({field})) as min_length_of_values, avg(len({field})) as average_length_of_values, max(len({field})) as max_length_of_values from {table}"  
            result: List[List[Any]] = self.db._execute(query)            
            
            for row in result:                                   
                return json.dumps({k: (float(v) if isinstance(v, decimal.Decimal) else v) for k, v in row.items()})
            return "<Empty>"        
        except Exception as e:
            return f"Error: {e}"
     

    async def _arun(
        self,
        table_names: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("ColumnStatsSQLDatabaseTool does not support async")
