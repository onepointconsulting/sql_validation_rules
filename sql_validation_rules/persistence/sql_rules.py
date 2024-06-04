from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Define the base class for declarative models
Base = declarative_base()


# Define a User class that will be mapped to a users table in the database
class SQLRule(Base):
    __tablename__ = "sql_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    table = Column(String)
    column = Column(String)
    sql = Column(String)
    title = Column(String)
    create_timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )


if __name__ == "__main__":
    from sql_validation_rules.persistence.db_connection_factory import sql_db_write_factory

    engine, _ = sql_db_write_factory()

    Base.metadata.create_all(engine)
