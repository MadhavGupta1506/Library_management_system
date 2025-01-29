from datetime import timedelta, datetime, timezone
import datetime as dt
from passlib.context import CryptContext

# Function to calculate the return date based on the issue date
def get_return_date(issue_date):
    return (datetime.now() + timedelta(days=15)).date()

# Initialize the password context for hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Function to hash a password
def hash_password(password):
    return pwd_context.hash(password)

# Function to verify a plain password against a hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
