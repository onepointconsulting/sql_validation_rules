from typing import List, Dict, Union, Any
from sql_validation_rules.graph.graph_factory import app
from langgraph.graph.graph import CompiledGraph
from sql_validation_rules.chain.sql_commands import SQLCommand
from sql_validation_rules.config.log_factory import logger


def stream_outputs(inputs: Dict[str, any], app: CompiledGraph = app):
    for s in app.stream(inputs):
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
