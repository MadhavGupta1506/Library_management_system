from fastapi import HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from .. import schemas,models,database,utils,oauth2


router=APIRouter(prefix="/user",tags=["Users"])


@router.get("/{id}")
def get_user(id:int,db:Session=Depends(database.get_db),role:str=Depends(oauth2.require_role(["admin"]))):
    user=db.query(models.Users).filter(models.Users.uid==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user



@router.post("/create_user",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.CreateUser,db:Session=Depends(database.get_db),role:str=Depends(oauth2.require_role(["admin"]))):
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
def delete_user(id:int,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user),role:str=Depends(oauth2.require_role(["admin","member"]))):
    
    user=db.query(models.Users).filter(models.Users.uid==id).first()
    if(not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with uid {id} does not exist!")
    
    if(user.uid!=current_user.uid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized")
    borrowed=db.query(models.IssueBook).filter(models.IssueBook.uid==current_user.uid).first()
    if( borrowed):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete your account while having borrowed books.")
    
    
    db.delete(user)
    db.commit()
    return {"message":"User deleted successfully"}

@router.put("/update_user/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def update_user(id:int,user:schemas.CreateUser,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user),role:str=Depends(oauth2.require_role(["admin","member"]))):
    
    if(len(str(user.mobile))!=10):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid mobile number!")
    
    updated_user=db.query(models.Users).filter(models.Users.uid==id)
    
    if(not updated_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with uid {id} does not exist!")
    
    if(updated_user.first().uid!=current_user.uid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized")
    
    updated_user.update(user.model_dump(),synchronize_session=False)
    db.commit()
    
    return user
