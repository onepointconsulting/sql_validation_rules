from sql_validation_rules.graph.graph_factory import app_numeric
from sql_validation_rules.agent.agent_state import (
    FIELD_VALIDATION_SQL_HISTORY,
    FIELD_CHAT_HISTORY,
)
from sql_validation_rules.graph.graph_integration_test_cases import execute_inputs

if __name__ == "__main__":
    from pathlib import Path

    inputs_list = [
        {
            "table": "call_center",
            "field": "cc_tax_percentage",
            FIELD_CHAT_HISTORY: [],
            FIELD_VALIDATION_SQL_HISTORY: [],
        }
    ]

    output_file = Path("integration_numeric_test_cases_out.txt")
    execute_inputs(inputs_list, output_file, app_numeric)
