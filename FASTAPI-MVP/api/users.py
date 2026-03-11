from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from schemas import User, UserCreate
from services.users import UserService
from database import get_db
from sqlalchemy.orm import Session
from models import User as UserModel

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    service = UserService(db)
    try:
        return service.create_user(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Login or email already exists")

@router.get("/me", response_model=User)
def get_current_user(db: Session = Depends(get_db)) -> User:
    users = db.query(UserModel).limit(1).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return User.model_validate(users[0])
