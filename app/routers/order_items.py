# app/routers/order_items.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/api/orderItems",
    tags=["orderItems"],
)

# get all users
@router.get("/")
def get_books(db: Session = Depends(get_db)):
    books = crud.get_all_data_orderItems(db=db)
    if not books:
        raise HTTPException(status_code=404, detail="No orderItems found")
    return books

# get user by id
@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_orderItem_by_id(db=db, orderItem_id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    return user