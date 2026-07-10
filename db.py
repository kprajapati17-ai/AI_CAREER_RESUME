import certifi
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# The user's connection URL
DATABASE_URL = "mysql+pymysql://3yGWmCTBFAKFap6.root:PP2lceh3tmfIoilq@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test"

# Fallback to local SQLite database if TiDB connection fails or contains placeholders
try:
    if "<CA_PATH>" in DATABASE_URL or "<PASSWORD>" in DATABASE_URL:
        raise ValueError("Database URL contains placeholder values.")

    # Remove query string parameters that cause PyMySQL connection errors
    base_url = DATABASE_URL.split("?")[0]
    
    engine = create_engine(
        base_url,
        pool_pre_ping=True,
        connect_args={
            "ssl": {
                "ca": certifi.where()
            }
        }
    )
    # Test connection
    with engine.connect() as conn:
        print("Connected to TiDB Cloud successfully.")
except Exception as e:
    print(f"TiDB Cloud connection failed ({e}). Falling back to local SQLite database...")
    SQLITE_URL = "sqlite:///local.db"
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False}
    )

sessionLocal = sessionmaker(bind=engine)
Base = declarative_base()