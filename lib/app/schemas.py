from pydantic import BaseModel
from datetime import date
from pydantic import EmailStr

class BaseBook(BaseModel):
    book_id:int
    title:str
    author:str
    category:str


class BookId(BaseModel):
    book_id:int


class Book(BaseModel):
    book_id:int
    title:str
    author:str
    category:str
    status:str
    class Config:
        from_attributes=True


    
class IssueBook(BaseModel):
    
    issue_date:date=None
    return_date:date=None
    
    
class CreateUser(BaseModel):
    user_name:str
    mobile:int
    email: EmailStr
    password:str
    role:str="member"
    class Config:
        from_attributes=True
        
class UserOut(BaseModel):
    user_name:str
    mobile:int
    email: EmailStr
    
    
class LoginUser(BaseModel):
    email: EmailStr
    password:str
    
class Token(BaseModel):
    token:str
    token_type:str
    
    
class TokenData(BaseModel):
    id:str=None
