from sqlalchemy.orm import Session
from models import Hobby as HobbyModel
from schemas import Hobby, HobbyCreate

class HobbyService:
    def __init__(self, db: Session):
        self.db = db

    def create_hobby(self, hobby: HobbyCreate) -> Hobby:
        db_hobby = HobbyModel(
            name=hobby.name,
            category=hobby.category,
            description=hobby.description
        )
        self.db.add(db_hobby)
        self.db.commit()
        self.db.refresh(db_hobby)
        return Hobby.model_validate(db_hobby)

    def get_all_hobbies(self):
        return [Hobby.model_validate(h) for h in self.db.query(HobbyModel).all()]

    def get_hobby_by_id(self, hobby_id: int):
        db_hobby = self.db.query(HobbyModel).filter(HobbyModel.id == hobby_id).first()
        return Hobby.model_validate(db_hobby) if db_hobby else None
