from fastapi import FastAPI, HTTPException,Depends,status,Response,APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .. import database,models,schemas,utils,oauth2

router=APIRouter(prefix="/login",tags=["Login"])

@router.post("/")
def login(credentials:schemas.LoginUser, db:Session=Depends(database.get_db)):
    user=db.query(models.Users).filter(models.Users.email==credentials.email).first()
    if( not user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials!!")
    if not utils.verify_password(credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials!!")
    token=oauth2.create_access_token(credentials.model_dump())
    return {"token":token,"token type":"bearer"}