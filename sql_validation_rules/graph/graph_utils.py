from typing import Dict
from sql_validation_rules.graph.graph_factory import app


def stream_outputs(inputs: Dict[str, any]):
    for s in app.stream(inputs):
        content = list(s.values())[0]
        yield content
