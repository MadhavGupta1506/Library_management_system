from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from . import schemas, models, database
from sqlalchemy.orm import Session

# Initialize the OAuth2 password bearer for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Constants for JWT token creation
SECRET_KEY = "uiwbcu1q32bv32bv92bn89c13h892cn3WNVN"
ALGORITHM = "HS256"
EXPIRATION_TIME = 50  # Token expiration time in minutes

# Function to create a new access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the access token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

# Function to get the current user based on the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.uid == token.id).first()
    return user

# Function to require a specific role for access
def require_role(required_role: list):
    def role_checker(user: models.Users = Depends(get_current_user)):
        if user.role not in required_role:
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient role")
        return user
    return role_checker
