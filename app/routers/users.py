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
@router.get("/userId")
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db=db, user_id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

@router.get("/purchase/userId", response_model=List[schemas.BookPurchase])
def get_books_purchased(user_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_purchased_by_user(db=db, user_id=user_id)
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this user")
    return books

@router.get("/reviews/")
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    books = crud.get_reviews_by_user(db=db, user_id=user_id)
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this user")
    return books

@router.get("/address")
def get_user_address(user_id: int, db: Session = Depends(get_db)):
    address = crud.get_user_address(db=db, user_id=user_id)
    if not address:
        raise HTTPException(status_code=404, detail="No address found for this user")
    return address

@router.get("/favorite")
def get_user_favorite(user_id: int, db: Session = Depends(get_db)):
    favorite = crud.get_user_favorite(db=db, user_id=user_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="No favorite found for this user")
    return favorite

@router.get("/coupons")
def get_user_coupons(user_id: int, db: Session = Depends(get_db)):
    coupons = crud.get_user_coupons(db=db, user_id=user_id)
    if not coupons:
        raise HTTPException(status_code=404, detail="No coupons found for this user")
    return coupons

# create user
@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)
 
# delete user
# delete user
@router.delete("/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = crud.delete_user_by_id(db=db, user_id=user_id)
    return deleted_user

# cap nhat thong tin nguoi dung

@router.put("/update", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Cập nhật thông tin người dùng
    """
    print("Incoming Data:", user.dict())  # Ghi log dữ liệu đầu vào
    try:
        updated_user = crud.update_user_info(db=db, user_id=user_id, user=user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# Cập nhật mật khẩu người dùng
@router.put("/updatePassword")
def update_user_password(user_id: int, user: schemas.UserPasswordUpdate, db: Session = Depends(get_db)):
    try:
        updated_user = crud.update_user_password(db=db, user_id=user_id, user=user)
        return {"message": "Password updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the password")

# them dia chi  cho user
@router.post("/addAddress", response_model=schemas.ShippingAddressResponse)
def add_shipping_address(user_id: int, address: schemas.ShippingAddressCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_shipping_address(db, address, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
