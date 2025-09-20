import os
from config.setting import OUTPUT_PATH_DIR
from scripts.db_connect import get_db_connection
from sqlalchemy import text

#Connect Dataframe to PostgreSQL DB
def load_to_postgres(df, table_name, if_exists="append"):
    """
    Load Dataframe to PostgreSQL database
    """
    engine = get_db_connection()
    
    with engine.connect() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        conn.commit()
    
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    print(f"Data loaded to table {table_name} successfully (table truncated first).")

def save_to_csv(df, filename):
    """
    Save dataframe to CSV in the config output directory
    """
    os.makedirs(OUTPUT_PATH_DIR, exist_ok=True)
    
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    full_path = os.path.join(OUTPUT_PATH_DIR, filename)
    
    df.to_csv(full_path, index=False)
    print(f"DataFrame saved to: {full_path}")