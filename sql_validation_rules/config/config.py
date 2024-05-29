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


class LangfuseConfig:
    langfuse_tracing = os.getenv("LANGFUSE_TRACING") == "true"
    langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_host = os.getenv("LANGFUSE_HOST")


class Config:
    project_root = Path(os.getenv("PROJECT_ROOT", "/home/ubuntu"))
    assert project_root.exists(), f"{project_root} does not exist."

    model = os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo-1106")
    logger.info(f"model: {model}")
    llm = ChatOpenAI(
        model=model,
        temperature=float(os.getenv("OPENAI_API_TEMPERATURE")),
    )
    verbose_llm = bool(os.getenv("VERBOSE_LLM", "True"))
    recursion_limit = int(os.getenv("RECURSION_LIMIT", "20"))
    snowflake_config = SnowflakeConfig()
    langfuse_config = LangfuseConfig()

    langsmith_project_url = os.getenv("LANGSMITH_PROJECT_URL")


cfg = Config()

if __name__ == "__main__":
    assert cfg.snowflake_config.snowflake_account is not None
    logger.info(f"Using account: {cfg.snowflake_config.snowflake_account}")
