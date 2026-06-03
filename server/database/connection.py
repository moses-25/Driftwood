from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

if db_url:
    engine = create_engine(db_url)
else:
    engine = None


def test_database_connection():
    try:
        if engine is None:
            print("No DATABASE_URL configured, skipping connection test.")
            return True
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connected successfully!")
            return True
    except Exception as error:
        print("Database connection failed!")
        print(f"Error: {error}")
        return False
