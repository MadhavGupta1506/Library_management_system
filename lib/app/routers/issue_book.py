from fastapi import FastAPI,HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .. import schemas,models,database,utils
from datetime import date

router=APIRouter(prefix="/book/issuebook",tags=["Issue/Return Book"])


@router.get("/")
def issue():
    return {"message": "Issue book"}

@router.post("/issue_book")
def issue_book(user_details:schemas.UserDetails,db:Session=Depends(database.get_db)):
    available=db.query(models.Book).filter(and_(models.Book.book_id==user_details.book_id, models.Book.status=="available")).first()
    if(not available):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Book with book_id {user_details.book_id} is already issued and unavailable currently!")
    
    available.status="issued"
    
    issue=models.IssueBook(
    book_id=user_details.book_id,
    issue_date=date.today(),
    return_date=utils.get_return_date(date.today),
    uid=user_details.uid,
    user_name=user_details.user_name,
    email=user_details.email,
    mobile=user_details.mobile
    )
    
    db.add(issue)
    db.add(available)
    db.commit()
    db.refresh(available)
    
    return available



@router.post("/return_book/{book_id}")
def issue_book(book_id:int,db:Session=Depends(database.get_db)):
    issued=db.query(models.IssueBook).filter(models.IssueBook.book_id==book_id).first()
    
    if not issued:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book is not issued yet!")
    db.delete(issued)
    db.commit()
    book_status=db.query(models.Book).filter(models.Book.book_id==book_id).first()
    if not book_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found!")
    print(book_status)
    book_status.status="available"
    db.commit()
    
    db.refresh(book_status)
    return book_status
    