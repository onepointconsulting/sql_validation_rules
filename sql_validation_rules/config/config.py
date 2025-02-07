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


class WriteDBConfig:
    db_url = os.getenv("WRITE_DB_URL")
    db_schema = os.getenv("WRITE_DB_SCHEMA")


class LangfuseConfig:
    langfuse_tracing = os.getenv("LANGFUSE_TRACING") == "true"
    langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_host = os.getenv("LANGFUSE_HOST")


class WriteDBConfig:
    db_url = os.getenv("WRITE_DB_URL")
    db_schema = os.getenv("WRITE_DB_SCHEMA")


class LangfuseConfig:
    langfuse_tracing = os.getenv("LANGFUSE_TRACING") == "true"
    langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_host = os.getenv("LANGFUSE_HOST")


class WriteDBConfig:
    db_url = os.getenv("WRITE_DB_URL")
    db_schema = os.getenv("WRITE_DB_SCHEMA")


class LangfuseConfig:
    langfuse_tracing = os.getenv("LANGFUSE_TRACING") == "true"
    langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_host = os.getenv("LANGFUSE_HOST")


class WriteDBConfig:
    db_url = os.getenv("WRITE_DB_URL")
    db_schema = os.getenv("WRITE_DB_SCHEMA")


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
    db_config = DBConfig()
    langfuse_config = LangfuseConfig()
    write_db_config = WriteDBConfig()

    langsmith_project_url = os.getenv("LANGSMITH_PROJECT_URL")


cfg = Config()

if __name__ == "__main__":
    assert cfg.db_config.host is not None
    logger.info(f"Using host: {cfg.db_config.host}")
    logger.info(f"Using db_type: {cfg.db_config.db_type}")
    assert cfg.db_config.host is not None
    logger.info(f"Using host: {cfg.db_config.host}")
    logger.info(f"Using db_type: {cfg.db_config.db_type}")
