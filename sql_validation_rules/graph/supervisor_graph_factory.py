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
from sql_validation_rules.graph.graph_factory import create_app, agent_runnable, agent_runnable_numeric
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
    for agent_name, runnable in zip(supervisor_members, [agent_runnable, agent_runnable_numeric]):
        _, agent_app = create_app(runnable)
        sql_validator_node = functools.partial(agent_node, agent=agent_app, name=agent_name)
        workflow.add_node(agent_name, sql_validator_node)

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


if __name__ == "__main__":
    
    from sql_validation_rules.test.provider.supervisor_prompt_provider import create_until_repeat_cc_tax_percentage

    workflow, supervisor_app = create_supervisor_app()
    print("app created")

    config = {"recursion_limit": 20}
    input = {"messages": [HumanMessage(content=create_until_repeat_cc_tax_percentage())]}

    def message_extractor(agent_result: dict) -> List[SQLCommand]:
        if "messages" in agent_result:
            messages = agent_result["messages"]
            if len(messages) > 1:
                return [SQLCommand.parse_raw(r.content) for r in messages[1:]]
        return []

    def stream_app():
        for s in supervisor_app.stream(input, config=config):
            if "__end__" not in s:
                print(s)
                print("----")

    def invoke_app() -> List[SQLCommand]:
        res = supervisor_app.invoke(input, config=config)
        print("*****************************************")
        print(res)
        return message_extractor(res)

    # commands = invoke_app()
    # for command in commands:
    #     print(command)

    stream_app()
