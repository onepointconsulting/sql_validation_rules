from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

from sql_validation_rules.config.toml_support import prompts
from sql_validation_rules.config.config import cfg
from sql_validation_rules.chain.sql_commands import SQLCommands


def prompt_factory_extract_sql_statements() -> ChatPromptTemplate:
    extraction_prompts = prompts["sql_validation"]["extract_sql"]
    return ChatPromptTemplate.from_messages(
        [
            ("system", extraction_prompts["system_message"]),
            ("human", extraction_prompts["human_message"]),
        ]
    )


def chain_factory_extract_sql_statements() -> LLMChain:
    return create_structured_output_chain(
        SQLCommands,
        cfg.llm,
        prompt_factory_extract_sql_statements(),
        verbose=cfg.verbose_llm,
    )


extraction_chain = chain_factory_extract_sql_statements()

if __name__ == "__main__":

    res = extraction_chain.invoke(
        """
The tool result is The provided Snowflake SQL query seems to be correct based on the requirements listed. It is using the REGEXP_LIKE function to filter out rows where the web_zip column does not match the regular expression for a standard 5-digit ZIP code or a ZIP+4 code. There are no apparent mistakes related to the common issues listed, such as using NOT IN with NULL values, UNION vs. UNION ALL, BETWEEN for exclusive ranges, data type mismatches, quoting identifiers, incorrect function arguments, casting, or join column issues.

Here is the original query:

```sql
SELECT web_site_sk, web_zip
FROM web_site
WHERE NOT REGEXP_LIKE(web_zip, '^[0-9]{5}(-[0-9]{4})?$');
```
"""
    )
    sql_commands: SQLCommands = res["function"]
    print(sql_commands.validation_commands)
