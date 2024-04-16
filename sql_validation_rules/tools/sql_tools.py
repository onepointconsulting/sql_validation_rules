from typing import List
from sql_validation_rules.db_connection_factory import sql_db_factory

from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain_community.tools.sql_database.tool import ListSQLDatabaseTool
from langchain_core.tools import BaseTool

from sql_validation_rules.config.config import cfg

db = sql_db_factory()

list_tables_tool: BaseTool = ListSQLDatabaseTool(db=db)

info_tables_tool: BaseTool = InfoSQLDatabaseTool(db=db)

query_sql: BaseTool = QuerySQLDataBaseTool(db=db)

query_sql_checker: BaseTool = QuerySQLCheckerTool(db=db, llm=cfg.llm)


@tool("list_tables", return_direct=True)
def sql_list_tables(input: str) -> str:
    """Returns all tables in the current database."""
    return list_tables_tool(tool_input="")


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

    table_list = call_list_tables()
    call_sql_info_tables(table_list)
    query = "select count(*) from call_center"
    call_sql_query(query)
    call_sql_query_checker(query)
    call_sql_query_checker("select from call_center")
