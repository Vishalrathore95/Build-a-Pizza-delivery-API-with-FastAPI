from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL (replace with your own MySQL credentials)
DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost/pizza"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Session Local (used to create sessions for interacting with the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare the base for your models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()