from fastapi import FastAPI,HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from .. import schemas,models,database,utils


router=APIRouter(prefix="/user",tags=["Users"])


@router.get("/{id}")
def get_user(id:int,db:Session=Depends(database.get_db)):
    user=db.query(models.Users).filter(models.Users.uid==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user



@router.post("/create_user",response_model=schemas.UserOut)
def create_user(user:schemas.CreateUser,db:Session=Depends(database.get_db)):
    if(len(str(user.mobile))!=10):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid mobile number!")
    try:
        
        hashed_password=utils.hash_password(user.password)
        user.password=hashed_password
        
        new_user=models.Users(**user.model_dump())
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User already exists!")
    return new_user




@router.post("/delete_user/{id}")
def delete_user(id:int,db:Session=Depends(database.get_db)):
    
    user=db.query(models.Users).filter(models.Users.uid==id).first()
    if(not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with uid {id} does not exist!")
    db.delete(user)
    db.commit()
    return {"message":"User deleted successfully"}

@router.put("/update_user/{id}")



def update_user(id:int,user:schemas.CreateUser,db:Session=Depends(database.get_db)):
    
    
    if(len(str(user.mobile))!=10):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid mobile number!")
    
    updated_user=db.query(models.Users).filter(models.Users.uid==id)
    if(not updated_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with uid {id} does not exist!")
    
    updated_user.update(user.model_dump(),synchronize_session=False)
    db.commit()
    return user
