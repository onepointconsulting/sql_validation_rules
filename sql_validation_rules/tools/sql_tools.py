import sys
from sql_validation_rules.persistence.db_connection_factory import sql_db_factory

from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
)
from langchain.tools import BaseTool, tool
from langchain_community.tools.sql_database.tool import ListSQLDatabaseTool
from langchain_core.tools import BaseTool

from sql_validation_rules.config.config import cfg
from sql_validation_rules.tools.list_columns_tool import ListIndicesSQLDatabaseTool
from sql_validation_rules.tools.numeric_stats_tool import (
    NumericStatsSQLDatabaseTool,
    TableColumn,
)
from sql_validation_rules.tools.table_column_info_tool import (
    TableColumnInfoDatabaseTool,
)
from sql_validation_rules.tools.query_sql_db_tool import ValidatorQuerySQLDataBaseTool
from langchain_core.runnables.base import RunnableSequence
from sql_validation_rules.tools.sql_numeric_stats_tool import NumericColumnStatsSQLDatabaseTool
from sql_validation_rules.tools.sql_stats_string import CalcStatsForStringCols

db = sql_db_factory()

list_tables_tool: BaseTool = ListSQLDatabaseTool(db=db)

info_tables_tool: BaseTool = InfoSQLDatabaseTool(db=db)

query_sql: BaseTool = ValidatorQuerySQLDataBaseTool(db=db)

query_sql_checker: BaseTool = QuerySQLCheckerTool(db=db, llm=cfg.llm)

query_columns_tool: BaseTool = ListIndicesSQLDatabaseTool(db=db)

numeric_stats_tool: BaseTool = NumericStatsSQLDatabaseTool(
    db=db, args_schema=TableColumn
)

table_column_info_tool: BaseTool = TableColumnInfoDatabaseTool(
    db=db, args_schema=TableColumn
)

query_numeric_columns_stats: BaseTool = NumericColumnStatsSQLDatabaseTool(db=db)
query_string_columns_stats: BaseTool = CalcStatsForStringCols(db=db)

# Simplistic cache for the SQL list tables.
list_tables_cache = ""

# Note that the input string is ignored here but cannot be removed.
@tool("list_tables", return_direct=True)
def sql_list_tables(input: str) -> str:
    """Returns all tables in the current database."""
    global list_tables_cache
    if len(list_tables_cache) > 0:
        return list_tables_cache
    sys.list_tables_cache = list_tables_tool(tool_input="")
    return sys.list_tables_cache

sql_info_tables_cache = {}

@tool("info_tables", return_direct=True)
def sql_info_tables(table_list_str: str) -> str:
    """Returns information about a list of tables."""
    global sql_info_tables_cache
    if table_list_str in sql_info_tables_cache:
        return sql_info_tables_cache[table_list_str]
    res = info_tables_tool(tool_input=table_list_str)
    sql_info_tables_cache[table_list_str] = res


@tool("sql_db_query", return_direct=True)
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
    """Gets column statistics of all string fields of a table as a JSON object"""
    return query_string_columns_stats(table_name)


@tool("calc_numeric_column_stats", return_direct=True)
def calc_numeric_column_stats(table_name: str) -> str:
    """Gets column statistics of all numeric fields of a table as a JSON object"""
    return query_numeric_columns_stats(table_name)


def create_table_info_runnable_sequence() -> RunnableSequence:
    """Creates a runnable sequence for the table information column tool"""

    from langchain_core.runnables import RunnableLambda

    def last_step(content: str) -> str:
        return content

    return RunnableSequence(
        first=table_column_info_tool, last=RunnableLambda(last_step)
    )


if __name__ == "__main__":

    from sql_validation_rules.config.log_factory import logger
    from sql_validation_rules.tools.numeric_stats_tool import TableColumn

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

    def call_sql_numeric_statistics(table_col_dict: TableColumn):
        logger.info(f"- Table: {table_col_dict}")
        res = numeric_stats_tool.run(table_col_dict.dict())
        assert res is not None
        assert isinstance(res, str)
        logger.info(f"Stats: {res}")

    def call_table_column_info(table_col_dict: TableColumn):
        logger.info(f"- Table: {table_col_dict}")
        res = table_column_info_tool.run(table_col_dict.dict())
        assert res is not None
        logger.info(f"Table column res: {res}; type: {type(res)}")

    def call_table_column_info_as_runnable_sequence(table_col_dict: TableColumn):
        res = create_table_info_runnable_sequence().invoke(table_col_dict.dict())
        assert res is not None
        logger.info(f"Table column info res: {res}; type: {type(res)}")

    table_list_str = call_list_tables()
    assert numeric_stats_tool.args_schema is not None
    call_sql_info_tables(table_list_str)
    query = "select count(*) from call_center"
    call_sql_query(query)
    call_sql_query_checker(query)
    call_sql_query_checker("select from call_center")
    table_list = [t.strip() for t in table_list_str.split(",")]
    call_sql_query_columns("customer")
    table_col = TableColumn(table="call_center", field="cc_tax_percentage")
    call_sql_numeric_statistics(table_col)
    call_table_column_info(table_col)
    call_table_column_info_as_runnable_sequence(table_col)
    call_table_column_info_as_runnable_sequence(
        TableColumn(table="call_center", field="cc_open_date_sk")
    )
    call_table_column_info_as_runnable_sequence(
        TableColumn(table="call_center", field="cc_closed_date_sk")
    )
