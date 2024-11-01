from typing import Optional, List, Any
from json import dumps

from langchain.tools.sql_database.tool import BaseSQLDatabaseTool
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class CalcStatsForStringCols(BaseSQLDatabaseTool, BaseTool):
    """Tool for getting statistics of all string columns."""

    name = "sql_db_calc_str_stats"
    description = """Input is a single table name, output is a JSON string with the statistics related to string columns of the table.

    Example Input: "table_name"
    """

    def _run(
        self,
        table_name: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Fetch statistics for all string column of a table."""
        try:
            columns: List[Any] = self.db._inspector.get_columns(table_name)
            # for col in columns:
            #    print(str(col['type']).startswith('VARCHAR'))
            #    print(type(col['type']))
            string_columns = [
                column["name"]
                for column in columns
                if str(column["type"]).startswith("VARCHAR")
                or str(column["type"]).startswith("TEXT")
            ]
            stats = {}
            for col in string_columns:
                query = f"select count({col}) as count_not_null, count(*) as count_with_nulls, count(distinct {col}) as count_distinct_values, min({col}) as min_value , max({col}) as max_value, mode({col}) as most_frequent_value, min(len({col})) as min_length_of_values, avg(len({col}))::string as average_length_of_values, max(len({col})) as max_length_of_values from {table_name}"
                res = self.db._execute(query)
                stats[col] = res[0]
                # print(stats[col])
            return dumps(stats)
        except Exception as e:
            return f"Error: {e}"

    async def _arun(
        self,
        table_names: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("CalcStatsForStringCols does not support async")
