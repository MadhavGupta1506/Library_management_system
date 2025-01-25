from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from datetime import datetime,timedelta


SECRET_KEY="uiwbcu1q32bv32bv92bn89c13h892cn3WNVN"
ALGORITHM="HS256"
EXPIRATION_TIME=50


def create_access_token(data:dict):
    to_encode = data.copy()
    expire=datetime.now()+timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp":expire})
    
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt