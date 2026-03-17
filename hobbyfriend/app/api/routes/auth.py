from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(data: dict, db: Session = Depends(get_db_dep)):
    return AuthService(db).register(data)

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db_dep)):
    return AuthService(db).login(data)
