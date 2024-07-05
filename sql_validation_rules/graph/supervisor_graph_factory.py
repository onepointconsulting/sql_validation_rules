from typing import Tuple, List
import functools

from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from langchain_core.runnables.base import RunnableSequence
from langchain_core.agents import AgentFinish

from sql_validation_rules.agent.agent_state import AgentState, AGENT_OUTCOME
from sql_validation_rules.agent.supervisor_factory import (
    create_supervisor_chain,
    supervisor_members,
    FINISH,
)
from sql_validation_rules.graph.graph_factory import (
    create_app,
    agent_runnable,
    agent_runnable_numeric,
)
from sql_validation_rules.chain.sql_commands import SQLCommands
from sql_validation_rules.tools.sql_tools import create_table_info_runnable_sequence


SUPERVISOR = "supervisor"


def create_if_missing(state: dict, key: str):
    if state[key] == None:
        state[key] = []


def agent_node(state: dict, agent: CompiledGraph, name: str) -> dict:
    create_if_missing(state, "chat_history")
    create_if_missing(state, "intermediate_steps")
    result = agent.invoke(state)
    content = "Failed to execute agent"
    if (
        isinstance(result[AGENT_OUTCOME], AgentFinish)
        and "extraction_content" in result
    ):
        sql_commands: SQLCommands = result["extraction_content"]
        content = sql_commands.json()
    return {"messages": [HumanMessage(content=content, name=name)]}


def runnable_sequence_node(state: dict, tool: RunnableSequence, name: str):
    create_if_missing(state, "chat_history")
    create_if_missing(state, "intermediate_steps")
    result = tool.invoke(state)
    return {"messages": [HumanMessage(content=str(result), name=name)]}


def create_supervisor_app() -> Tuple[StateGraph, CompiledGraph]:
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node(SUPERVISOR, create_supervisor_chain())
    # Setup the agents
    agent_names = [sm for sm in supervisor_members if not "tool" in sm]
    for agent_name, runnable in zip(
        agent_names, [agent_runnable, agent_runnable_numeric]
    ):
        _, agent_app = create_app(runnable)
        sql_validator_node = functools.partial(
            agent_node, agent=agent_app, name=agent_name
        )
        workflow.add_node(agent_name, sql_validator_node)

    # Set up the tools
    tool_names = [sm for sm in supervisor_members if "tool" in sm]
    for tool_name, runnable in zip(tool_names, [create_table_info_runnable_sequence()]):
        tool_node = functools.partial(
            runnable_sequence_node, tool=runnable, name=tool_name
        )
        workflow.add_node(tool_name, tool_node)

    # Edges

    # for member in supervisor_members:
    #     # We want our workers to ALWAYS "report back" to the supervisor when done
    #     workflow.add_edge(member, SUPERVISOR)  # add one edge for each of the agents
    conditional_map = {k: k for k in supervisor_members}
    conditional_map[FINISH] = END
    workflow.add_conditional_edges(SUPERVISOR, lambda x: x["next"], conditional_map)
    for agent_name in supervisor_members:
        workflow.add_edge(agent_name, SUPERVISOR)

    workflow.set_entry_point(SUPERVISOR)

    return workflow, workflow.compile()
