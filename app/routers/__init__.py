from fastapi import APIRouter
from .books import router as books_router
from .categories import router as categories_router
from .reviews import router as reviews_router
from .users import router as users_router
from .order_items import router as order_items_router
from .orders import router as orders_router

# Tạo một router chính
router = APIRouter()

# Đăng ký các router con
router.include_router(books_router)
router.include_router(categories_router)
router.include_router(reviews_router)
router.include_router(users_router)
router.include_router(order_items_router)
router.include_router(orders_router)
