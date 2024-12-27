from fastapi import APIRouter

from api.list_users import router as list_users_router
from api.create_user import router as create_user_router
from api.create_user_raise import router as create_user_raise_router
from api.get_user import router as get_user_router
from api.update_user import router as update_user_router
from api.bulk_create_example import router as bulk_create_example_router

users_router = APIRouter()
users_router.include_router(list_users_router)
users_router.include_router(create_user_router)
users_router.include_router(create_user_raise_router)
users_router.include_router(get_user_router)
users_router.include_router(update_user_router)
users_router.include_router(bulk_create_example_router)
