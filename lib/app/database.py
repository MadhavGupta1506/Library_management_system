from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL defines the connection string for the PostgreSQL database.
# Format: "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/fastapi"

# Create an SQLAlchemy engine using the database URL.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory for managing database sessions.
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base class for declarative models.
Base = declarative_base()

# Dependency function to get a database session.
def get_db():
    db = sessionLocal()  # Create a new database session.
    try:
        yield db  # Yield the session for use in a request.
    finally:
        db.close()  # Close the session after use.
