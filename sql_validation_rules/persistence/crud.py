from sql_validation_rules.persistence.sql_rules import SQLRule
from sql_validation_rules.db_connection_factory import sql_db_write_factory
from sqlalchemy.orm import sessionmaker


def save_sql_rule(sql_rule: SQLRule):
    engine, _ = sql_db_write_factory()
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(sql_rule)
        session.commit()


if __name__ == "__main__":
    # Quick check to see if DB is working.
    sql_rule = SQLRule(
        table="test", column="test_col", sql="select * from test", title="Just testing"
    )
    save_sql_rule(sql_rule)
