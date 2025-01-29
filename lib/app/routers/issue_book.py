from fastapi import FastAPI,HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .. import schemas,models,database,utils,oauth2
from datetime import date

router=APIRouter(prefix="/book/issuebook",tags=["Issue/Return Book"])


@router.get("/")
def issue():
    return {"message": "Issue book"}

@router.post("/issue_book",status_code=status.HTTP_201_CREATED)
def issue_book(user_details:schemas.BookId,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user),role:str=Depends(oauth2.require_role(["librarian"]))):
    available=db.query(models.Book).filter(and_(models.Book.book_id==user_details.book_id, models.Book.status=="available")).first()
    if(not available):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Book with book_id {user_details.book_id} is already issued and unavailable currently!")
    
    available.status="issued"
    user=db.query(models.Users).filter(models.Users.uid==current_user.uid).first()
    
    
    issue=models.IssueBook(
    book_id=user_details.book_id,
    issue_date=date.today(),
    return_date=utils.get_return_date(date.today),
    uid=current_user.uid,
    
    user_name=user.user_name,
    email=user.email,
    mobile=user.mobile
    )
    
    db.add(issue)
    db.add(available)
    db.commit()
    db.refresh(available)
    
    return available



@router.post("/return_book/{book_id}")
def return_book(book_id:int,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user),role:str=Depends(oauth2.require_role(["librarian"]))):
    issued=db.query(models.IssueBook).filter(models.IssueBook.book_id==book_id).first()
    
    if not issued:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book is not issued yet!")
    book_status=db.query(models.Book).filter(models.Book.book_id==book_id).first()
    if not book_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found!")
    
    if(current_user.uid!=issued.uid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorized!")
    book_status.status="available"
    db.delete(issued)
    db.commit()
    
    db.refresh(book_status)
    return book_status