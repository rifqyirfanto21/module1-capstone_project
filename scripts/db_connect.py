from sqlalchemy import create_engine
from config.setting import DB_CONFIG

def get_db_connection():
    host = DB_CONFIG["host"]
    port = DB_CONFIG["port"]
    database = DB_CONFIG["database"]
    user = DB_CONFIG["user"]
    password = DB_CONFIG["password"]

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
    return engine