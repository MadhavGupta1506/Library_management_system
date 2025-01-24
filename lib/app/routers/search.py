from fastapi import FastAPI,HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from .. import schemas,models,database

router=APIRouter(prefix="/book/search",tags=["Search"])

@router.get("/id/{id}",response_model=schemas.Book)
def get_book(id:int,db:Session=Depends(database.get_db)):
    book=db.query(models.Book).filter(models.Book.book_id==id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {id} does not exist")
    return book 

@router.get("/title/{title}",response_model=schemas.Book)
def get_book_by_title(title:str, db: Session = Depends(database.get_db)):
    title_names=db.query(models.Book).filter(models.Book.title==title).first()    
    
    if not title_names:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with title {title} does not exist")
    return title_names 


@router.get("/authors/{author}",response_model=list[schemas.Book])
def get_book_by_author(author:str, db: Session = Depends(database.get_db)):
    author_names=db.query(models.Book).filter(models.Book.author==author).all()
    if not author_names:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with Author name {author} does not exist")
    return author_names 

@router.get("/category/{category}",response_model=list[schemas.Book])
def get_book_by_category(category:str, db: Session = Depends(database.get_db)):
    books=db.query(models.Book).filter(models.Book.category==category).all()
    print(books)
    
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with category {category} does not exist")
    
    return books


