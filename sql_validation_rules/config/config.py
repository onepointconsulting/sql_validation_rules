from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI

from sql_validation_rules.config.log_factory import logger


load_dotenv()

from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI

from sql_validation_rules.config.log_factory import logger


load_dotenv()


class DBConfig:
    db_type = os.getenv("DB_TYPE")
    account = os.getenv("DB_ACCOUNT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")
    schema = os.getenv("DB_SCHEMA")
    warehouse = os.getenv("DB_WAREHOUSE")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

# class SnowflakeConfig:
#     snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
#     snowflake_user = os.getenv("SNOWFLAKE_USER")
#     snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")
#     snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
#     snowflake_schema = os.getenv("SNOWFLAKE_SCHEMA")
#     snowflake_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
#     snowflake_host = os.getenv("SNOWFLAKE_HOST")


class Config:
    project_root = Path(os.getenv("PROJECT_ROOT", "/home/ubuntu"))
    assert project_root.exists(), f"{project_root} does not exist."

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo-1106"),
        temperature=float(os.getenv("OPENAI_API_TEMPERATURE")),
    )
    verbose_llm = bool(os.getenv("VERBOSE_LLM", "True"))
    #snowflake_config = SnowflakeConfig()
    db_config = DBConfig()


cfg = Config()

# if __name__ == "__main__":
#     assert cfg.snowflake_config.snowflake_account is not None
#     logger.info(f"Using account: {cfg.snowflake_config.snowflake_account}")

if __name__ == "__main__":
    assert cfg.db_config.host is not None
    logger.info(f"Using host: {cfg.db_config.host}")
    logger.info(f"Using db_type: {cfg.db_config.db_type}")