from pydantic import BaseModel
from datetime import date
from pydantic import EmailStr

class BaseBook(BaseModel):
    title:str
    author:str
    category:str

class UpdateBook(BaseBook):
    book_id:int


class Book(BaseModel):
    book_id:int
    title:str
    author:str
    category:str
    status:str
    class Config:
        from_attributes=True

class UserDetails(BaseModel):
    uid:int
    book_id:int
    user_name:str
    mobile:int
    email: EmailStr
    
class IssueBook(UserDetails):
    issue_date:date=None
    return_date:date=None
    
    
class CreateUser(BaseModel):
    user_name:str
    mobile:int
    email: EmailStr
    password:str
    class Config:
        from_attributes=True
        
class UserOut(BaseModel):
    user_name:str
    mobile:int
    email: EmailStr
    
    
class LoginUser(BaseModel):
    email: EmailStr
    password:str