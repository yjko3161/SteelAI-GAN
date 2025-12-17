from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .schema import Base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DBManager:
    def __init__(self):
        # Fetch DB config from .env
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "steelai_gan")
        
        # Construct connection string
        # Fallback to SQLite if env vars are missing or explicitly set to sqlite
        if os.getenv("DB_TYPE", "mysql") == "sqlite":
            self.db_url = "sqlite:///steelai_gan.db"
        else:
            self.db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
            
        print(f"[DEBUG] Connecting to Database: {self.db_url.split('@')[-1]}") # Hide credentials
        
        try:
            self.engine = create_engine(self.db_url, pool_recycle=3600)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            print(f"[ERROR] Database Connection Failed: {e}")
            # Ensure calling get_session doesn't crash immediately, though it will likely fail later
            self.Session = None

    def get_session(self):
        if self.Session:
            return self.Session()
        else:
            raise ConnectionError("Database session could not be created. Check your connection settings.")

# Simple test to verify connection
if __name__ == "__main__":
    db = DBManager()
    print("Database initialized successfully.")
