from sqlalchemy import create_engine

def create_database_if_not_exists(database_url, database_name):
    engine = create_engine(database_url, echo=True)
    conn = engine.connect()
    try:
        conn.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    except Exception as e:
        pass
    finally:
        conn.close()
        return f"{database_url}/{database_name}"
