import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'onepoint_admin',
    'password': '2Q8j9&$26YAR',
    'host': 'op-training-postgresql-server.postgres.database.azure.com',  # or your database host
    'port': '5432'        # default PostgreSQL port
}

conn = None
cur = None

try:
    # Establishing the connection
    conn = psycopg2.connect(**db_params)
    print("Connected to the database!")

    # Creating a cursor object using the cursor() method
    cur = conn.cursor()

    # Execute a simple query
    cur.execute("SELECT version();")

    # Fetch and print the result of the query
    db_version = cur.fetchone()
    print("Database version:", db_version)

except Exception as e:
    print("Error while connecting to PostgreSQL", e)

finally:
    # Closing the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()

        