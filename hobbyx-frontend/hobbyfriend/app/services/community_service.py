from app.models.community import Community
from app.utils.slug import generate_slug
import random
import string

class CommunityService:
    def __init__(self, db):
        self.db = db

    def create(self, user_id, data):
        name = data.get("name")
        if not name:
            return {"error": "Name required"}

        # Создаём базовый slug
        base_slug = generate_slug(name)
        slug = base_slug

        # Проверяем уникальность slug и при необходимости добавляем случайный суффикс
        while self.db.query(Community).filter(Community.slug == slug).first():
            slug = f"{base_slug}-{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"

        # Проверяем уникальность имени и при необходимости добавляем суффикс
        original_name = name
        counter = 1
        while self.db.query(Community).filter(Community.name == name).first():
            name = f"{original_name} ({counter})"
            counter += 1

        # Создаём сообщество
        community = Community(
            name=name,
            slug=slug,
            description=data.get("description"),
            is_private=data.get("is_private", False),
            creator_id=user_id
        )
        self.db.add(community)
        self.db.commit()
        self.db.refresh(community)

        return {"id": community.id, "name": community.name, "slug": community.slug}

    def join(self, user_id, community_id):
        community = self.db.query(Community).filter(Community.id == community_id).first()
        if not community:
            return {"error": "community not found"}
        return {"msg": f"user {user_id} joined community {community_id}"}

    def get_members(self, community_id):
        return {"members": ["user1", "user2"]}