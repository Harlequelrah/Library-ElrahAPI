from sqlalchemy import create_engine,text


def create_database_if_not_exists(database_url, database_name):
    engine = create_engine(database_url, pool_pre_ping=True)
    conn = engine.connect()
    try:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
    finally:
        conn.close()


