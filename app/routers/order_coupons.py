# app/routers/orderCoupons.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db
from typing import List

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

router = APIRouter(
    prefix="/api/orderCoupons",
    tags=["orderCoupons"],
)

# get all favorites
@router.get("/all")
def get_order_coupons_all(db: Session = Depends(get_db)):
    order_coupons = crud.get_order_coupons_all(db=db)
    if not order_coupons:
        raise HTTPException(status_code=404, detail="No order_coupons found")
    return order_coupons

