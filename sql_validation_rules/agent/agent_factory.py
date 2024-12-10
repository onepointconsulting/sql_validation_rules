from typing import List

from langchain.agents import create_openai_functions_agent
from langchain_core.runnables.base import RunnableSequence

from sql_validation_rules.config.config import cfg
from sql_validation_rules.tools.sql_tools import (
    sql_query,
    sql_query_checker,
    sql_info_tables,
    sql_query_table_stats,
    #column_stats_tool,
    calc_string_column_stats,
    calc_numeric_column_stats,
)
from sql_validation_rules.agent.prompt_factory import create_sql_validation_template
from sql_validation_rules.agent.agent_state import FIELD_EXCLUSION_RULES


def create_agent_runnable() -> RunnableSequence:
    """Construct an OpenAI functions agent"""
    return create_openai_functions_agent(
        llm=cfg.llm,
        prompt=create_sql_validation_template(),
        tools=[sql_info_tables, sql_query, sql_query_checker, sql_query_table_stats],
        #tools=[sql_info_tables, sql_query, sql_query_checker, column_stats_tool],
        #tools=[sql_info_tables, calc_string_column_stats, calc_numeric_column_stats, sql_query, sql_query_checker],
    )


agent_runnable = create_agent_runnable()

if __name__ == "__main__":

    inputs = {
        "table": "web_site",
        "field": "web_suite_number",
        FIELD_EXCLUSION_RULES: "",
        "chat_history": [],
        "intermediate_steps": [],
    }
    res = agent_runnable.invoke(inputs)
    print(res)
