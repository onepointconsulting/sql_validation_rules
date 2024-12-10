from langchain.sql_database import SQLDatabase
from snowflake.sqlalchemy import URL as SF_URL
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

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
    

    #snowflake_config = cfg.snowflake_config
    #schema = snowflake_config.snowflake_schema
    engine = create_engine(url)
    
    return SQLDatabase(engine=engine, schema=db_config.schema, lazy_table_reflection=True)


if __name__ == "__main__":

    from sql_validation_rules.config.log_factory import logger

    logger.info("sql_db_factory")
    sql_database = sql_db_factory()
    logger.info("sql_database %s", sql_database)
