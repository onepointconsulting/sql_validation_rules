from typing import Tuple

from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph

from sql_validation_rules.tools.sql_tools import (
    sql_list_tables,
    sql_info_tables,
    sql_query,
    sql_query_checker,
)
from sql_validation_rules.agent.agent_factory import agent_runnable
from sql_validation_rules.config.log_factory import logger
from sql_validation_rules.agent.agent_state import (
    AgentState,
    INTERMEDIATE_STEPS,
    AGENT_OUTCOME,
    EXTRACTION_CONTENT,
)
from sql_validation_rules.chain.command_extraction_factory import extraction_chain
from sql_validation_rules.chain.sql_commands import SQLCommands


AGENT = "agent"
ACTION = "action"
EXTRACTION = "extraction"


def create_tool_executor():
    return ToolExecutor(
        [sql_list_tables, sql_info_tables, sql_query, sql_query_checker]
    )


tool_executor = create_tool_executor()


def execute_tools(data):
    """Define the function call to execute tools"""
    agent_action = data[AGENT_OUTCOME]
    output = tool_executor.invoke(agent_action)
    logger.info(f"The agent action is {agent_action}")
    logger.info(f"The tool result is {output}")
    return {INTERMEDIATE_STEPS: [(agent_action, str(output))]}


def should_continue(data):
    """Define logic that will be used to determine which conditional edge to go down."""
    if isinstance(data[AGENT_OUTCOME], AgentFinish):
        return "end"
    return "continue"


def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {AGENT_OUTCOME: agent_outcome}


def run_extraction(data):
    agent_outcome = data["agent_outcome"]
    if isinstance(agent_outcome, AgentFinish):
        output = agent_outcome.return_values["output"]
        outcome = extraction_chain.invoke(output)
        sql_commands: SQLCommands = outcome["function"]
        return {EXTRACTION_CONTENT: sql_commands.validation_commands}
    else:
        return {EXTRACTION_CONTENT: "No results"}


def build_workflow(workflow: StateGraph):
    workflow.add_node(AGENT, run_agent)  # LLM
    workflow.add_node(ACTION, execute_tools)  # SQL tools
    workflow.add_node(EXTRACTION, run_extraction)  # Extraction

    workflow.set_entry_point(AGENT)

    workflow.add_edge(ACTION, AGENT)
    workflow.add_conditional_edges(
        AGENT, should_continue, {"continue": ACTION, "end": EXTRACTION}
    )
    workflow.add_edge(EXTRACTION, END)


def create_app() -> Tuple[StateGraph, CompiledGraph]:
    workflow = StateGraph(AgentState)
    build_workflow(workflow)

    return workflow, workflow.compile()


workflow, app = create_app()
