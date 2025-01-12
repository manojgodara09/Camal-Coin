import os
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text

# Cloud SQL connection configuration
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "ramji-445410:asia-south2:testdata")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Ramram#123")
DB_NAME = os.getenv("DB_NAME", "testdata")

def get_db_connection():
    connector = Connector()
    
    def getconn():
        conn = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )
        return conn

    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return engine

def init_db():
    engine = get_db_connection()
    with engine.connect() as conn:
        # Create user_data table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_data (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                balance FLOAT NOT NULL,
                add_bal FLOAT NOT NULL,
                token TEXT
            )
        """))
        
        # Create user_game_history table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_game_history (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                game_name TEXT NOT NULL,
                before_balance FLOAT NOT NULL,
                after_balance FLOAT NOT NULL,
                multiplier FLOAT NOT NULL,
                play_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_data (id) ON DELETE CASCADE
            )
        """))
        conn.commit()

if __name__ == "__main__":
    init_db()
