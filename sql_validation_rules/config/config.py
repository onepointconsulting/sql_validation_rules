from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI

from sql_validation_rules.config.log_factory import logger


load_dotenv()


class SnowflakeConfig:
    snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
    snowflake_user = os.getenv("SNOWFLAKE_USER")
    snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")
    snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
    snowflake_schema = os.getenv("SNOWFLAKE_SCHEMA")
    snowflake_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    snowflake_host = os.getenv("SNOWFLAKE_HOST")


class Config:
    project_root = Path(os.getenv("PROJECT_ROOT", "/home/ubuntu"))
    assert project_root.exists(), f"{project_root} does not exist."

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo-1106"),
        temperature=float(os.getenv("OPENAI_API_TEMPERATURE")),
    )
    verbose_llm = bool(os.getenv("VERBOSE_LLM", "True"))
    snowflake_config = SnowflakeConfig()


cfg = Config()

if __name__ == "__main__":
    assert cfg.snowflake_config.snowflake_account is not None
    logger.info(f"Using account: {cfg.snowflake_config.snowflake_account}")
