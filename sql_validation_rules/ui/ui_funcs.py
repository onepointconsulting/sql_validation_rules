import json
import streamlit as st

from sql_validation_rules.tools.sql_tools import sql_query_columns
from sql_validation_rules.graph.graph_utils import (
    invoke_column_rule,
    extract_sql_command,
    convert_sql_command_to_str,
)
from sql_validation_rules.graph.graph_utils import generate_supervisor_config
from sql_validation_rules.persistence.sql_rules import SQLRule
from sql_validation_rules.persistence.crud import save_sql_rule

config = generate_supervisor_config()


@st.cache_data
def retrieve_cols(table: str):
    col_info_str = sql_query_columns(table)
    return json.loads(col_info_str)


def save_rule(table: str, column: str, sql: str, rule_title: str):
    sql_rule = SQLRule(table=table, column=column, sql=sql, title=rule_title)
    save_sql_rule(sql_rule)


def generate_rules(table: str, column: str) -> str:
    res = invoke_column_rule(table, column, config)
    sql_commands = extract_sql_command(res["messages"])
    for sql_command in sql_commands:
        save_rule(
            table, column, sql_command.validation_command, sql_command.validation_type
        )
    return convert_sql_command_to_str(sql_commands)
