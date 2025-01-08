# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/api/books",
    tags=["books"],
)

# get all books
@router.get("/", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    books = crud.get_all_data_books(db=db)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# get book by id
@router.get("/getBookId")
def get_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db=db, book_id=id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# get books by category
@router.get("/getBook/categoryId")
def get_books_by_category(category_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_category(db=db, category_id=category_id)
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this category")
    return books

@router.get("/reviews")
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews_book = crud.get_book_reviews(db=db, book_id=book_id)
    if not reviews_book:
        raise HTTPException(status_code=404, detail="No books found for this category")
    return reviews_book

# create book 
@router.post("/create", response_model=schemas.User)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)



