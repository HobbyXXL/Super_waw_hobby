from app.models.community import Community

class CommunityService:
    def __init__(self, db):
        self.db = db

    def create(self, user_id, data):
        community = Community(
            name=data.get("name"),
            slug=data.get("name"),
            creator_id=user_id
        )
        self.db.add(community)
        self.db.commit()
        self.db.refresh(community)
        return {"id": community.id, "name": community.name}

    def join(self, user_id, community_id):
        community = self.db.query(Community).filter(Community.id == community_id).first()

        if not community:
            return {"error": "community not found"}

        return {"msg": f"user {user_id} joined community {community_id}"}

    def get_members(self, community_id):
        return {"members": ["user1", "user2"]}