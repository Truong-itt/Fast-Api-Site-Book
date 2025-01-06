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
    prefix="/api/coupons",
    tags=["coupons"],
)

# get all favorites
@router.get("/all")
def get_coupons_all(db: Session = Depends(get_db)):
    coupons = crud.get_coupons_all(db=db)
    if not coupons:
        raise HTTPException(status_code=404, detail="No favorites found")
    return coupons

    