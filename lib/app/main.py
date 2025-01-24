from fastapi import FastAPI, Depends, HTTPException
from . import models,schemas
from .database import engine,get_db
from .routers import search,issue_book

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(search.router)
app.include_router(issue_book.router)


@app.get("/")
def root():
    return {"message": "Welcome to the library management system"}