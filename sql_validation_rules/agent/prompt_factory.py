from langchain_core.prompts import ChatPromptTemplate
from sql_validation_rules.config.toml_support import prompts


def create_sql_validation_template() -> ChatPromptTemplate:
    return create_template_helper("main")


def create_sql_validation_numeric_template() -> ChatPromptTemplate:
    return create_template_helper("numeric_field")


def create_template_helper(key: str) -> ChatPromptTemplate:
    main_prompts = prompts["sql_validation"][key]
    return ChatPromptTemplate.from_messages(
        [
            ("system", main_prompts["system_message"]),
            # Means the template will receive an optional list of messages under
            # the "placeholder" key
            ("placeholder", "{chat_history}"),
            ("human", main_prompts["human_message"]),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )


prompt_template = create_sql_validation_template()
