from fastapi import APIRouter

from .views import auth, categories, chats, orders, products, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(orders.router)
api_router.include_router(products.router)
api_router.include_router(chats.router)
api_router.include_router(categories.router)
