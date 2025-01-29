from datetime import timedelta,datetime,timezone
import datetime as dt
from passlib.context import CryptContext


def get_return_date(issue_date):
    return (datetime.now()+timedelta(days=15)).date()




pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password,hash_password):
    return pwd_context.verify(plain_password,hash_password)