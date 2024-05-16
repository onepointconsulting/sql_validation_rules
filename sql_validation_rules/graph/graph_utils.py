from typing import List, Dict, Union, Any
from typing import Dict, Any, Generator

from langgraph.graph.graph import CompiledGraph
from langchain_core.messages import HumanMessage

from sql_validation_rules.graph.graph_factory import app
from sql_validation_rules.chain.sql_commands import SQLCommand
from sql_validation_rules.config.log_factory import logger
from sql_validation_rules.config.toml_support import prompts


def stream_outputs(
    inputs: Dict[str, any],
    config: dict,
    app: CompiledGraph = app,
) -> Generator[Any, None, None]:
    for s in app.stream(inputs, config=config):
        content = list(s.values())[0]
        yield content


def invoke_app(inputs: Dict[str, any]) -> Union[dict[str, Any], Any]:
    return app.invoke(inputs)


def message_extractor(agent_result: dict) -> List[SQLCommand]:
    if "messages" in agent_result:
        messages = agent_result["messages"]
        if len(messages) > 1:
            results = []
            for r in messages[1:]:
                try:
                    results.append(SQLCommand.parse_raw(r.content))
                except Exception as e:
                    logger.exception(f"Cannot extract {r.content}")
            return results
    return []


def create_human_message(input_str: str) -> dict:
    return {"messages": [HumanMessage(content=input_str)]}


def create_supervisor_message(table: str, column: str) -> dict:
    initial_message = prompts["sql_validation"]["supervisor"]["initial"]["human_message"]
    return initial_message.format(table=table, column=column)
