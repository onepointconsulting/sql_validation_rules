from typing import List

from sql_validation_rules.test.provider.supervisor_prompt_provider import (
    create_until_no_more_meaningful,
    create_until_repeat_cc_tax_percentage,
)
from sql_validation_rules.config.log_factory import logger
from sql_validation_rules.config.config import cfg
from sql_validation_rules.graph.supervisor_graph_factory import create_supervisor_app
from sql_validation_rules.chain.sql_commands import SQLCommand
from sql_validation_rules.graph.graph_utils import (
    message_extractor,
    create_human_message,
    create_supervisor_message,
)
from sql_validation_rules.observability.langfuse_factory import create_langfuse_handler


if __name__ == "__main__":
    langfuse_handler = create_langfuse_handler()

    workflow, supervisor_app = create_supervisor_app()
    print("app created")

    config = {
        "recursion_limit": cfg.recursion_limit,
        "callbacks": [langfuse_handler] if cfg.langfuse_config.langfuse_tracing else [],
    }

    def stream_supervisor_app(input: str):
        for s in supervisor_app.stream(input, config=config):
            if "__end__" not in s:
                print(s)
                print("----")

    def invoke_app(input: str) -> List[SQLCommand]:
        res = supervisor_app.invoke(input, config=config)
        print("*****************************************")
        print(res)
        return message_extractor(res)

    def print_commands(commands: SQLCommand):
        for command in commands:
            print("--   Command   --")
            print(command)
            print("-- End Command --")

    def execute_test(prompt: str):
        input = create_human_message(prompt)
        commands = invoke_app(input)
        print_commands(commands)

    def create_unspecified_rules():
        execute_test(create_until_no_more_meaningful())

    def figure_out_type():
        execute_test(create_until_repeat_cc_tax_percentage())

    def specify_type():
        execute_test(create_supervisor_message("call_center", "cc_tax_percentage"))

    specify_type()
