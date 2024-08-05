import duckdb

def create_connection():
    conn = duckdb.connect(database='my.db')
    return conn