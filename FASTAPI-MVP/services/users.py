from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import User, UserCreate
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        db_user = UserModel(
            id=str(hash(user.login + str(datetime.utcnow())) % 10**18),
            login=user.login,
            email=user.email,
            password_hash=hashed_password,
            role=user.role,
            created_at=datetime.utcnow()
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User.model_validate(db_user)
