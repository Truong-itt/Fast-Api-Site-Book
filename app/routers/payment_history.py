# app/routers/coupons.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from typing import List

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

router = APIRouter(
    prefix="/api/paymentHistory",
    tags=["paymentHistory"],
)

# get all favorites
@router.get("/all")
def get_payment_history_all(db: Session = Depends(get_db)):
    payment_history = crud.get_payment_history_all(db=db)
    if not payment_history:
        raise HTTPException(status_code=404, detail="No payment_history found")
    return payment_history

