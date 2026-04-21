from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from schemas import Hobby, HobbyCreate
from services.hobbies import HobbyService
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/hobbies", tags=["Hobbies"])

@router.post("/", response_model=Hobby, status_code=status.HTTP_201_CREATED)
def create_hobby(hobby: HobbyCreate, db: Session = Depends(get_db)) -> Hobby:
    service = HobbyService(db)
    try:
        return service.create_hobby(hobby)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Hobby with this name already exists")

@router.get("/", response_model=list[Hobby])
def get_hobbies(db: Session = Depends(get_db)) -> list[Hobby]:
    service = HobbyService(db)
    return service.get_all_hobbies()

@router.get("/{hobby_id}", response_model=Hobby)
def get_hobby(hobby_id: int, db: Session = Depends(get_db)) -> Hobby:
    service = HobbyService(db)
    hobby = service.get_hobby_by_id(hobby_id)
    if not hobby:
        raise HTTPException(status_code=404, detail="Hobby not found")
    return hobby
