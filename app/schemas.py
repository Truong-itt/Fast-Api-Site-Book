from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str]
    price: float
    stock: int

class BookCreate(BookBase):
    category_id: Optional[int]

class Book(BookBase):
    book_id: int
    created_at: datetime  

    class Config:
        from_attributes = True 

class ReviewBase(BaseModel):
    book_id: int
    user_id: int
    rating: int
    comment: Optional[str]

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int]
    comment: Optional[str]

class Review(ReviewBase):
    review_id: int
    created_at: str

    class Config:
        from_attributes = True 

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    order_id: int
    book_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    order_item_id: int


    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    total_amount: float
    status: str
    created_at: datetime


class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    order_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BookPurchase(BaseModel):
    book_id: int
    title: str
    author: str
    price: float
    quantity: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True
        