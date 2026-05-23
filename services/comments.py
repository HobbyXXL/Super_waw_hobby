from fastapi import HTTPException, status
from repositories.comments import CommentRepository
from schemas.comments import CommentSchema, CommentAuthor


class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    def list_comments(self, post_id: int) -> list[CommentSchema]:
        if not self.repo.get_post(post_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        rows = self.repo.list_for_post(post_id)
        return [self._to_schema(comment, user) for comment, user in rows]

    def add_comment(self, post_id: int, user_id: str, body: str) -> CommentSchema:
        if not self.repo.get_post(post_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        comment = self.repo.create(post_id, user_id, body.strip())
        row = self.repo.get_with_author(comment.id)
        if not row:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Comment create failed")
        return self._to_schema(row[0], row[1])

    @staticmethod
    def _to_schema(comment, user) -> CommentSchema:
        return CommentSchema(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            body=comment.body,
            created_at=comment.created_at,
            author=CommentAuthor(id=user.id, login=user.login),
        )
