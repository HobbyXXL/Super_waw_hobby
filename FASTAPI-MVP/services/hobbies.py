from schemas import Hobby, HobbyCreate
from datetime import datetime
from typing import List, Optional

hobby_db = []

class HobbyService:
    def __init__(self):
        self.db = hobby_db

    def create_hobby(self, hobby: HobbyCreate) -> Hobby:
        hobby_id = 1 if not self.db else self.db[-1].id + 1
        new_hobby = Hobby(
            id=hobby_id,
            name=hobby.name,
            category=hobby.category,
            description=hobby.description,
            created_at=datetime.now()
        )
        self.db.append(new_hobby)
        return new_hobby

    def get_all_hobbies(self) -> List[Hobby]:
        return self.db

    def get_hobby_by_id(self, hobby_id: int) -> Optional[Hobby]:
        for h in self.db:
            if h.id == hobby_id:
                return h
        return None