import psycopg2

"""Helper functions to manage database connections and queries."""

def execute_query(query, params=None, fetchone=False, fetchall=False):
    """Helper function to execute a query with automatic connection and cursor management."""
    with psycopg2.connect(database="postgres", user="postgres", password="datadatabejs", host="localhost", port="5432") as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            conn.commit()  # Commit if it's an insert/update/delete query