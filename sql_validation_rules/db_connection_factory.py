from langchain.sql_database import SQLDatabase
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

from sql_validation_rules.config.config import cfg


def sql_db_factory() -> SQLDatabase:
    snowflake_config = cfg.snowflake_config
    schema = snowflake_config.snowflake_schema
    engine = create_engine(
        URL(
            account=snowflake_config.snowflake_account,
            user=snowflake_config.snowflake_user,
            password=snowflake_config.snowflake_password,
            database=snowflake_config.snowflake_database,
            schema=schema,
            warehouse=snowflake_config.snowflake_warehouse,
            host=snowflake_config.snowflake_host,
        )
    )
    return SQLDatabase(engine=engine, schema=schema, lazy_table_reflection=True)


if __name__ == "__main__":

    from sql_validation_rules.config.log_factory import logger

    logger.info("sql_db_factory")
    sql_database = sql_db_factory()
    logger.info("sql_database %s", sql_database)
