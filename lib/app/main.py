from fastapi import FastAPI, Depends, HTTPException
from . import models, schemas
from .database import engine, get_db
from .routers import search, issue_book, books_crud, users, login
import uvicorn
from .config import settings
# Create all database tables defined in the models
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Include routers for different functionalities
app.include_router(login.router)
app.include_router(users.router)
app.include_router(search.router)
app.include_router(issue_book.router)
app.include_router(books_crud.router)

@app.get("/")
def root():
    # Root endpoint that returns a welcome message
    return {"message": "Welcome to the library management system"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)