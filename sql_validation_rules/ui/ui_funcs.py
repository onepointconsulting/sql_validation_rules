import json
import streamlit as st

from sql_validation_rules.tools.sql_tools import sql_query_columns
from sql_validation_rules.graph.graph_utils import (
    invoke_column_rule,
    extract_sql_command,
)
from sql_validation_rules.graph.graph_utils import generate_supervisor_config

config = generate_supervisor_config()


@st.cache_data
def retrieve_cols(table: str):
    col_info_str = sql_query_columns(table)
    return json.loads(col_info_str)


def generate_rules(table: str, column: str) -> str:
    res = invoke_column_rule(table, column, config)
    return extract_sql_command(res["messages"])
