from typing import Dict, Union, Any
from sql_validation_rules.graph.graph_factory import app
from langgraph.graph.graph import CompiledGraph


def stream_outputs(inputs: Dict[str, any], app: CompiledGraph = app):
    for s in app.stream(inputs):
        content = list(s.values())[0]
        yield content


def invoke_app(inputs: Dict[str, any]) -> Union[dict[str, Any], Any]:
    return app.invoke(inputs)
