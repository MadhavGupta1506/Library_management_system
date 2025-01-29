from fastapi import HTTPException,Depends,status,APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, schemas, utils, oauth2

# Initialize the API router for login functionality
router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/", response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Authenticate user and return a JWT token
    user = db.query(models.Users).filter(models.Users.email == credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!!")
    
    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!!")
    
    token = oauth2.create_access_token(data={"user_id": user.uid})
    return schemas.Token(token=token, token_type="bearer")
