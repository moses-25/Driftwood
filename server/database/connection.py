from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database credentials
DB_USER = "postgres"
DB_PASSWORD = "ochiengmose"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "driftwood_cafe"

# PostgreSQL connection URL
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create engine
engine = create_engine(DATABASE_URL)


def test_database_connection():
    """
    Test if PostgreSQL database connection works.
    Returns True if successful, False otherwise.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Database connected successfully!")
            return True

    except Exception as error:
        print("❌ Database connection failed!")
        print(f"Error: {error}")
        return False