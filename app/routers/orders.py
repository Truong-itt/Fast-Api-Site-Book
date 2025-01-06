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
@router.get("/all")
def get_books(db: Session = Depends(get_db)):
    books = crud.get_all_data_orders(db=db)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# get book by id
# @router.get("/{id}", response_model=schemas.OrderBase)
@router.get("/")
def get_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_order_by_id(db=db, order_id=id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# truyen vao trạng thai status thuc hien tim kiem
# completed - cancelled - pending - processing - shipped
@router.get("/status")
def get_book_status(status: str, db: Session = Depends(get_db)):
    book = crud.get_order_by_status(db=db, status=status)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/orderItem/")
def get_book_status(order_id: int, db: Session = Depends(get_db)):
    book = crud.get_orderItem_by_order(db=db, order_id=order_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


