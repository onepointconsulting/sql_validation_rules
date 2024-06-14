from typing import List

from langchain.agents import create_openai_functions_agent
from langchain_core.runnables.base import RunnableSequence

from sql_validation_rules.config.config import cfg
from sql_validation_rules.tools.sql_tools import (
    sql_query,
    sql_query_checker,
    sql_info_tables,
    numeric_stats_tool,
    calc_string_column_stats,
    calc_numeric_column_stats
)
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from sql_validation_rules.agent.prompt_factory import (
    create_sql_validation_template,
    create_sql_validation_numeric_template
)
from sql_validation_rules.agent.agent_state import (
    FIELD_VALIDATION_SQL_HISTORY,
    FIELD_CHAT_HISTORY,
)


def create_agent_runnable() -> RunnableSequence:
    """Construct an OpenAI functions agent"""
    return create_agent_runnable_helper(
        create_sql_validation_template(),
        [sql_info_tables, calc_string_column_stats, calc_numeric_column_stats, sql_query, sql_query_checker],
    )


def create_numeric_agent_runnable() -> RunnableSequence:
    """Construct an OpenAI functions agent"""
    return create_agent_runnable_helper(
        create_sql_validation_numeric_template(),
        [sql_info_tables, sql_query, sql_query_checker, numeric_stats_tool],
    )


def create_agent_runnable_helper(
    template: ChatPromptTemplate, tools: List[BaseTool]
) -> RunnableSequence:
    """Construct an OpenAI functions agent"""
    return create_openai_functions_agent(
        llm=cfg.llm,
        prompt=template,
        tools=tools,
    )


agent_runnable = create_agent_runnable()

agent_runnable_numeric = create_numeric_agent_runnable()

if __name__ == "__main__":

    # Run with python .\sql_validation_rules\agent\agent_factory.py

    def test_default_agent_runnable():
        inputs = {
            "table": "web_site",
            "field": "web_suite_number",
            FIELD_VALIDATION_SQL_HISTORY: "",
            FIELD_CHAT_HISTORY: [],
            "intermediate_steps": [],
        }
        res = agent_runnable.invoke(inputs)
        print(res)

    def test_numeric_agent_runnable():
        inputs = {
            "table": "call_center",
            "field": "cc_tax_percentage",
            FIELD_VALIDATION_SQL_HISTORY: "",
            FIELD_CHAT_HISTORY: [],
            "intermediate_steps": [],
        }
        res = agent_runnable.invoke(inputs)
        print(res)

    # test_default_agent_runnable()
    test_numeric_agent_runnable()
