import sys
from sql_validation_rules.db_connection_factory import sql_db_factory

from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain.tools import BaseTool, tool
from langchain_community.tools.sql_database.tool import ListSQLDatabaseTool
from langchain_core.tools import BaseTool

from sql_validation_rules.config.config import cfg
from sql_validation_rules.tools.list_columns_tool import ListIndicesSQLDatabaseTool
from sql_validation_rules.tools.sql_numeric_stats_tool import NumericColumnStatsSQLDatabaseTool
from sql_validation_rules.tools.sql_stats_string import CalcStatsForStringCols

db = sql_db_factory()

list_tables_tool: BaseTool = ListSQLDatabaseTool(db=db)

info_tables_tool: BaseTool = InfoSQLDatabaseTool(db=db)

query_sql: BaseTool = QuerySQLDataBaseTool(db=db)

query_sql_checker: BaseTool = QuerySQLCheckerTool(db=db, llm=cfg.llm)

query_columns_tool: BaseTool = ListIndicesSQLDatabaseTool(db=db)

query_numeric_columns_stats: BaseTool = NumericColumnStatsSQLDatabaseTool(db=db)
query_string_columns_stats: BaseTool = CalcStatsForStringCols(db=db)

# Simplistic cache for the SQL list tables.
sys.list_tables_cache = ""


# Note that the input string is ignored here but cannot be removed.
@tool("list_tables", return_direct=True)
def sql_list_tables(input: str) -> str:
    """Returns all tables in the current database."""
    if len(sys.list_tables_cache) > 0:
        return sys.list_tables_cache
    sys.list_tables_cache = list_tables_tool(tool_input="")
    return sys.list_tables_cache


@tool("info_tables", return_direct=True)
def sql_info_tables(table_list_str: str) -> str:
    """Returns information about a list of tables."""
    return info_tables_tool(tool_input=table_list_str)


@tool("sql_query", return_direct=True)
def sql_query(sql: str) -> str:
    """Executes a SQL query"""
    return query_sql(tool_input=sql)


@tool("sql_query_checker", return_direct=True)
def sql_query_checker(sql: str) -> str:
    """Validates SQL queries to check if the syntax is correct"""
    return query_sql_checker(tool_input=sql)


@tool("sql_query_columns", return_direct=True)
def sql_query_columns(table_name: str) -> str:
    """Gets columns of a table as a JSON array"""
    return query_columns_tool(table_name)

@tool("calc_string_column_stats", return_direct=True)
def calc_string_column_stats(table_name: str) -> str:
    """Gets column statistics of string fields of a table as a JSON object"""
    return query_string_columns_stats(table_name)


@tool("calc_numeric_column_stats", return_direct=True)
def calc_numeric_column_stats(table_name: str) -> str:
    """Gets column statistics of numeric fields of a table as a JSON object"""
    return query_numeric_columns_stats(table_name)

if __name__ == "__main__":

    from sql_validation_rules.config.log_factory import logger

    def call_list_tables() -> str:
        table_list = sql_list_tables.run("")
        logger.info(f"table list: {table_list}")
        return table_list

    def call_sql_info_tables(table_list_str: str):
        res = sql_info_tables.run(table_list_str)
        logger.info(type(res))
        logger.info(f"table info: {res}")

    def call_sql_query(sql: str):
        res = sql_query.run(sql)
        logger.info(type(res))
        logger.info(f"SQL query result: {res}")

    def call_sql_query_checker(sql: str):
        res = sql_query_checker(sql)
        logger.info(type(res))
        logger.info(f"SQL query check result: {res}")

    def call_sql_query_columns(table_name: str):
        logger.info(f"- Table: {table_name}")
        res = sql_query_columns(table_name)
        logger.info(type(res))
        logger.info(f"SQL query columns result: {res}")
        
    def call_calc_str_col_stats(table_name: str):
        logger.info(f"- Table: {table_name}")
        res = calc_numeric_column_stats(table_name)
        logger.info(type(res))
        logger.info(f"SQL query columns result: {res}")        

    def call_sql_numeric_stats(table_name: str):
        logger.info(f"- Table: {table_name}")
        res = calc_numeric_column_stats(table_name)
        logger.info(type(res))
        logger.info(f"Numeric Stats result: {res}")        

    #table_list_str = call_list_tables()
    # call_sql_info_tables(table_list_str)
    # query = "select count(*) from call_center"
    # call_sql_query(query)
    # call_sql_query_checker(query)
    # call_sql_query_checker("select from call_center")
    #table_list = [t.strip() for t in table_list_str.split(",")]
    #call_sql_query_columns(table_list[0])
    
    call_calc_str_col_stats("warehouse")
