# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from typing import List

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

router = APIRouter(
    prefix="/api/orders",
    tags=["orders"],
)

# get all books
@router.get("/")
def get_books(db: Session = Depends(get_db)):
    books = crud.get_all_data_orders(db=db)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# get book by id
# @router.get("/{id}", response_model=schemas.OrderBase)
@router.get("/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_order_by_id(db=db, order_id=id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# get product has status = "completed"
@router.get("/completed/")
def get_books_completed(db: Session = Depends(get_db)):
    try:
        books = crud.get_orders_completed(db=db)
        logging.info('books: %s', books)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:  
        logging.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/cancelled/")
def get_books_cancelled(db: Session = Depends(get_db)):
    try:
        books = crud.get_orders_cancelled(db=db)
        logging.info('books: %s', books)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:  
        logging.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/pending/")
def get_books_pending(db: Session = Depends(get_db)):
    try:
        books = crud.get_orders_pending(db=db)
        logging.info('books: %s', books)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:  
        logging.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/processing/")
def get_books_pending(db: Session = Depends(get_db)):
    try:
        books = crud.get_orders_processing(db=db)
        logging.info('books: %s', books)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:  
        logging.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/shipped/")
def get_books_pending(db: Session = Depends(get_db)):
    try:
        books = crud.get_orders_shipped(db=db)
        logging.info('books: %s', books)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:  
        logging.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
