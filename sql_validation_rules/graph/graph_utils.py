from typing import List, Dict, Union, Any
from typing import Dict, Any, Generator

from langgraph.graph.graph import CompiledGraph
from langchain_core.messages import HumanMessage

from sql_validation_rules.graph.graph_factory import app
from sql_validation_rules.chain.sql_commands import SQLCommand, SQLCommands
from sql_validation_rules.config.log_factory import logger
from sql_validation_rules.config.config import cfg
from sql_validation_rules.config.toml_support import prompts
from sql_validation_rules.graph.supervisor_graph_factory import create_supervisor_app
from sql_validation_rules.observability.langfuse_factory import create_langfuse_handler


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
    initial_message = prompts["sql_validation"]["supervisor"]["initial"][
        "human_message"
    ]
    return initial_message.format(table=table, column=column)


def invoke_column_rule(table: str, column: str, config: dict):
    inputs = create_human_message(create_supervisor_message(table, column))
    _, supervisor_app = create_supervisor_app()
    res = supervisor_app.invoke(inputs, config=config)
    return res


def extract_sql_command(messages: list) -> List[SQLCommand]:
    if len(messages) > 0 and len(messages[-1].content) > 0:
        acc = []
        for message in messages[1:]:
            try:
                sql_commands = SQLCommands.parse_raw(message.content)
                acc.extend(sql_commands.validation_commands)
            except Exception as e:
                logger.exception(
                    f"Could not extract sql command from {message.content}: {e}"
                )
        return acc
    return []


def convert_sql_command_to_str(sql_commands: List[SQLCommand]) -> str:
    acc = ""
    for c in sql_commands:
        acc += sql_command_to_str(c)
    return acc


def sql_command_to_str(sql_command: SQLCommand) -> str:
    return f"""
### {sql_command.validation_type}

{sql_command.reasoning}

```sql
{sql_command.validation_command}
```
"""


def generate_supervisor_config() -> dict:
    langfuse_handler = create_langfuse_handler()
    return {
        "recursion_limit": cfg.recursion_limit,
        "callbacks": [langfuse_handler] if cfg.langfuse_config.langfuse_tracing else [],
    }
