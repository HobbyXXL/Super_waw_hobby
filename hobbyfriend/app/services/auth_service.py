from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, db):
        self.db = db

    def register(self, data):
        existing = self.db.query(User).filter_by(login=data["login"]).first()
        if existing:
            return {"error": "user exists"}

        user = User(
            id=data["login"],
            login=data["login"],
            email=data["email"],
            hashed_password=hash_password(data["password"])
        )

        self.db.add(user)
        self.db.commit()
        return {"msg": "created"}

    def login(self, data):
        user = self.db.query(User).filter_by(login=data["login"]).first()

        if not user:
            return {"error": "not found"}

        if not verify_password(data["password"], user.hashed_password):
            return {"error": "wrong password"}

        token = create_access_token({"sub": user.id})

        return {"access_token": token}