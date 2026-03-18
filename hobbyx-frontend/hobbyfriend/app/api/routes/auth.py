from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import AuthService
from app.api.deps import get_db

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(user.dict())

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(user.dict())
