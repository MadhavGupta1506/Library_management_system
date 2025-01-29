from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,CheckConstraint,ForeignKey
from sqlalchemy.sql import text

class Book(Base):
    __tablename__="books"
    book_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    title=Column(String,nullable=False)
    author=Column(String,nullable=False)
    category=Column(String,nullable=False)
    status=Column(String,nullable=False,server_default='available')


    
class Users(Base):
    __tablename__="user_login"
    uid=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    user_name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    mobile=Column(Integer,nullable=False)
    password=Column(String,nullable=False)
    role=Column(String,nullable=False)
    

class IssueBook(Base):
    __tablename__="issue_books"
    uid=Column(Integer,ForeignKey("user_login.uid",ondelete="CASCADE"),primary_key=True,nullable=False)
    book_id=Column(Integer,ForeignKey("books.book_id",ondelete="CASCADE"),primary_key=True,nullable=False)
    user_name=Column(String,nullable=False)
    email=Column(String,nullable=False)
    mobile=Column(Integer,nullable=False)
    issue_date=Column(TIMESTAMP,nullable=False)
    return_date=Column(TIMESTAMP,nullable=False)
    