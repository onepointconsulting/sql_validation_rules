from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from sql_validation_rules.config.toml_support import prompts
from sql_validation_rules.config.config import cfg

FUNCTION_NAME = "route"
FINISH = "FINISH"

VALIDATOR_MAIN_VALIDATOR = "SQL_Validator"
VALIDATOR_SQL_NUMERIC_VALIDATOR = "SQL_Numeric_Statistical_Validator"

supervisor_members = [
    VALIDATOR_MAIN_VALIDATOR,
    VALIDATOR_SQL_NUMERIC_VALIDATOR,
    "Table_column_tool",
]

options = [FINISH] + supervisor_members

function_def = {
    "name": FUNCTION_NAME,
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {
            "next": {
                "title": "Next",
                "anyOf": [
                    {"enum": options},
                ],
            },
            "table": {
                "title": "Table",
                "type": "string",
                "description": "The database table",
            },
            "field": {
                "title": "Field",
                "type": "string",
                "description": "The field of the database table",
            },
        },
        "required": ["next", "table", "field"],
    },
}


def create_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", prompts["sql_validation"]["supervisor"]["system_message"]),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next? Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join(supervisor_members))


def create_supervisor_chain():
    return (
        create_prompt()
        | cfg.llm.bind_functions(functions=[function_def], function_call=FUNCTION_NAME)
        | JsonOutputFunctionsParser()
    )


if __name__ == "__main__":
    supervisor_prompt = create_prompt()
    print(supervisor_prompt)
    print(
        supervisor_prompt.format(
            messages=[
                "Please extract 3 SQL validation rules for column web_suite_number in table web_site."
            ]
        )
    )
