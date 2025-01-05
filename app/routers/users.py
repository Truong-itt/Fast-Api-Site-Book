# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

# get all users
@router.get("/", response_model=list[schemas.User])
def get_books(db: Session = Depends(get_db)):
    books = crud.get_all_data_users(db=db)
    if not books:
        raise HTTPException(status_code=404, detail="No users found")
    return books

# get user by id
# @router.get("/{id}", response_model=schemas.User)
@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db=db, user_id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

@router.get("/purchased_books/{id}", response_model=List[schemas.BookPurchase])
def get_books_purchased(user_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_purchased_by_user(db=db, user_id=user_id)
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this user")
    return books