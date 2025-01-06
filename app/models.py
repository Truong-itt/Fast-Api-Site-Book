from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Text,
    ForeignKey,
    Boolean,
    TIMESTAMP,
    DECIMAL,
    SmallInteger
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default="now()")

    orders = relationship("Order", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=True)
    
    books = relationship("Book", back_populates="category")

class Book(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    created_at = Column(TIMESTAMP, default="now()")

    category = relationship("Category", back_populates="books")
    order_items = relationship("OrderItem", back_populates="book")    

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, default="now()")
    status = Column(String(50), default="pending")

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    book = relationship("Book", back_populates="order_items")

class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(TIMESTAMP, default="now()")

    book = relationship("Book")
    user = relationship("User")

class Favorite(Base): 
    __tablename__ = "favorites"
    favorite_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    created_at = Column(TIMESTAMP, default="now()")

    book = relationship("Book")
    user = relationship("User")

class Coupon(Base): 
    __tablename__ = "coupons"
    coupon_id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), nullable=False)
    discount_percentage = Column(DECIMAL(10, 2), nullable=False)
    max_discount = Column(DECIMAL(10, 2), nullable=False)
    expiration_date = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, default="now()")
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    usage_limit = Column(Integer, default=0)
    times_used = Column(Integer, default=0)

    user = relationship("User")

class Order_coupon(Base):
    __tablename__ = "order_coupons"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    coupon_id = Column(Integer, ForeignKey("coupons.coupon_id"), nullable=False)
    discount_applied = Column(DECIMAL(10, 2), nullable=False, default=0)
    created_at = Column(TIMESTAMP, default="now()")

    order = relationship("Order")

class Payment_history(Base):
    __tablename__ = "payment_history"
    payment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    amount_paid = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(100), nullable=False)
    payment_status = Column(String(100), default="success")
    created_at = Column(TIMESTAMP, default="now()")
    
    user = relationship("User")
    order = relationship("Order")

class Shipping_address(Base):
    __tablename__ = "shipping_addresses"
    address_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    full_name = Column(String(100),  nullable=False)
    phone = Column(String(15),  nullable=False)
    address_line1 = Column(Text, nullable=False)
    address_line2 = Column(Text, nullable=False)
    city = Column(String(100),  nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20),  nullable=False)
    country = Column(String(100),  nullable=False)
    is_default = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default="now()")

    user = relationship("User")
