from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from schemas import Hobby, HobbyCreate
from services import HobbyService
from typing import List

router = APIRouter(prefix="/hobbies", tags=["Hobbies"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_hobby(hobby: HobbyCreate, service: HobbyService = Depends()) -> JSONResponse:
    new_hobby = service.create_hobby(hobby)
    return JSONResponse(
        {"message": "Hobby created", "hobby": new_hobby.model_dump()},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/", response_model=List[Hobby])
def get_hobbies(service: HobbyService = Depends()) -> List[Hobby]:
    return service.get_all_hobbies()

@router.get("/{hobby_id}", response_model=Hobby)
def get_hobby(hobby_id: int, service: HobbyService = Depends()) -> Hobby:
    hobby = service.get_hobby_by_id(hobby_id)
    if not hobby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hobby not found")
    return hobby