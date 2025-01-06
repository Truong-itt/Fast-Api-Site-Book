from fastapi import APIRouter
from .books import router as books_router
from .categories import router as categories_router
from .reviews import router as reviews_router
from .users import router as users_router
from .order_items import router as order_items_router
from .orders import router as orders_router
from .favorites import router as favorites_router
from .coupons import router as coupons_router 
from .order_coupons import router as order_coupons_router
from .payment_history import router as payment_history_router
from .shipping_addresses import router as shipping_addresses_router
# Tạo một router chính
router = APIRouter()

# Đăng ký các router con
router.include_router(books_router)
router.include_router(categories_router)
router.include_router(reviews_router)
router.include_router(users_router)
router.include_router(order_items_router)
router.include_router(orders_router)
router.include_router(favorites_router)
router.include_router(coupons_router)
router.include_router(order_coupons_router)
router.include_router(payment_history_router)
router.include_router(shipping_addresses_router)
