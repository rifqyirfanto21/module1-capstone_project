import pandas as pd
from scripts.db_connect import get_db_connection
from sqlalchemy import text

#Connect Dataframe to PostgreSQL DB
def load_to_postgres(df, table_name, if_exists="append"):
    engine = get_db_connection()
    
    with engine.connect() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        conn.commit()
    
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    print(f"Data loaded to table {table_name} successfully (table truncated first).")