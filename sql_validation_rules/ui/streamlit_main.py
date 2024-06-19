from typing import Generator, List
import streamlit as st

from sql_validation_rules.tools.sql_tools import sql_list_tables
from sql_validation_rules.config.config import cfg
from sql_validation_rules.ui.session_keys import init_session, SessionKeys
from sql_validation_rules.ui.ui_funcs import generate_rules, retrieve_cols
from sql_validation_rules.graph.graph_utils import sql_command_to_str
from sql_validation_rules.persistence.sql_to_pandas import execute_read_sql_as_df
from sql_validation_rules.chain.sql_commands import SQLCommand

# Define custom CSS for column width
st.markdown(
    """
    <style>
    .block-container {
        max-width: 90% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Set the title of the app
st.title("SQL Rule Generator")

tab_column, tab_table = st.tabs(["Column Generator", "Table Generator"])

init_session()


def table_col_render(tab_name: str):
    st.header("Table")
    tables = sql_list_tables("")
    for idx, t in enumerate(tables.split(",")):
        if st.button(t, key=f"{tab_name}_{idx}"):
            st.session_state[SessionKeys.TABLE] = t
            st.session_state[SessionKeys.COLUMNS] = retrieve_cols(t)
            st.session_state[SessionKeys.COLUMN] = ""


def has_selected_table():
    return len(st.session_state[SessionKeys.TABLE]) > 0


def col_generator() -> Generator[str, None, None]:
    for col in st.session_state[SessionKeys.COLUMNS]:
        col_name: str = col["name"]
        yield col_name, col["type"]


def display_sql_commands(sql_commands: List[SQLCommand]):
    if len(sql_commands) == 0:
        st.write("No SQL commands were generated.")
    for i, sql_command in enumerate(sql_commands):
        st.write(sql_command_to_str(sql_command))
        # Printing 10 results
        st.write("#### Query result")
        df = execute_read_sql_as_df(sql_command.validation_command, 10)
        st.dataframe(df)


with tab_column:

    # Create three columns
    table_col, field_col, results_col = st.columns([0.25, 0.25, 0.5])

    # Used to display the tables
    with table_col:
        table_col_render("tab_column")

    # Used to display the columns
    with field_col:
        st.header("Column")
        for col_name, col_type in col_generator():
            if st.button(f"{col_name}"):
                st.session_state[SessionKeys.COLUMN] = col_name
                st.session_state[SessionKeys.COLUMN_TYPE] = col_type

    # Used to display the selected column
    with results_col:
        st.header("Generate Rules")
        if has_selected_table() and len(st.session_state["selected_column"]) > 0:
            table = st.session_state[SessionKeys.TABLE]
            column = st.session_state[SessionKeys.COLUMN]
            st.write(f"Table: {table}")
            st.write(f"Column: {column}")
            st.write(st.session_state[SessionKeys.COLUMN_TYPE])
            if st.button("Generate rules"):
                if cfg.langsmith_project_url:
                    st.markdown(
                        f"[View execution on Langsmith]({cfg.langsmith_project_url})"
                    )
                with st.spinner("Generating rules. Please wait ..."):
                    try:
                        sql_commands = generate_rules(table, column)
                        display_sql_commands(sql_commands)
                    except Exception as e:
                        st.exception(e)


with tab_table:

    # Create three columns
    table_col, results_col = st.columns([0.25, 0.75])

    # Used to display the tables
    with table_col:
        table_col_render("tab_table")

    # The table used to print the results
    with results_col:
        st.header("Generate Table Rules")
        if has_selected_table():
            table = st.session_state[SessionKeys.TABLE]
            st.write(f"Table: {table}")
            if st.button(
                f"Generate rules for {len(st.session_state[SessionKeys.COLUMNS])} columns"
            ):
                for col_name, _ in col_generator():
                    with st.spinner(
                        f"Generating rules for {col_name}. Please wait ..."
                    ):
                        try:
                            st.markdown(f"## {col_name}")
                            sql_commands = generate_rules(table, col_name)
                            display_sql_commands(sql_commands)
                        except Exception as e:
                            st.exception(e)
