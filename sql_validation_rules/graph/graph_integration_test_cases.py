from typing import Dict
from sql_validation_rules.config.log_factory import logger
from sql_validation_rules.graph.graph_factory import workflow, app
from sql_validation_rules.graph.graph_utils import stream_outputs
from sql_validation_rules.agent.agent_state import FIELD_VALIDATION_SQL_HISTORY


def log_workflow_properties():
    logger.info(workflow.branches)
    logger.info("Nodes: %s", workflow.nodes)
    logger.info("Edges: %s", workflow.edges)
    logger.info(workflow.channels)


def invoke(inputs: Dict[str, any]) -> Dict[str, any]:
    return app.invoke(inputs)


if __name__ == "__main__":

    from pathlib import Path

    inputs_list = [
        {
            "table": "web_site",
            "field": "web_zip",
            "chat_history": [],
            FIELD_VALIDATION_SQL_HISTORY: [],
        },
        {
            "table": "web_site",
            "field": "web_street_type",
            "chat_history": [],
            FIELD_VALIDATION_SQL_HISTORY: [],
        },
        {
            "table": "web_site",
            "field": "web_company_name",
            "chat_history": [],
            FIELD_VALIDATION_SQL_HISTORY: [],
        },
        {
            "table": "web_site",
            "field": "web_suite_number",
            "chat_history": [],
            FIELD_VALIDATION_SQL_HISTORY: [],
        },
        {
            "table": "web_site",
            "field": "web_site_id",
            "chat_history": [],
            FIELD_VALIDATION_SQL_HISTORY: [],
        },
    ]

    output_file = Path("integration_test_cases_out.txt")

    with open(output_file, "w") as f:
        for inputs in inputs_list:
            f.write(f"\n\n# {inputs['table']} - {inputs['field']}\n")
            for content in stream_outputs(inputs):
                f.write("\n -------------------- \n")
                f.write(f"{content}")
