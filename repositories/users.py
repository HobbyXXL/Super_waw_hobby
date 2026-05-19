from sqlalchemy.orm import Session
from models.users import User
from schemas.users import UserRegisterRequest
from core.security import hash_password
import uuid

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserRegisterRequest):
        """
        Создаёт нового пользователя
        
        Args:
            user: UserRegisterRequest (login, email, password, role)
        
        Returns:
            User: Созданный объект пользователя
        """
        user_data = {
            "id": str(uuid.uuid4()),
            "login": user.login,
            "email": user.email,
            "password_hash": hash_password(user.password),
            "role": user.role,
            "is_verified": False
        }
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.flush()
        return db_user

    def get_by_login(self, login: str):
        """Получает пользователя по login"""
        return self.db.query(User).filter(User.login == login).first()

    def get_by_email(self, email: str):
        """Получает пользователя по email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: str):
        """Получает пользователя по ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def mark_as_verified(self, user_id: str):
        """Помечает пользователя как подтверждённого"""
        user = self.get_by_id(user_id)
        if user:
            user.is_verified = True
            user.verification_code = None
            user.verification_code_expires = None
            self.db.commit()
            return True
        return False