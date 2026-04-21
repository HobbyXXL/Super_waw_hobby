from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from api.hobbies import router as hobbies_router
from api.users import router as users_router
from api.auth import router as auth_router
from api.likes import router as likes_router
from api.portfolio import router as portfolio_router
from api.chats import router as chats_router 

common_router = APIRouter()

@common_router.get("/")
def root():
    return JSONResponse({"message": "HobbyX API — ready"}, status_code=status.HTTP_200_OK)

common_router.include_router(auth_router)
common_router.include_router(hobbies_router)
common_router.include_router(users_router)
common_router.include_router(portfolio_router)
common_router.include_router(likes_router)
common_router.include_router(chats_router)