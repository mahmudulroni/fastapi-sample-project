from fastapi import APIRouter

from app.modules.auth.routes import router as auth_router
from app.modules.user.routes import router as user_router
from app.modules.post.routes import router as post_router
from app.modules.category.routes import router as category_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(post_router, prefix="/posts", tags=["Posts"])
api_router.include_router(category_router, prefix="/categories", tags=["Categories"])
