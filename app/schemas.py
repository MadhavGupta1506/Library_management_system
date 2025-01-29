from pydantic import BaseModel
from datetime import date
from pydantic import EmailStr

# Base model for book representation
class BaseBook(BaseModel):
    book_id: int
    title: str
    author: str
    category: str

# Model for book identification by ID
class BookId(BaseModel):
    book_id: int

# Model for book representation with status
class Book(BaseModel):
    book_id: int
    title: str
    author: str
    category: str
    status: str

    class Config:
        from_attributes = True

# Model for issuing books, including issue and return dates
class IssueBook(BaseModel):
    issue_date: date = None
    return_date: date = None

# Model for creating a new user
class CreateUser(BaseModel):
    user_name: str
    mobile: int
    email: EmailStr
    password: str
    role: str = "member"

    class Config:
        from_attributes = True

# Model for user output without sensitive data
class UserOut(BaseModel):
    user_name: str
    mobile: int
    email: EmailStr

# Model for user login credentials
class LoginUser(BaseModel):
    email: EmailStr
    password: str

# Model for JWT token response
class Token(BaseModel):
    token: str
    token_type: str

# Model for extracting token data
class TokenData(BaseModel):
    id: str = None
