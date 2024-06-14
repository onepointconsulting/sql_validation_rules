from typing import Optional, List, Any
from json import dumps

from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun
)

class NumericColumnStatsSQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for executing statistical queries for a numeric column of a table."""

    name = "sql_db_numeric_statistics"
    description = """Input is a table name, output is a json string with the statistics for numeric columns of the table.

    Example Input: "table_name"
    """
    def _run(
        self,
        table_name: str = "",
        #column_name: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute statistical queries."""
        try:
            columns: List[Any] = self.db._inspector.get_columns(table_name)
            numeric_columns = [{"name": c["name"]} for c in columns if str(c["type"]).startswith('DECIMAL') or str(c["type"]).startswith('NUMBER') or str(c["type"]).startswith('NUMERIC')]
            #return dumps(numeric_columns)
            stats= dict()
            for nc in numeric_columns:
               #column_name: str ="W_WAREHOUSE_SQ_FT"
               column_name: str =nc["name"]
               stats_query: str = f"select count({column_name}) as count_not_null, count(*) - count({column_name}) as count_of_nulls, count(distinct {column_name})  as count_distinct_values, min({column_name})::string as min_value, max({column_name})::string as max_value  , mode({column_name})::string as most_frequent_value from {table_name}"
               #stats_query_result:str = self.db._execute(stats_query)
               stats[column_name] = self.db._execute(stats_query)[0]
               #print(stats[column_name])
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
        raise NotImplementedError("NumericColumnStatsSQLDatabaseTool does not support async")
            
    # query = "select count({column_name}) as CountNotNull, count(*) - count({column_name}) as CountNull, count(distinct {column_name})  as CountDistinct, min({column_name}) as MinValue, max({column_name}) as MaxValue  , mode({column_name}) as ModeValue from {table_name}"
    # call_sql_query(query)

    # query = "select count(field_name) from table_name"
    # query = "select count(*) - count(field_name) from table_name"    
    # query = "select count(distinct field_name) from table_name"  
    # query = "select min(field_name) from table_name"          
    # query = "select max(field_name) from table_name"
    # query = "select mode(field_name) from table_name"    