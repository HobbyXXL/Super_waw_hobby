from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from api.hobbies import router as hobbies_router

common_router = APIRouter()

@common_router.get("/")
def root():
    return JSONResponse({"message": "HobbyX API — ready"}, status_code=status.HTTP_200_OK)

common_router.include_router(hobbies_router)
