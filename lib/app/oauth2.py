from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from datetime import datetime,timedelta
from . import schemas,models,database
from sqlalchemy.orm import Session


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY="uiwbcu1q32bv32bv92bn89c13h892cn3WNVN"
ALGORITHM="HS256"
EXPIRATION_TIME=50


def create_access_token(data:dict):
    to_encode = data.copy()
    expire=datetime.now()+timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp":expire})
    
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=str(payload.get("user_id"))
        if not id:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

   
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    
    
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.Users).filter(models.Users.uid==token.id).first()
    return user


def require_role(required_role: list):
    def role_checker(user: models.Users = Depends(get_current_user)):
        if user.role not in required_role:
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient role")
        return user
    return role_checker