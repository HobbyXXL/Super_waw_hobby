from sqlalchemy.orm import Session
from sqlalchemy import func
from models import PortfolioWork as PortfolioWorkModel, User as UserModel, Like as LikeModel
from schemas import PortfolioWork, PortfolioWorkCreate
from datetime import datetime

class PortfolioService:
    def __init__(self, db: Session):
        self.db = db

    def create_portfolio_work(self, portfolio: PortfolioWorkCreate, user_id: str) -> PortfolioWork:
        db_portfolio = PortfolioWorkModel(
            user_id=user_id,
            title=portfolio.title,
            description=portfolio.description,
            file_url=portfolio.file_url,
            visibility=portfolio.visibility,
            activity_status=portfolio.activity_status,
            created_at=datetime.utcnow()
    )
        self.db.add(db_portfolio)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return PortfolioWork.model_validate(db_portfolio)

    def get_user_portfolio(self, user_id: str) -> list[PortfolioWork]:
        return [
            PortfolioWork.model_validate(p) 
            for p in self.db.query(PortfolioWorkModel)
            .filter(PortfolioWorkModel.user_id == user_id)
            .order_by(PortfolioWorkModel.created_at.desc())
            .all()
        ]

    def get_portfolio_by_id(self, portfolio_id: int) -> PortfolioWork | None:
        db_portfolio = self.db.query(PortfolioWorkModel).filter(
            PortfolioWorkModel.id == portfolio_id
        ).first()
        return PortfolioWork.model_validate(db_portfolio) if db_portfolio else None

    def get_public_feed(
        self,
        skip: int = 0,
        limit: int = 10,
        hobby_id: int | None = None,
        current_user_id: str | None = None,
    ) -> list[dict]:
        query = (
            self.db.query(PortfolioWorkModel, UserModel)
            .join(UserModel, PortfolioWorkModel.user_id == UserModel.id)
            .filter(PortfolioWorkModel.visibility == "public")
            .order_by(PortfolioWorkModel.created_at.desc())
        )
        if hobby_id is not None:
            query = query.filter(PortfolioWorkModel.hobby_id == hobby_id)
        rows = query.offset(skip).limit(limit).all()
        feed = []
        for post, author in rows:
            likes_count = (
                self.db.query(func.count(LikeModel.id))
                .filter(LikeModel.portfolio_id == post.id)
                .scalar()
            ) or 0
            liked = False
            if current_user_id:
                liked = (
                    self.db.query(LikeModel)
                    .filter(
                        LikeModel.portfolio_id == post.id,
                        LikeModel.user_id == current_user_id,
                    )
                    .first()
                    is not None
                )
            feed.append(
                {
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                    "file_url": post.file_url,
                    "activity_status": post.activity_status,
                    "hobby_id": post.hobby_id,
                    "created_at": post.created_at,
                    "likes_count": likes_count,
                    "liked": liked,
                    "author": {
                        "id": author.id,
                        "login": author.login,
                        "email": author.email,
                    },
                }
            )
        return feed

    def delete_portfolio_work(self, portfolio_id: int, user_id: str) -> bool:
        db_portfolio = self.db.query(PortfolioWorkModel).filter(
            PortfolioWorkModel.id == portfolio_id,
            PortfolioWorkModel.user_id == user_id
        ).first()
        
        if db_portfolio:
            from models import Like as LikeModel
            self.db.query(LikeModel).filter(
                LikeModel.portfolio_id == portfolio_id
            ).delete(synchronize_session=False)
            
            self.db.delete(db_portfolio)
            self.db.commit()
            return True
        return False
