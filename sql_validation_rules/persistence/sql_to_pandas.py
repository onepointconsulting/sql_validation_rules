import pandas as pd

from sql_validation_rules.persistence.db_connection_factory import read_engine_factory


def execute_read_sql_as_df(query: str, limit: int = 100) -> pd.DataFrame:
    engine = read_engine_factory()
    with engine.connect() as connection:
        resultset = connection.execute(query)
        results_as_dict = resultset.mappings().all()
        df = pd.DataFrame(results_as_dict)
        return df[:limit]


if __name__ == "__main__":
    df = execute_read_sql_as_df(
        """SELECT c_salutation
FROM customer
WHERE c_salutation IS NOT NULL
LIMIT 1000;""",
    )
    print(df.shape)
