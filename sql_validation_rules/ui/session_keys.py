from enum import StrEnum

import streamlit as st


class SessionKeys(StrEnum):
    COLUMNS = "columns"
    TABLE = "selected_table"
    COLUMN = "selected_column"
    COLUMN_TYPE = "selected_column_type"
    GENERATED_RULE = "generated_rule"


def init_session():
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
