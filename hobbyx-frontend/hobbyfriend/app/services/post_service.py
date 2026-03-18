from app.models.post import Post

class PostService:
    def __init__(self, db):
        self.db = db

    def create_post(self, user_id, data):
        post = Post(
            author_id=user_id,
            content=data.get("content")
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return {"id": post.id, "content": post.content}

    def get_feed(self, user_id):
        return self.db.query(Post).all()

    def like_post(self, post_id):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return {"error": "post not found"}

        post.likes += 1 if hasattr(post, "likes") else 1
        self.db.commit()
        return {"likes": getattr(post, "likes", 1)}

    def add_comment(self, post_id, content):
        return {"msg": "comment added", "post_id": post_id, "content": content}