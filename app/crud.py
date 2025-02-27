# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from app.schemas import UserCreate
# from app.utils import hash_password 

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Tạo đánh giá mới
def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# Lấy tất cả đánh giá của một sách
def get_reviews_by_book(db: Session, book_id: int):
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()

# Lấy đánh giá cụ thể
def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.review_id == review_id).first()

# Cập nhật đánh giá
def update_review(db: Session, review_id: int, review: schemas.ReviewUpdate):
    db_review = db.query(models.Review).filter(models.Review.review_id == review_id).first()
    if not db_review:
        return None
    for key, value in review.dict(exclude_unset=True).items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

# Xóa đánh giá
def delete_review(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.review_id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review


def get_all_data_books(db: Session):
    return db.query(models.Book).all()

def get_all_data_users(db: Session):
    return db.query(models.User).all()

def get_all_data_categories(db: Session):
    return db.query(models.Category).all()

def get_all_data_orders(db: Session):
    return db.query(models.Order).all()

def get_all_data_orderItems(db: Session):
    return db.query(models.OrderItem).all()

def get_all_data_reviews(db: Session):
    return db.query(models.Review).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.category_id == category_id).first()

def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.order_id == order_id).first()

def get_review_by_id(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.review_id == review_id).first()

def get_orderItem_by_id(db: Session, orderItem_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.order_item_id == orderItem_id).first()

def get_books_by_category(db: Session, category_id: int):
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()


def get_books_purchased_by_user(db: Session, user_id: int):
    result = (
        db.query(
            models.Book.book_id.label("book_id"),
            models.Book.title.label("title"),
            models.Book.author.label("author"),
            models.Book.price.label("price"),
            models.OrderItem.quantity.label("quantity"),
        )
        .join(models.Order, models.Order.order_id == models.OrderItem.order_id)
        .join(models.Book, models.Book.book_id == models.OrderItem.book_id) 
        .filter(models.Order.user_id == user_id)  
        .all()
    )
    return result

def get_orders_completed(db: Session):
    result = (
        db.query(models.Order)
        .filter(models.Order.status == "completed")
        .all()
    )
    return result

def get_orders_cancelled(db: Session):
    result = (
        db.query(models.Order)
        .filter(models.Order.status == "cancelled")
        .all()
    )
    return result

def get_orders_pending(db: Session):
    result = (
        db.query(models.Order)
        .filter(models.Order.status == "pending")
        .all()
    )
    return result

def get_orders_processing(db: Session):
    result = (
        db.query(models.Order)
        .filter(models.Order.status == "processing")
        .all()
    )
    return result

def get_orders_shipped(db: Session):
    result = (
        db.query(models.Order)
        .filter(models.Order.status == "shipped")
        .all()
    )
    return result

def get_order_by_status (db: Session, status: str):
    return db.query(models.Order).filter(models.Order.status == status).all()

def get_reviews_by_user(db: Session, user_id: int):
    return db.query(models.Review).filter(models.Review.user_id == user_id).all()
    
def get_orderItem_by_order(db: Session, order_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    
def get_favorites_all(db: Session):
    return db.query(models.Favorite).all()

def get_coupons_all(db: Session):
    return db.query(models.Coupon).all()

def get_order_coupons_all(db: Session):
    return db.query(models.Coupon).all()

def get_order_coupons_all(db: Session):
    return db.query(models.Order_coupon).all()

def get_payment_history_all(db:Session):
    return db.query(models.Payment_history).all()

def get_shippingAddresses_all(db: Session):
    return db.query(models.Shipping_address).all()

def get_user_address(db: Session, user_id: int):
    return db.query(models.Shipping_address).filter(models.Shipping_address.user_id ==  user_id).all()

def get_user_favorite(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id ==  user_id).all()

def get_user_coupons(db: Session, user_id: int):
    return db.query(models.Coupon).filter(models.Coupon.user_id ==  user_id).all()

def get_book_reviews(db: Session, book_id: int):
    return db.query(models.Review).filter(models.Review.book_id ==  book_id).all()

def create_user(db: Session, user: UserCreate):
    # Mã hóa mật khẩu trước khi lưu vào DB
    # hashed_password = hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user
    return None

def update_user_info(db: Session, user_id: int, user: schemas.UserUpdate):
    """
    Cập nhật thông tin người dùng trong cơ sở dữ liệu
    """
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        return None

    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email
    if user.is_active is not None:
        db_user.is_active = user.is_active
    if user.mode is not None:
        if user.mode < 0 or user.mode > 3:
            raise ValueError("Mode must be between 0 and 3")
        db_user.mode = user.mode

    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(db: Session, user_id: int, user: schemas.UserPasswordUpdate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        if user.password != user.confirm_password:
            raise ValueError("Passwords do not match")
        db_user.password = user.password 
        db.commit()
        db.refresh(db_user)
    return db_user

def create_shipping_address(db: Session, address: schemas.ShippingAddressCreate, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not db_user:
        return ValueError("Not found user in db")
    
    if address.is_default:
        db.query(models.Shipping_address).filter(
            models.Shipping_address.user_id == user_id,
            models.Shipping_address.is_default == True
        ).update({"is_default": False}, synchronize_session=False)    
    new_address = models.Shipping_address(**address.dict(), user_id=user_id)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address
    # result = (
    #     db.query(models.Review)
    #     .
    # )
    # return db.query(models.Review).filter(models.Review.review_id == review_id).first()

# def create_user(db: Session, user: UserCreate):
#     # Mã hóa mật khẩu trước khi lưu vào DB
#     hashed_password = hash_password(user.password)
#     db_user = User(
#         name=user.name,
#         email=user.email,
#         password=hashed_password
#     )
#     db.add(db_user)
#     db.commit()  # Commit dữ liệu vào DB
#     db.refresh(db_user)  # Đảm bảo nhận dữ liệu cập nhật từ DB
#     return db_user