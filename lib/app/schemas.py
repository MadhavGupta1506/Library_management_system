from pydantic import BaseModel
from datetime import date
from pydantic import EmailStr
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
    