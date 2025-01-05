# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
)

# get all books
@router.get("/", response_model=list[schemas.CategoryBase])
def get_books(db: Session = Depends(get_db)):
    books = crud.get_all_data_categories(db=db)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# get book by id
@router.get("/{id}", response_model=schemas.CategoryBase)
def get_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_category_by_id(db=db, category_id=id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
