import json
import streamlit as st

from sql_validation_rules.tools.sql_tools import sql_query_columns, sql_list_tables

# Set the title of the app
st.title('SQL Rule Generator')

# Create three columns
table_col, field_col, results_col = st.columns(3)

try:
    # check if the key exists in session state
    st.session_state["columns"]
except KeyError:
    # otherwise set it to it init value
    st.session_state["columns"] = []

st.session_state["selected_table"] = ""
st.session_state["selected_column"] = ""

@st.cache_data
def retrieve_cols(table: str):
    col_info_str = sql_query_columns(table)
    return json.loads(col_info_str)


# Used to display the tables
with table_col:
    st.header("Table")
    tables = sql_list_tables("")
    for t in tables.split(","):
        if st.button(t):
            st.session_state["selected_table"] = t
            st.session_state["columns"] = retrieve_cols(t)
    

# Used to display the columns
with field_col:
    st.header("Column")
    for col in st.session_state["columns"]:
        col_name = col['name']
        if st.button(f"{col_name}", help=f"Type: {col['type']}"):
            st.session_state["selected_column"] = col_name
    

# Used to display rules
with results_col:
    st.header("SQL rule")
    if len(st.session_state["selected_table"]) > 0 and len(st.session_state["selected_column"]) > 0:
        st.write("This is the content of the third column.")
        st.checkbox("Checkbox in Column 3")