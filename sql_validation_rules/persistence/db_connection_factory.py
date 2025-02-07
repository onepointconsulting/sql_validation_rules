from typing import Tuple

from langchain.sql_database import SQLDatabase
from snowflake.sqlalchemy import URL as SF_URL
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from sql_validation_rules.config.config import cfg

def sql_db_factory() -> SQLDatabase:
    db_config = cfg.db_config

    if db_config.db_type == 'snowflake':
        url = SF_URL(
            account=db_config.account,
            user=db_config.user,
            password=db_config.password,
            database=db_config.database,
            schema=db_config.schema,
            warehouse=db_config.warehouse,
            host=db_config.host,
        )
    elif db_config.db_type == 'postgres':
        url = URL.create(
            drivername='postgresql+psycopg2',
            username=db_config.user,
            password=db_config.password,
            host=db_config.host,
            port=db_config.port,
            database=db_config.database
        )
    else:
        raise ValueError("Unsupported database type!")
    
    engine = create_engine(url)
    return SQLDatabase(engine=engine, schema=db_config.schema, lazy_table_reflection=True)



def sql_db_write_factory() -> Tuple[Engine, SQLDatabase]:
    write_db_config = cfg.write_db_config
    engine = create_engine(write_db_config.db_url)
    return engine, SQLDatabase(
        engine=engine, schema=write_db_config.db_schema, lazy_table_reflection=True
    )


if __name__ == "__main__":
    from sql_validation_rules.config.log_factory import logger

    logger.info("sql_db_factory")
    sql_database = sql_db_factory()
    logger.info("sql_database %s", sql_database)

    logger.info("sql_db_write_factory")
    engine, write_db = sql_db_write_factory()
    logger.info(type(engine))
    logger.info("write_db %s", write_db)
