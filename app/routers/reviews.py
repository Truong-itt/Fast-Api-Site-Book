# app/routers/reviews.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/api/reviews",
    tags=["reviews"],
)

# get all reviews
@router.get("/" )
def get_books(db: Session = Depends(get_db)):
    books = crud.get_all_data_reviews(db=db)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# get review by id
@router.get("/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_review_by_id(db=db, review_id=id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book



# 🟢 Tạo đánh giá mới
# @router.post("/", response_model=schemas.Review)
# def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
#     return crud.create_review(db=db, review=review)

# 🟡 Lấy danh sách đánh giá của một sách
# @router.get("/book/{book_id}", response_model=list[schemas.Review])
# def get_reviews_by_book(book_id: int, db: Session = Depends(get_db)):
#     reviews = crud.get_reviews_by_book(db=db, book_id=book_id)
#     if not reviews:
#         raise HTTPException(status_code=404, detail="No reviews found for this book")
#     return reviews

# 🟡 Lấy một đánh giá cụ thể
# @router.get("/{review_id}", response_model=schemas.Review)
# def get_review(review_id: int, db: Session = Depends(get_db)):
#     review = crud.get_review(db=db, review_id=review_id)
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     return review

# 🔵 Cập nhật đánh giá
# @router.put("/{review_id}", response_model=schemas.Review)
# def update_review(review_id: int, review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
#     updated_review = crud.update_review(db=db, review_id=review_id, review=review)
#     if not updated_review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     return updated_review

# 🔴 Xóa đánh giá
# @router.delete("/{review_id}")
# def delete_review(review_id: int, db: Session = Depends(get_db)):
#     deleted_review = crud.delete_review(db=db, review_id=review_id)
#     if not deleted_review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     return {"detail": "Review deleted successfully"}
