from pydantic import BaseModel, EmailStr, Field
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
        
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    # mode: Optional[int] = Field(None, ge=0, le=3, description="Mode must be between 0 and 3")
    mode: Optional[int] = None
    
    class Config:
        from_attributes = True

class UserPasswordUpdate(BaseModel):
    password: str
    confirm_password: str

    class Config:
        from_attributes = True

class ShippingAddressBase(BaseModel):
    full_name:  Optional[str] = None
    phone:  Optional[str] = None
    address_line1:  Optional[str] = None
    address_line1:  Optional[str] = None
    city:  Optional[str] = None
    state:  Optional[str] = None
    country:  Optional[str] = None
    postal_code:  Optional[str] = None
    country:  Optional[str] = None
    is_default:  Optional[bool] = None

class ShippingAddressCreate(BaseModel):
    full_name: str = Field(..., max_length=100, description="Họ và tên người nhận")
    phone: str = Field(..., max_length=15, description="Số điện thoại của người nhận")
    address_line1: str = Field(..., description="Địa chỉ chính (vd: số nhà, đường)")
    address_line2: Optional[str] = Field(None, description="Địa chỉ phụ (vd: tòa nhà, tầng)")
    city: str = Field(..., max_length=100, description="Thành phố")
    state: Optional[str] = Field(None, max_length=100, description="Bang hoặc tỉnh")
    postal_code: str = Field(..., max_length=20, description="Mã bưu điện")
    country: str = Field(..., max_length=100, description="Quốc gia")
    is_default: Optional[bool] = Field(True, description="Đặt làm địa chỉ mặc định")

class ShippingAddressResponse(ShippingAddressBase):
    address_id: int
    user_id: int
    create_at: Optional[datetime] = None

    class Config:
        orm_mode = True        
