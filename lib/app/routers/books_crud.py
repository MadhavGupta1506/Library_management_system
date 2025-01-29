from fastapi import HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from .. import schemas,models,database,oauth2
from sqlalchemy import and_


router=APIRouter(prefix="/book",tags=["CRUD BOOK"])

@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
def add_book(book:schemas.BaseBook,db:Session=Depends(database.get_db),role:str=Depends(oauth2.require_role(["librarian"]))):
    
    available=db.query(models.Book).filter(and_(book.author==models.Book.author , book.title==models.Book.title)).first()
    
    if available:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Book with Author- {book.author} and Title- {book.title} already exist!!")
    
    new_book=models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.post("/delete/book_id/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id:int,db:Session=Depends(database.get_db),role:str=Depends(oauth2.require_role(["librarian"]))):
    
    available=db.query(models.Book).filter(id==models.Book.book_id).first()
    
    if not available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with Book_id {id} does not exist!")
    
    db.delete(available)
    db.commit()
    return {"message":"Book deleted successfully!!"}


@router.put("/update", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
def update_book(book:schemas.BookId,db:Session=Depends(database.get_db),role:str=Depends(oauth2.require_role(["librarian"]))):
    
    available=db.query(models.Book).filter(book.book_id==models.Book.book_id)
    print(available)
    if not available.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {book.book_id} does not exist!")    

    available.update(book.model_dump(),synchronize_session=False)
    db.commit()
    return available.first()
