from fastapi import HTTPException
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
import uuid

class AuthService:
    def __init__(self, db):
        self.db = db

    def register(self, data: dict):
        # Проверяем существует ли пользователь
        existing = self.db.query(User).filter_by(login=data["login"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(
            id=str(uuid.uuid4()),  # уникальный UUID
            login=data["login"],
            email=data["email"],
            hashed_password=hash_password(data["password"])
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return {"msg": "User created"}

    def login(self, data: dict):
        user = self.db.query(User).filter_by(login=data["login"]).first()

        if not user:
            raise HTTPException(status_code=400, detail="Invalid login or password")

        if not verify_password(data["password"], user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid login or password")

        token = create_access_token({"sub": user.id})
        return {"access_token": token, "token_type": "bearer"}