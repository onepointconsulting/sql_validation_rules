from sqlalchemy.orm import sessionmaker

from sql_validation_rules.persistence.sql_rules import SQLRule
from sql_validation_rules.persistence.db_connection_factory import sql_db_write_factory
from sql_validation_rules.config.log_factory import logger


def save_sql_rule(sql_rule: SQLRule):
    try:
        engine, _ = sql_db_write_factory()
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(sql_rule)
            session.commit()
    except Exception as e:
        logger.exception("Cannot insert record in database")


if __name__ == "__main__":
    # Quick check to see if DB is working.
    sql_rule = SQLRule(
        table="test", column="test_col", sql="select * from test", title="Just testing"
    )
    save_sql_rule(sql_rule)
