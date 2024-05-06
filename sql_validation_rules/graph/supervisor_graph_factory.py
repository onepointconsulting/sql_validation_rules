from typing import Tuple, List
import functools

from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from langchain_core.agents import AgentFinish

from sql_validation_rules.agent.agent_state import AgentState, AGENT_OUTCOME
from sql_validation_rules.agent.supervisor_factory import (
    create_supervisor_chain,
    supervisor_members,
    FINISH,
)
from sql_validation_rules.graph.graph_factory import create_app
from sql_validation_rules.chain.sql_commands import SQLCommand


SUPERVISOR = "supervisor"


def create_if_missing(state: dict, key: str):
    if state[key] == None:
        state[key] = []


def agent_node(state: dict, agent: CompiledGraph, name: str):
    create_if_missing(state, "chat_history")
    create_if_missing(state, "intermediate_steps")
    result = agent.invoke(state)
    content = "Failed to execute agent"
    if (
        isinstance(result[AGENT_OUTCOME], AgentFinish)
        and "extraction_content" in result
    ):
        content = ""
        sql_commands: List[SQLCommand] = result["extraction_content"]
        for sql_command in sql_commands:
            content += sql_command.json()
    return {"messages": [HumanMessage(content=content, name=name)]}


def create_supervisor_app() -> Tuple[StateGraph, CompiledGraph]:
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node(SUPERVISOR, create_supervisor_chain())
    agent_name = supervisor_members[0]
    _, agent_app = create_app()
    sql_validator_node = functools.partial(agent_node, agent=agent_app, name=agent_name)
    workflow.add_node(agent_name, sql_validator_node)

    # Edges

    # for member in supervisor_members:
    #     # We want our workers to ALWAYS "report back" to the supervisor when done
    #     workflow.add_edge(member, SUPERVISOR)  # add one edge for each of the agents
    conditional_map = {k: k for k in supervisor_members}
    conditional_map[FINISH] = END
    workflow.add_conditional_edges(SUPERVISOR, lambda x: x["next"], conditional_map)
    workflow.add_edge(agent_name, SUPERVISOR)

    workflow.set_entry_point(SUPERVISOR)

    return workflow, workflow.compile()


if __name__ == "__main__":
    workflow, app = create_supervisor_app()
    print("app created")

    prompt1 = """Please extract 2 SQL validation rules for column web_suite_number in table web_site."""
    prompt2 = """Please extract SQL validation rules for column web_suite_number in table web_site as long as new ones can be found. 
When you cannot find new ones stop"""
    prompt3 = """Please extract SQL validation rules for column web_suite_number in table web_site as long as you can generate more meaningful rules. Stop when there are no more meaningful rules to generate on this field."""
    prompt4 = """Please extract SQL validation rules for column web_suite_number in table web_site 
as long as you can generate more meaningful rules. Stop when there are no more meaningful rules to generate on this field."""

    config = {"recursion_limit": 20}
    input = {"messages": [HumanMessage(content=prompt2)]}

    def message_extractor(agent_result: dict) -> List[SQLCommand]:
        if "messages" in agent_result:
            messages = agent_result["messages"]
            if len(messages) > 1:
                return [SQLCommand.parse_raw(r.content) for r in messages[1:]]
        return []

    def stream_app():
        for s in app.stream(input, config=config):
            if "__end__" not in s:
                print(s)
                print("----")

    def invoke_app() -> List[SQLCommand]:
        res = app.invoke(input, config=config)
        print("*****************************************")
        print(res)
        return message_extractor(res)

    commands = invoke_app()
    for command in commands:
        print(command)
