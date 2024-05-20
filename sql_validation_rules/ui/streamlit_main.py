from enum import StrEnum

import json
import streamlit as st

from sql_validation_rules.tools.sql_tools import sql_query_columns, sql_list_tables
from sql_validation_rules.graph.graph_utils import (
    generate_supervisor_config,
    invoke_column_rule,
    extract_sql_command,
)

config = generate_supervisor_config()

# Define custom CSS for column width
st.markdown(
    """
    <style>
    .block-container {
        max-width: 90% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the title of the app
st.title("SQL Rule Generator")

# Create three columns
table_col, field_col, results_col = st.columns([0.25, 0.25, 0.5])


class SessionKeys(StrEnum):
    COLUMNS = "columns"
    TABLE = "selected_table"
    COLUMN = "selected_column"
    COLUMN_TYPE = "selected_column_type"
    GENERATED_RULE = "generated_rule"


if SessionKeys.COLUMNS not in st.session_state:
    st.session_state[SessionKeys.COLUMNS] = []

if SessionKeys.TABLE not in st.session_state:
    st.session_state[SessionKeys.TABLE] = ""

if SessionKeys.COLUMN not in st.session_state:
    st.session_state[SessionKeys.COLUMN] = ""

if SessionKeys.COLUMN_TYPE not in st.session_state:
    st.session_state[SessionKeys.COLUMN_TYPE] = ""

if SessionKeys.GENERATED_RULE not in st.session_state:
    st.session_state[SessionKeys.GENERATED_RULE] = ""


@st.cache_data
def retrieve_cols(table: str):
    col_info_str = sql_query_columns(table)
    return json.loads(col_info_str)


def generate_rules(table: str, column: str) -> str:
    res = invoke_column_rule(table, column, config)
    return extract_sql_command(res["messages"])


# Used to display the tables
with table_col:
    st.header("Table")
    tables = sql_list_tables("")
    for t in tables.split(","):
        if st.button(t):
            st.session_state[SessionKeys.TABLE] = t
            st.session_state[SessionKeys.COLUMNS] = retrieve_cols(t)


# Used to display the columns
with field_col:
    st.header("Column")
    for col in st.session_state[SessionKeys.COLUMNS]:
        col_name = col["name"]
        if st.button(f"{col_name}"):
            st.session_state[SessionKeys.COLUMN] = col_name
            st.session_state[SessionKeys.COLUMN_TYPE] = col["type"]


# Used to display the selected column
with results_col:
    st.header("Column Details")
    if (
        len(st.session_state["selected_table"]) > 0
        and len(st.session_state["selected_column"]) > 0
    ):
        table = st.session_state[SessionKeys.TABLE]
        column = st.session_state[SessionKeys.COLUMN]
        st.write(f"Table: {table}")
        st.write(f"Column: {column}")
        st.write(st.session_state[SessionKeys.COLUMN_TYPE])
        if st.button("Generate rules"):
            with st.spinner("Processing..."):
                st.write(generate_rules(table, column))
